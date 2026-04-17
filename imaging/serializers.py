from rest_framework import serializers
from api.models import Device
from .models import RawImage, ClassificationResult


class CaptureSerializer(serializers.Serializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    image = serializers.ImageField()

    def validate_device(self, value):
        request = self.context.get("request")
        if value.owner != request.user:
            raise serializers.ValidationError("You can only capture for your own devices.")
        return value


class RawImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RawImage
        fields = ["id", "device", "image", "captured_at", "notes"]


class ClassificationResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassificationResult
        fields = ["id", "raw_image", "device", "label", "confidence", "status", "classified_at"]
