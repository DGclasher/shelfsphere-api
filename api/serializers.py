from users.models import *
from books.models import *
from rest_framework import serializers

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "is_available")


class BookCUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author")

    def create(self, validated_data):
        return Book.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.save()
        return instance

class UserUsernameField(serializers.RelatedField):
    def to_representation(self, value):
        return value.username

class MemberSerializer(serializers.ModelSerializer):
    user = UserUsernameField(read_only=True)

    class Meta:
        model = Member
        fields = ('id','user', 'borrowed_books',)


class MemberBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowBooksSerializer(serializers.Serializer):
    book_ids = serializers.ListField(child=serializers.IntegerField())

    def validate_book_ids(self, value):
        return value


