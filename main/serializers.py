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
        fields = ('id', 'title', 'category', 'created', 'text')

    def get_rating(self, instance):
        total_rating = sum(instance.reviews.values_list('rating', flat=True))
        reviews_count = instance.reviews.count()
        rating = total_rating / reviews_count if reviews_count > 0 else 0
        return round(rating, 1)

    # def get_like(self, instance):
    #     total_like = sum(instance.reviews.values_list('likes', flat=True))
    #     reviews_count = instance.reviews.count()
    #     likes = total_like if reviews_count > 0 else 0
    #     return round(likes, 1)

    def to_representation(self, instance): #переопределяем в каком виде возвращется респонс
        rep = super().to_representation(instance)
        rep['author'] = instance.author.email
        rep['category'] = CategorySerializer(instance.category).data
        rep['comments'] = CommentSerializer(instance.comments.all(), many=True).data
        rep['images'] = PImageSerializer(instance.image.all(), many=True, context=self.context).data
        rep['rating'] = RatingSerializer(instance.rating.all(), many=True).data
        # rep['likes'] = self.get_like(instance)

        return rep

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user
        validated_data['author'] = user_id
        post = Post.objects.create(**validated_data)
        return post


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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = "__all__"

    def validate_rating(self, rating):
        if not rating in range(1, 6):
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return rating

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['author'] = request.user
        return attrs