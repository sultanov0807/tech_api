from django.db.models import Q
from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from main.models import Post, Category, PImage
from .serializers import PostSerializer, CategorySerializer, PImageSerializer, PostListSerializer


class CategoryListView(generics.ListAPIView): #листинк категории
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ] #для того чтобы можно было смотреть всем  катигорию


class PostsViewSet(viewsets.ModelViewSet):  #CRAD
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, ] #посты могуть смотреть только те кто авторизован

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