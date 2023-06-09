from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("get_movies", views.get_movies, name = "get_movies"),
    path("movie_page", views.movie_page, name="movie_page"),
    path("get_seats", views.get_seats, name = "get_seats"),
    path("checkout", views.checkout, name = "checkout"),
    path("reserve_seat", views.reserve_seat, name = "reserve_seat"),
    path("profile", views.profile_page, name="profile_page"),
    path("get_qr", views.get_qr, name="get_qr"),
    path("post_comment", views.post_comment, name ="post_comment"),
    path("check_login", views.check_login, name = "check_login")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)