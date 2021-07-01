
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework import serializers


User = get_user_model()


class RegSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, required=True)
    password_confirm = serializers.CharField(max_length=6, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь уже зарегистрирован')
        return email

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.pop('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Пароль не совпадает')
        return attrs

    def create(self, validated_data): #создаем
        user = User.objects.create(**validated_data)
        user.create_activation_code()
        User.send_activation_mail(user.email, user.activation_code)
        return User


class ActSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    activation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        activation_code = attrs.get('activation_code')
        if not User.objects.filter(email=email, activation_code=activation_code).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return attrs

    #если валидатция прошла мы активируем
    def activate(self):
        data = self.validated_data
        user = User.objects.get(**data)
        user.is_active = True
        user.activation_code = ''
        user.save()


class LogSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password, request=self.context.get('request'))
            if not user:
                raise serializers.ValidationError('Неверно указан email или праоль')
        else:
            raise serializers.ValidationError('Email и пароль обязателен')
        attrs['user'] = user
        return attrs


#востановаление

class RestPassSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError()
        return email

    def send_message(self):
        email = self.validated_data.get('email')
        new_pass = get_random_string(length=8)
        user = User.objects.get(email=email)
        user.set_password(new_pass)
        user.save()
        message = f'ваш новый пароль {new_pass}'
        send_mail(
            'Смена пароля',
            message,
            'sultanov0807@gmail.com',
            [email]
        )