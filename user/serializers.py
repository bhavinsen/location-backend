from user.models import Message
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model




User = get_user_model()
class RegistraionSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            is_active=True,
            is_admin=False,
            city=validated_data['city'],
            state=validated_data['state'],
            zip=validated_data['zip'],
            country=validated_data['country'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
        )
        print("user",user)
        user.set_password(validated_data['password'])
        user.save()
        return user





class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, error_messages={
        'required': 'Please enter a valid email address.',
        'invalid': 'Please enter a valid email address.',
        'blank': 'Email address may not be blank'
    })
    password = serializers.CharField(
        max_length=50, allow_blank=True, required=False, default="")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',"email", "city", "state", "country", 'zip', 'latitude', 'longitude']
        

class MessageSerializer(serializers.Serializer):
    
    message = serializers.CharField(required=True, error_messages={
        'blank': 'message address may not be blank'
    })
    latitude = serializers.CharField(max_length=100, allow_blank=False)
    longitude = serializers.CharField(max_length=100, allow_blank=False)
    
    class Meta:
        model = Message
        fields = '__all__'
        
        
    def create(self, validated_data):
        message = Message.objects.create(
            message = validated_data['message'],
            latitude=validated_data['latitude'],
            longitude=validated_data['longitude'],
        )
        print("user",message)
        message.save()
        return message


