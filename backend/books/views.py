from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.utils import timezone

# Khassanov

from .models import Book, UserBook, ReadingLog, Review, Badge, UserBadge, UserProfile
from .serializers import (
    RegisterSerializer, LoginSerializer,
    BookSerializer, UserBookSerializer,
    ReadingLogSerializer, ReviewSerializer,
    UserBadgeSerializer,
)

def award_badges(user):
    """
    это у нас считает сколько книг прочитал(finished) юзер и 
    дает ему бадж в зависимости от этого, просто функция на питоне
    """
    
    finished_count = UserBook.objects.filter(user=user, status='finished').count()
    milestones = {
        'first_book': 1,
        'five_books':  5,
        'ten_books':  10,
    }
    for condition_key, threshold in milestones.items():
        if finished_count >= threshold:
            badge = Badge.objects.filter(condition_key=condition_key).first()
            if badge:
                UserBadge.objects.get_or_create(user=user, badge=badge)


# авторизация

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    # FBV с методом пост для создания пользователя который принимает данные и на выходе дает JWT токен
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
    serializer = LoginSerializer(data=request.data) #еще один FBV
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) #это функция выхода, соответственно только зашедший может выйти
def logout_view(request):
    try:
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response({'detail': 'Logged out.'})
    except Exception:
        return Response({'detail': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)


# профиль

# вот тут уже начинаются CBV 
class ProfileView(APIView):
    permission_classes = [IsAuthenticated] # паша фейс контроль

    def get(self, request):
        user = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        current_year = timezone.now().year

        finished_total = UserBook.objects.filter(user=user, status='finished').count() # основная инфа по пользователю, 
        reading = UserBook.objects.filter(user=user, status='reading').count()         # какие книги он прочел читает или хочет прочитать
        want_to_read = UserBook.objects.filter(user=user, status='want_to_read').count()
        finished_this_year = UserBook.objects.filter(
            user=user, status='finished'
        ).count()

        return Response({
            'username': user.username,
            'email': user.email,
            'reading_goal': profile.reading_goal,
            'stats': {
                'finished': finished_total,
                'reading': reading,
                'want_to_read': want_to_read,
                'finished_this_year': finished_this_year,
            }
        })

    def patch(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        goal = request.data.get('reading_goal') 
        if goal is not None:
            profile.reading_goal = goal
            profile.save()
        return Response({'reading_goal': profile.reading_goal})


# каталог

class AllBooksView(APIView):
    def get_permissions(self):
        if self.request.method == 'POST': # здесь реализован DRF хук который выбирает права
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get(self, request): 
        books = Book.objects.all()                              # GET /api/catalog/ этим методом только 
        return Response(BookSerializer(books, many=True).data)  # админ может пользоваться и тем что ниже(post)

    def post(self, request):
        many = isinstance(request.data, list)
        serializer = BookSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# список(my list)

class UserBookListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        status_filter = request.query_params.get('status')
        qs = UserBook.objects.filter(user=request.user).select_related('book')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return Response(UserBookSerializer(qs, many=True).data)

    def post(self, request):
        book_id = request.data.get('book_id')
        if UserBook.objects.filter(user=request.user, book_id=book_id).exists():
            return Response({'detail': 'Already in your list.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserBookSerializer(data=request.data)
        if serializer.is_valid():
            user_book = serializer.save(user=request.user)
            ReadingLog.objects.create(user=request.user, book=user_book.book, status='want_to_read')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserBookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return UserBook.objects.select_related('book').get(pk=pk, user=user)
        except UserBook.DoesNotExist:
            return None

    def get(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(UserBookSerializer(obj).data)

    def put(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        old_status = obj.status
        serializer = UserBookSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_status = serializer.validated_data.get('status')
            if old_status != new_status:
                ReadingLog.objects.create(user=request.user, book=obj.book, status=new_status)
            if old_status != 'finished' and new_status == 'finished':
                award_badges(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        old_status = obj.status
        serializer = UserBookSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            new_status = serializer.validated_data.get('status')
            if new_status and old_status != new_status:
                ReadingLog.objects.create(user=request.user, book=obj.book, status=new_status)
            if old_status != 'finished' and new_status == 'finished':
                award_badges(request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        obj = self.get_object(pk, request.user)
        if not obj:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# отзывы

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


class BookReviewsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, book_id):
        reviews = Review.objects.filter(book_id=book_id)
        return Response(ReviewSerializer(reviews, many=True).data)


class ReadingLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logs = ReadingLog.objects.filter(user=request.user).select_related('book').order_by('-date')
        return Response(ReadingLogSerializer(logs, many=True).data)

    def post(self, request):
        serializer = ReadingLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# награды

class UserBadgeListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_badges = UserBadge.objects.filter(user=request.user).select_related('badge')
        return Response(UserBadgeSerializer(user_badges, many=True).data)


class BulkDeleteBooksView(APIView):
    def get_permissions(self):
        return [IsAdminUser()]

    def delete(self, request):
        ids = request.data.get('ids', [])
        Book.objects.filter(id__in=ids).delete()
        return Response({'detail': f'Deleted {len(ids)} books.'}, status=status.HTTP_200_OK)