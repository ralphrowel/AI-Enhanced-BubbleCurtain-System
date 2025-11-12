from rest_framework import serializers
from .models import Device, Signal

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ["id", "device", "timestamp", "value"]

class DeviceSerializer(serializers.ModelSerializer):
    signals = SignalSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = ["id", "name", "serial_number", "location", "owner", "signals"]
