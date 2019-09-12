from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date, timedelta
from apps.log_reg_app.models import User

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 2 and postData['title'] in self.get_titles():
            errors['title'] = 'Book title should be at least 2 characters and must be unique'
        return errors

    def get_author_ids(self):
        ids = []
        authors = Author.objects.all()
        for author in authors:
            ids.append(author.id)
        return ids

    def get_titles(self):
        titles = []
        books = Book.objects.all()
        for book in books:
            titles.append(book.title)
        return titles

class AuthorManager(models.Manager):
    def author_validator(self, postData):
        errors = {}
        if len(postData['new_author']) < 5:
            errors['new_author'] = 'Author name must be at least 5 characters'
        return errors

    def get_author_names(self):
        names = []
        authors = Author.objects.all()
        for author in authors:
            names.append(author.author_name)
        return names

class ReviewManager(models.Manager):
    def review_validator(self, postData):
        errors = {}
        if len(postData['review']) < 10:
            errors['review'] = 'Review should be at least 10 characters'
        if int(postData['rating']) < 0 and int(postData['rating']) > 5:
            errors['rating'] = 'Rating must be between 0 and 5'
        return errors        

class Book(models.Model):
    title = models.CharField(max_length=255)
    author_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()

    def __repr__(self):
        return f"title: {self.title}, author_id: {self.author_id}"

    def get_book_ids(self):
        ids = []
        books = Book.objects.all()
        for book in books:
            ids.append(book.id)
        return ids


class Author(models.Model):
    author_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AuthorManager()

    def __repr__(self):
        return f"Author name: {self.author_name}"

class Review(models.Model):
    book_id = models.IntegerField()
    user_id = models.IntegerField()
    review = models.TextField()
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReviewManager()

    def __repr__(self):
        return f"book_id: {self.book_id}, user_id: {self.user_id}, review: {self.review}, rating: {self.rating}"

    def get_review_ids(self):
        ids = []
        reviews = Review.objects.all()
        for review in reviews:
            ids.append(review.id)
        return ids

