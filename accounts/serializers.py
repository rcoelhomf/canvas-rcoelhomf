from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'username', 'password', 'email', 'is_superuser']
        extra_kwargs = {'password': {'write_only': True},
                        'is_superuser': {'required': False},
                        'username': {'validators': [UniqueValidator(queryset=Account.objects.all(), message='A user with that username already exists.')]},
                        'email': {'validators': [UniqueValidator(queryset=Account.objects.all(), message='user with this email already exists.')]}}

    def create(self, validated_data):
        if validated_data['is_superuser']:
            return Account.objects.create_superuser(**validated_data)
        return Account.objects.create_user(**validated_data)


class AccountIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id']
        read_only_fields = ['id']


class AccountUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username']


class AccountEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['email']
