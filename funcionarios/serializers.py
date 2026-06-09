from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Funcionario

class FuncionarioSerializer(serializers.ModelSerializer):

    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Funcionario
        fields = '__all__'

    def create(self, validated_data):

        username = validated_data.pop('username')
        password = validated_data.pop('password')

        user = User.objects.create_user(
            username=username,
            password=password
        )

        funcionario = Funcionario.objects.create(
            usuario=user,
            **validated_data
        )

        return funcionario