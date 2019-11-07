from .models import User
from rest_framework import serializers


class UserModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


# is same with UserModelSerializers
class SignupUserSerializers(serializers.Serializer):
    userId = serializers.CharField(max_length=20)
    userPw = serializers.CharField()
    userName = serializers.CharField(max_length=15)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.userId = validated_data.get('userId', instance.userId)
        instance.userPw = validated_data.get('userPw', instance.userPw)
        instance.userName = validated_data.get('userName', instance.userName)
        instance.save()
        return instance


class LoginUserSerializers(serializers.Serializer):
    userId = serializers.CharField(max_length=20)
    userPw = serializers.CharField(max_length=20)
