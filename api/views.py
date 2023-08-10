import json
from .serializers import *
from .permissions import *
from books.models import *
from users.models import *
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticated, IsLibrarian]
    serializer_class = BookCUDSerializer

    def perform_create(self, serializer):
        return super().perform_create(serializer)


class BookDeleteUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookCUDSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class MemberListCreateView(generics.ListCreateAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class MemberDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsLibrarian]


class BookListMemberView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = MemberBookSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def get_queryset(self):
        return self.queryset.filter(is_available=True)


class MemberBorrowedBooksView(generics.ListAPIView):
    serializer_class = MemberBookSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def get_queryset(self):
        user = self.request.user
        member = Member.objects.get(user=user)
        return member.borrowed_books.all()


class MemberDeleteView(generics.DestroyAPIView):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated, IsMember]

    def get_object(self):
        member = get_object_or_404(Member, user=self.request.user)
        return member

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Account deleted successfully"})


@api_view(['POST'])
@permission_classes([IsMember, IsAuthenticated])
def borrow_books(request):
    data = json.loads(request.body)
    book_ids = data['book_ids']
    member = get_object_or_404(Member, user=request.user)

    try:
        valid_ids = []

        for book_id in book_ids:
            try:
                book = Book.objects.get(id=book_id)
                if book.is_available:
                    book.is_available = False
                    book.save()
                    valid_ids.append(book_id)
                else:
                    return Response({'message': f'Book with ID {book_id} is not available for borrowing'})
            except Book.DoesNotExist:
                return Response({'message': f'Book with ID {book_id} does not exist'})

        member.borrowed_books.add(*valid_ids)
        return Response({'message': 'Books borrowed successfully'})

    except Member.DoesNotExist:
        return Response({'message': 'Member does not exist'})

    except User.DoesNotExist:
        return Response({'message': 'User does not exist'})


@api_view(['POST'])
@permission_classes([IsMember, IsAuthenticated])
def return_books(request):
    try:
        returned_book_ids = request.data['book_ids']
        member = get_object_or_404(Member, user=request.user)
        valid_book_ids = []
        borrowed_books_list = []
        borrowed_books = list(member.borrowed_books.all().values('id'))
        for books in borrowed_books:
            borrowed_books_list.append(books['id'])

        for book_id in returned_book_ids:
            try:
                book = Book.objects.get(id=book_id)
                if book_id in borrowed_books_list:
                    book.is_available = True
                    book.save()
                    valid_book_ids.append(book_id)
                else:
                    return Response({'message': f'You cannot return the book with id {book_id}'})
            except Book.DoesNotExist:
                pass

        member.borrowed_books.remove(*valid_book_ids)

        return Response({'message': 'Books returned successfully'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
