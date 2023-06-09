from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Halls)
admin.site.register(Movies)
admin.site.register(Reviews)
admin.site.register(Tickets)
admin.site.register(Movie_Hall_Allocation)
admin.site.register(Transaction)
admin.site.register(Highlights)