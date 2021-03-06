from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
]

urlpatterns += [   
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('book/<uuid:pk>/borrow/', views.borrow_book_instance, name='borrow-book'),
]
urlpatterns += [   
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [   
    path('borrowed/', views.BookInstanceListView.as_view(), name='borrowed-books'),
]

urlpatterns += [
    path('author_search/', views.AuthorSearchResultsView.as_view(), name='author_search_results'),
    path('book_search/', views.BookSearchResultsView.as_view(), name='book_search_results'),
    # path('book_instance_search/', views.BookInstanceSearchResultsView.as_view(), name='book_instance_search_results'),
]