from django.contrib import admin
from .models import User,Book,Genre,Rating
# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Rating)
