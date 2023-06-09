import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import *
import math
from django.views.decorators.http import require_http_methods
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from datetime import datetime
from .models import *

# Create your views here.
def index(request):
    highlights = Highlights.objects.all()
    return render(request, "ticket_purchase/index.html", {
        "url_1": highlights[0].banner.url,
        "urls": [highlight.banner.url for highlight in highlights[1:]] if len(highlights) > 1 else []
    })


def check_login(request):
    if request.method == "GET":
        return JsonResponse({
            "message": request.user.is_authenticated
        })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "ticket_purchase/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "ticket_purchase/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "ticket_purchase/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "ticket_purchase/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "ticket_purchase/register.html")


def get_movies(request):
    if request.method == "GET":
        movies = [each.serialize() for each in Movies.objects.all().order_by("-release")]
        return JsonResponse({"movies": movies})
    else:
        return JsonResponse({"error": "invalid request method - {request.method}"})
    

def movie_page(request):
    movie_id = request.GET.get('movie_id')
    movie = Movies.objects.get(id = movie_id)
    reviews = Reviews.objects.filter(movie = movie).order_by("-timestamp")
    slots = [each.serialize() for each in Movie_Hall_Allocation.objects.filter(movie_id = movie_id).order_by("datetime_info")]
    to_return = movie.serialize()
    to_return["slots"] = slots
    to_return["comments"] = [review.serialize() for review in reviews]
    return render(request, "ticket_purchase/movie_page.html", to_return)


def profile_page(request):
    tickets_purchased = request.user.ticket_bought.all()
    transactions = Transaction.objects.filter(ticket__in = tickets_purchased).distinct().order_by("-id")

    to_return = []
    
    for transaction in transactions:
        ls = []
        seats = []
        for ticket in transaction.ticket.all():
            seats.append(
                f"{chr(int(ticket.seat_row) + 64)}{ticket.seat_column}"
            )
        ls.append(", ".join(seats))
        last_ticket = transaction.ticket.last()
        ls = [
            last_ticket.session.movie.title, 
            last_ticket.session.datetime_info, 
            last_ticket.session.hall.hall_num, 
            last_ticket.timestamp,
            len(transaction.ticket.all())*10,
            *ls,
            last_ticket.session.movie.thumbnail.url,
            transaction.id
        ]
        to_return.append(ls)

    return render(request, "ticket_purchase/profile.html", {
        "transactions": to_return
    })


def get_seats(request):
    if request.method == "GET":
        slot_id = request.GET.get('slot_id')
        to_return = Movie_Hall_Allocation.objects.get(id = slot_id).serialize()

        session = get_object_or_404(Movie_Hall_Allocation, id = slot_id)
        session_tickets = session.ticket.all()

        is_authenticated = request.user.is_authenticated

        if is_authenticated:
            reserved = session_tickets.filter(Q(holder=request.user) & Q(status='reserved'))

        return JsonResponse({
            "data": to_return,
            "user": request.user.username if is_authenticated else '',
            "unavailable": [ticket.serialize() for ticket in session_tickets],
            "reserved_by_user": [u.serialize() for u in reserved] if is_authenticated else []
        })
    else:
        return JsonResponse({"error": "Invalid request method - {request.method}"})
    

@login_required
@csrf_exempt
def get_qr(request):
    if request.method == "GET":
        transaction_id = request.GET.get('transaction_id')
        validation = Transaction.objects.get(id = transaction_id).validate_user(username=request.user.username)

        if validation["outcome"]:
            return JsonResponse({
                "url": Transaction.objects.get(id=transaction_id).qr_code.url
            })
        else:
            return JsonResponse({
                "error": "not authorized to view this ticket"
            })
    else:
        return JsonResponse({"error": "Invalid request method - {request.method}"})
    

@login_required
@csrf_exempt
def checkout(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        #check if seats are still avaiable
        for each in data:
            try:
                ticket_obj = Tickets.objects.get(
                    holder = request.user,
                    seat_row = each[0], 
                    seat_column = each[1],
                    session = Movie_Hall_Allocation.objects.get(id=each[2]),
                    status = 'reserved'
                )

            except ObjectDoesNotExist:
                return JsonResponse({
                    "message": "expired"
                })
        
        #create transaction entry for all tickets
        to_encode = ''
        for each in data:
            to_encode += f' {each[0]}-{each[1]}-{each[2]}'

        to_encode = to_encode.strip()
        
        qr = qrcode.QRCode(
            version=1,
            error_correction = qrcode.ERROR_CORRECT_L,
            box_size=10,
            border=4
        )

        #generate qrcode
        qr.add_data(to_encode)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color = "black", back_color = "white")
        
        #generate BytesIO object to store image temporarily
        qr_image_io = BytesIO()
        qr_image.save(qr_image_io)
        qr_image_io.seek(0)

        #add new transaction entry
        new_txn = Transaction.objects.create()
        new_txn.qr_code.save(
            f"qr_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png", 
            File(qr_image_io), 
            save=True
        )

        #create ticket entry for each ticket
        for each in data:
            ticket_obj = Tickets.objects.get(
                holder = request.user,
                seat_row = each[0], 
                seat_column = each[1],
                session = Movie_Hall_Allocation.objects.get(id=each[2]),
                status = 'reserved'
            )
            ticket_obj.status = 'sold'
            ticket_obj.transaction = new_txn
            ticket_obj.save()
        
        return JsonResponse({
            "message": "Success",
            "ticket": new_txn.qr_code.url
        })
    else:
        return JsonResponse({"error": "Invalid request method - {request.method}"})
    

@login_required
@csrf_exempt
def reserve_seat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if request.GET.get('action') == 'unreserve':
            Tickets.objects.get(
                holder = request.user,
                seat_row = data[0],
                seat_column = data[1],
                session = Movie_Hall_Allocation.objects.get(id = data[2]),
                status = 'reserved'
            ).delete()
            return JsonResponse({"message": "Success"})
        else:
            try:
                Tickets.objects.get(
                    seat_row = data[0],
                    seat_column = data[1],
                    session = Movie_Hall_Allocation.objects.get(id = data[2])
                )
                return JsonResponse({"message": "Conflict"})
            except:
                Tickets(
                    holder = request.user,
                    seat_row = data[0],
                    seat_column = data[1],
                    session = Movie_Hall_Allocation.objects.get(id = data[2]),
                    status = 'reserved'
                ).save()
                return JsonResponse({"message": "Success"})
    else:
        return JsonResponse({"error": "Invalid request method - {request.method}"})


@login_required
def post_comment(request):
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')
        movie_id = int(request.POST.get('id'))

        #check if rating and movie id is valid
        valid = (rating >= 0 and rating <=5) and (Movies.objects.filter(id=movie_id).exists())
        
        if valid:
            Reviews(
                author = request.user,
                rating = rating,
                comment = comment,
                movie = Movies.objects.get(id=movie_id)
            ).save()
        else:
            return JsonResponse({
                "error": "invalid input"
            })

        return JsonResponse({
            "message": "success"
        })
    else:
        return JsonResponse({"error": "Invalid request method - {request.method}"})