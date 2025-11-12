from django.db import models
from accounts.models import CustomUser

class Device(models.Model):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="devices")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Signal(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="signals")
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"
