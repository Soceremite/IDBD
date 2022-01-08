from rest_framework import serializers
from server.models import User,Userinfo,Admin,Police,Mobile,Drink,Tired,Yawn,Blink,Smoke

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
class UserinfoSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Userinfo
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Admin
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

class PoliceSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Police
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }

class MobileSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Mobile
        fields = '__all__'

class DrinkSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Drink
        fields = '__all__'

class SmokeSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Smoke
        fields = '__all__'

class TiredSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Tired
        fields = '__all__'

class YawnSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Yawn
        fields = '__all__'

class BlinkSerializer(serializers.ModelSerializer):
    #user = UserSerializer()
    class Meta:
        model = Blink
        fields = '__all__'