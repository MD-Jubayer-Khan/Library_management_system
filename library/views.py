
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Transaction, Review, Category
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .forms import ReviewForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    user_profile = request.user.userprofile
    amount=book.borrowing_price
    
    if request.method == 'POST':
        if user_profile.balance >= book.borrowing_price:
            user_profile.balance -= book.borrowing_price
            user_profile.save()
            Transaction.objects.create(
                user=request.user,
                book=book,
                price=book.borrowing_price
            )
            send_email(request.user, amount, "Borrow Book Message", "borrowed_email.html")            
            return redirect('profile')

            
        else:
            return render(request, 'borrow_book.html', {'book': book, 'error': 'Insufficient balance'})
    return render(request, 'borrow_book.html', {'book': book})

@login_required
def return_book(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    if transaction.date_returned:
        return redirect('profile')
    transaction.date_returned = datetime.now()
    transaction.save()
    user_profile = request.user.userprofile
    user_profile.balance += transaction.price
    user_profile.save()
    amount = transaction.price
    send_email(request.user, amount, "Returned Book Message", "return_email.html")
    return redirect('profile')

@login_required
def review_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', book_id=book.id)
    else:
        form = ReviewForm()

    return render(request, 'review_book.html', {'book': book, 'form': form})

def book_list(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('selectedCategory')
    if selected_category:
        books = Book.objects.filter(categories__name=selected_category)
    else:
        books = Book.objects.all()
    return render(request, 'home.html', {'books': books, 'categories': categories})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    reviews = Review.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'reviews': reviews})


