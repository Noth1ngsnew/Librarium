# from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from .models import Book, ReadingLog, Review, Badge, UserBadge
from .serializers import (
    RegisterSerializer, LoginSerializer,
    BookSerializer, ReadingLogSerializer,
    ReviewSerializer, UserBadgeSerializer,
)


def award_badges(user):
    """
    здесь у нас идет проверка на награду, т.е мы поощеряем пользователя за
    прочитанные книги :)
    """
    finished_count = Book.objects.filter(owner=user, status='finished').count()
    milestones = {          # .filter() у нас возращает обычно список 
        'first_book': 1,    # но здесь вернет число прочитанных книг юзером,
        'five_books': 5,    # btw milestones is a term for a progress (этапы на русском)
        'ten_books':  10,
    }
    
    for condition_key, threshold in milestones.items():
        if finished_count >= threshold:
            badge = Badge.objects.filter(condition_key=condition_key).first()
            if badge:
                UserBadge.objects.get_or_create(user=user, badge=badge)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    """ 
    здесь и в функции ниже я настроил авторизацию через function based view, 
    обычно джанго функция принимает httprequest и отдает
    httpresponse, но @api_view позволяет нам получить request
    и response фактически работая только с тем что выбирает
    юзер, к примеру 'POST' или 'PUT' etc.
    """
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response(
            {'refresh': str(refresh), 'access': str(refresh.access_token)},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {'refresh': str(refresh), 'access': str(refresh.access_token)}
            )
        return Response(
            {'detail': 'Invalid credentials.'},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'detail': 'Logged out.'})
    except Exception:
        return Response(
            {'detail': 'Invalid refresh token.'},
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookListCreateView(APIView):
    """
    это у нас class based view 
    в первую очередь проверяется аутентификация
    он может и отдавать и создавать список объектов
    """

    permission_classes = [IsAuthenticated] # фейс контроль

    def get(self, request):
        status_filter = request.query_params.get('status')
        if status_filter:
            books = Book.objects.by_status(request.user, status_filter)
        else:
            books = Book.objects.filter(owner=request.user)
        return Response(BookSerializer(books, many=True).data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return Book.objects.get(pk=pk, owner=user)
        except Book.DoesNotExist:
            return None

    def get(self, request, pk):
        book = self.get_object(pk, request.user)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BookSerializer(book).data)

    def put(self, request, pk):
        book = self.get_object(pk, request.user)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        old_status = book.status
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            if old_status != 'finished' and serializer.validated_data.get('status') == 'finished':
                award_badges(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        book = self.get_object(pk, request.user)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        old_status = book.status
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            if old_status != 'finished' and serializer.validated_data.get('status') == 'finished':
                award_badges(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        book = self.get_object(pk, request.user)
        if not book:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# начало отзывов

class ReviewListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reviews = Review.objects.filter(user=request.user)
        return Response(ReviewSerializer(reviews, many=True).data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# конец отзывов

class ReadingLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = ReadingLog.objects.filter(user=request.user)
        return Response(ReadingLogSerializer(logs, many=True).data)

    def post(self, request):
        serializer = ReadingLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserBadgeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_badges = UserBadge.objects.filter(
            user=request.user
        ).select_related('badge')
        return Response(UserBadgeSerializer(user_badges, many=True).data)

