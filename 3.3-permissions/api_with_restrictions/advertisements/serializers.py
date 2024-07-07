from django.contrib.auth.models import User
from rest_framework import serializers
from django_filters import rest_framework as filters

from advertisements.models import Advertisement, AdvertisementStatusChoices


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""

        # Простановка значения поля создатель по-умолчанию.
        # Текущий пользователь является создателем объявления
        # изменить или переопределить его через API нельзя.
        # обратите внимание на `context` – он выставляется автоматически
        # через методы ViewSet.
        # само поле при этом объявляется как `read_only=True`
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        if len(data.get('description', '')) > 1000:
            raise serializers.ValidationError("Описание не может превышать 1000 символов.")

        return data


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    creator = filters.ModelChoiceFilter(
        field_name='creator',
        to_field_name='id',
        queryset=User.objects.all()
    )
    status = filters.ChoiceFilter(
        field_name='status',
        choices=AdvertisementStatusChoices.choices
    )

    class Meta:
        model = Advertisement
        fields = ['created_at', 'creator', 'status']
