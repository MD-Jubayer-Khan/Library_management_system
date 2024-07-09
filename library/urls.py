from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='home'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow_book/<int:book_id>/', views.borrow_book, name='book_borrow'),
    path('review_book/<int:book_id>/', views.review_book, name='book_review'),
    path('return_book/<int:transaction_id>/', views.return_book, name='return_book'),
]
