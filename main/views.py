from rest_framework import generics, viewsets
from main.models import Post, Category, PImage
from .serializers import PostSerializer, CategorySerializer, PImageSerializer


class CategoryListView(generics.ListAPIView): #листинк категории
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PImageView(generics.ListAPIView): #листинк картинки
    queryset = PImage.objects.all()
    serializer_class = PImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}