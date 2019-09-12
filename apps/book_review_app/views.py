from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Book, Author, Review
from apps.log_reg_app.models import User
from datetime import datetime, timedelta
import bcrypt



def books_home(request):
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")
        users = User.objects.all()
        reviews = Review.objects.all().order_by("-created_at")
        books = Book.objects.all()
        first_name = User.objects.get(id=user_id).first_name
        revObjs = []
        for i in range(3):
            revObjs.append({'title': Book.objects.get(id=reviews[i].book_id).title,
                            'book_id': reviews[i].book_id,
                            'rating': reviews[i].rating,
                            'first_name': User.objects.get(id=reviews[i].user_id).first_name,
                            'user_id': reviews[i].user_id,
                            'review': reviews[i].review,
                            'created_at': reviews[i].created_at})
        context = {'books': books, 'reviews':revObjs, 'users': users, 'first_name': first_name}
        return render(request, 'book_review_app/index.html', context)

def show_add_book(request):
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")
        authors = Author.objects.all()
        context = {'authors': authors,}
        return render(request, "book_review_app/new_book.html", context)    

def add_book(request):
    if request.method == "POST":
        user_id = request.session['user_id']
        title = request.POST['title']
        existing_author = request.POST['existing_author']
        new_author = request.POST['new_author']
        review = request.POST['review']
        rating = request.POST['rating']
        if existing_author:
            author_id = int(existing_author)
        else:
            errors = Author.objects.author_validator(request.POST)
            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/books/add")
        # Perform all other validations
        errors1 = Book.objects.book_validator(request.POST)
        errors2 = Review.objects.review_validator(request.POST)
        errors = dict(errors1, **errors2)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/books/add")
        if not existing_author:
            author_id = Author.objects.create(author_name=new_author).id
        book = Book.objects.create(title=title, author_id=author_id )
        review = Review.objects.create(book_id=book.id, user_id=user_id, review=review, rating=rating)
        return redirect(f"/books/{book.id}")
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")
        
def show_book_reviews(request, book_id):
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")
        author_id = Book.objects.get(id=book_id).author_id
        author_name = Author.objects.get(id=author_id).author_name
        title = Book.objects.get(id=book_id).title
        my_user_id = request.session['user_id']
        revObjs = []
        for review in Review.objects.all().filter(book_id=book_id):
            revObjs.append({'rating': review.rating,
                            'review_id': review.id,
                            'review': review.review,
                            'user': User.objects.get(id=review.user_id).first_name,
                            'user_id': review.user_id,
                            'created_at': review.created_at})
        context = {'author_name': author_name, 'reviews':revObjs, 'title': title, 'book_id': book_id, 'my_user_id': my_user_id}
        return render(request, "book_review_app/book_review.html", context)

def add_review(request, book_id):
    if request.method == "POST":
        user_id = request.session['user_id']
        book_id = request.POST['book_id']
        review = request.POST['review']
        rating = request.POST['rating']
        errors = Review.objects.review_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f"/books/{book_id}")
        else:
            review = Review.objects.create(book_id=book_id, user_id=user_id, review=review, rating=rating)
            return redirect(f"/books/{book_id}")
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")

def delete_review(request, review_id):
    if request.method == "POST":
        book_id = request.POST['book_id']
        review = Review.objects.get(id=review_id).delete()
        return redirect(f"/books/{book_id}")
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")

def user_reviews(request, user_id):
    if request.method == "GET":
        try:
            user_id = request.session['user_id']
        except:
            return redirect("/")
        user = User.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        reviews = []
        for review in Review.objects.all().filter(user_id=user_id):
            reviews.append({'book_id': review.book_id,
                            'title': Book.objects.get(id=review.book_id).title,})
        total_reviews = len(reviews)
        context = {'first_name': first_name, 'last_name': last_name, 'email': email, 'reviews': reviews, 'total_reviews': total_reviews}
        return render(request, "book_review_app/user.html", context)


def log_out(request):
    request.session.clear()
    return redirect("/")