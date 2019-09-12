from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.books_home),
    url(r'^add$', views.show_add_book),
    url(r'^new$', views.add_book),
    url(r'^(?P<book_id>\d+)$', views.show_book_reviews),
    url(r'^review/(?P<book_id>\d+)$', views.add_review),
    url(r'^delete/(?P<review_id>\d+)$', views.delete_review),
    url(r'^user/(?P<user_id>\d+)$', views.user_reviews),
    url(r'^logout$', views.log_out),]
