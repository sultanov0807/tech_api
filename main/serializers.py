from rest_framework import serializers

from .models import Category, Post, PImage

class CategorySerializer(serializers.ModelSerializer): #ModelSerializers используем
    class Meta:
        model = Category
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def to_representation(self, instance): #переопределяем в каком виде возвращется респонс
        rep = super().to_representation(instance)
        rep['images'] = PImageSerializer(instance.images.all(), many=True, context=self.context)
        return rep

class PImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PImage
        fields = '__all__'


