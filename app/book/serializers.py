from .models import Book, BookReview, Genre
from rest_framework import serializers


class BookListSerializer(serializers.ModelSerializer):
    """serializer for recipes"""
    author = serializers.CharField(source="author.name", read_only=True)
    genre = serializers.CharField(source="genre.title", read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'genre', 'author', 'rating']
        read_only_fields = ['id']


class ReviewListSerializer(serializers.ModelSerializer):
    """serializer for recipes"""

    class Meta:
        model = BookReview
        fields = ['id', 'title', 'description', 'rating', 'user']
        read_only_fields = ['id']


class BookDetailSerializer(BookListSerializer):
    """Serializer for book detail view"""
    reviews = ReviewListSerializer(many=True)
    in_fav = serializers.SerializerMethodField()

    def get_in_fav(self, obj):
        if not self.context['req'].user.is_anonymous:
            if self.context['req'].user.favourite_books.filter(
                    id=obj.pk
            ).exists():
                return True
        return False

    class Meta(BookListSerializer.Meta):
        fields = (BookListSerializer.Meta.fields +
                  ['description', 'created_at', 'reviews', 'author', 'in_fav'])


class GenresListSerializer(serializers.ModelSerializer):
    """serializer for book list request"""
    class Meta:
        model = Genre
        fields = ['id', 'title']
        read_only_fields = ['id']


class BookListRequestSerializer(serializers.Serializer):
    """serializer for book list request"""
    authors = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        default=None)
    genres = serializers.ListField(child=serializers.IntegerField(),
                                   required=False,
                                   default=None)
    page = serializers.IntegerField(required=True)
    limit = serializers.IntegerField(required=True)
    title = serializers.CharField(required=False, default=None)
    date_from = serializers.DateField(required=False, default=None)
    date_to = serializers.DateField(required=False, default=None)


class BookDetailRequestSerializer(serializers.Serializer):
    """serializer for book detail request"""
    id = serializers.IntegerField(required=True)


class AddBookToFavRequestSerializer(serializers.Serializer):
    """serializer for adding book to fav request"""
    id = serializers.IntegerField(required=True)


class LeaveReviewOnBookRequestSerializer(serializers.Serializer):
    """serializer for leaving review request"""
    book_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    rating = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """Creating review"""
        user = self.context['req'].user
        return BookReview.objects.create(
            user=user,
            **validated_data)
