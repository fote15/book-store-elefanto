"""
Views for book module
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Genre
from .serializers import BookListSerializer, BookListRequestSerializer, \
    BookDetailRequestSerializer, BookDetailSerializer, \
    LeaveReviewOnBookRequestSerializer, AddBookToFavRequestSerializer, \
    GenresListSerializer
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Q
from django.shortcuts import get_object_or_404


def get_serializer_data(req, serializer):
    request = serializer(data=req)
    if not request.is_valid():
        return None
    return request.data


@swagger_auto_schema(method='get',
                     query_serializer=BookListRequestSerializer)
@api_view(('GET',))
@permission_classes((AllowAny,))
def get_list_books(req):
    request = get_serializer_data(req.GET, BookListRequestSerializer)
    if not request:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Provide data')
    filters = {
        'title__icontains': request['title'],
        'author__in': request['authors'],
        'genre__in': request['genres'],
        'created_at__gte': request['date_from'],
        'created_at__lte': request['date_to'],
        'is_active': True,
    }
    queryset = Book.objects.filter(
        *[Q(**{k: v}) for k, v in filters.items() if v]
    ).all()[
               ((request['page'] - 1) * request['limit']):
               ((request['page'] - 1) * request['limit'])
               + request['limit']
               ]
    serializer = BookListSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(('GET',))
@permission_classes((AllowAny,))
def get_list_genres(req):
    queryset = Genre.objects.filter().all()
    serializer = GenresListSerializer(queryset, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='get',
                     query_serializer=BookDetailRequestSerializer)
@api_view(('GET',))
@permission_classes((AllowAny,))
def get_detail_book(req):
    context = {
        'req': req
    }
    request = get_serializer_data(req.GET, BookDetailRequestSerializer)
    if not request:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Provide data')

    queryset = get_object_or_404(Book, pk=request['id'])
    serializer = BookDetailSerializer(queryset, context=context)
    return Response(serializer.data)


@swagger_auto_schema(method='post',
                     request_body=LeaveReviewOnBookRequestSerializer)
@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def leave_review(req):
    context = {
        'req': req
    }
    review = LeaveReviewOnBookRequestSerializer(data=req.data, context=context)
    if not review.is_valid():
        return Response(status=status.HTTP_400_BAD_REQUEST, data=review.errors)
    review.save()
    return Response(status=status.HTTP_201_CREATED, data=review.data)


@swagger_auto_schema(method='post',
                     request_body=AddBookToFavRequestSerializer)
@api_view(('POST',))
@permission_classes((IsAuthenticated,))
def add_book_to_fav(req):
    request = get_serializer_data(req.data, AddBookToFavRequestSerializer)
    if not request:
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data='Provide data')
    book = get_object_or_404(Book, pk=request['id'])
    req.user.favourite_books.add(book)
    req.user.save()
    return Response(status=status.HTTP_201_CREATED, data='ok')
