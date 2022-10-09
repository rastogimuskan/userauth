from rest_framework import serializers
from .models import NewUser, links

class UserRegistrationSerializers(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = NewUser
        fields = ['email', 'name', 'tc', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password didn't match with confirm password")
        return attrs

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)


class UserLoginSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = NewUser
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','email', 'name']


class UsercChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("Password didn't match with confirm password")
        user.set_password(password)
        user.save()
        return attrs

class ShowDynamicSerializer(serializers.ModelSerializer):
    class Meta:
        model = links
        fields = ['id', 'link']





