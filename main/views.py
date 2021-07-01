from datetime import timedelta

from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from main.models import Post, Category, PImage, Like, Comment
from .serializers import *
from .permissions import IsPostAuthor


class CategoryListView(generics.ListAPIView): #листинк категории
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ] #для того чтобы можно было смотреть всем  катигорию


class PostsViewSet(viewsets.ModelViewSet):  #CRAD
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ] #посты могуть смотреть только те кто авторизован

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self): #любой аутентифицированный пользователь мог смотреть посты
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsPostAuthor, ]
        elif self.action in ['comment', 'like', 'rating']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = []
        return [permission() for permission in permissions]

    #Рейтинг
    @action(detail=True, methods=['POST'])
    def rating(self, request, pk):
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.data, status=400)


    #Лийк
    @action(detail=True, methods=['POST'])
    def like(self, request, pk):
        post = self.get_object()
        user = request.user
        like_obj, created = Like.objects.get_or_create(post=post, user=user)

        if like_obj.is_liked:
            like_obj.is_liked = False
            like_obj.save()
            return Response('disliked')
        else:
            like_obj.is_liked = True
            like_obj.save()
            return Response('like')

    #коммент
    @action(detail=True, methods=['POST'])
    def comment(self, request, pk):
        data = request.data.copy()
        data['post'] = pk
        serializer = CommentSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)


    #Филтрация по постам
    @action(detail=False, methods=['get'])
    def fil(self, request, pk=None):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



    #Поиск
    @action(detail=False, methods=['get'])  #Доступны только во ViewSet
    def find(self, request, pk=None):       # router builds path posts/find/?q=....
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |   #"|" или
                                   Q(text__icontains=q))
        serializer = PostSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PImageView(generics.ListCreateAPIView): #листинк картинки
    queryset = PImage.objects.all()
    serializer_class = PImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentViewSet(mixins.CreateModelMixin,
                     viewsets.GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
