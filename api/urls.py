from . import views
from .views import *
from django.urls import path

urlpatterns = [
    path('books/', BookListCreateView.as_view(), name='list_create_books'),
    path('books/<int:pk>/', BookDeleteUpdateView.as_view(),
         name='delete_update_books'),
    path('books/view/all', BookListMemberView.as_view(), name='list_books'),
    path('books/view/borrowed', MemberBorrowedBooksView.as_view(),
         name='borrowed_books'),
    path('members/', MemberListCreateView.as_view(), name='list_create_members'),
    path('members/<int:pk>/', MemberDetailView.as_view(),
         name='update_delete_members'),
    path('books/borrow/', views.borrow_books, name='borrow_books'),
    path('books/return/', views.return_books, name='return_books'),
    path('account/delete/', MemberDeleteView.as_view(), name='delete_account')
]
