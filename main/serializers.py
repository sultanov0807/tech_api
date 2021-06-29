from rest_framework import serializers

from .models import *


class CategorySerializer(serializers.ModelSerializer): #ModelSerializers используем
    class Meta:
        model = Category
        fields = '__all__'


class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'category', 'created', 'text', 'author')

    def to_representation(self, instance): #переопределяем в каком виде возвращется респонс
        rep = super().to_representation(instance)
        rep['images'] = PImageSerializer(instance.image.all(), many=True, context=self.context).data

        return rep


class PImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PImage
        fields = '__all__'

        def _get_image_url(self, obj):
            if obj.image:
                url = obj.image.url
                request = self.context.get('request')
                if request is not None:
                    url = request.build_absolute_uri(url)
            else:
                url = ''
            return url

        def to_representation(self, instance):  # переопределяем в каком виде возвращется респонс
            rep = super().to_representation(instance)
            rep['images'] = self._get_image_url(instance)
            return rep



