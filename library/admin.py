from django.contrib import admin
from .models import Book, Category, UserProfile, Transaction, Review

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Transaction)
admin.site.register(Review)