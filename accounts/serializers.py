from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id","username","email","password","first_name","last_name")

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email",""),
            first_name=validated_data.get("first_name",""),
            last_name=validated_data.get("last_name",""),
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
