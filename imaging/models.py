from django.db import models

from django.db import models
from api.models import Device

class RawImage(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="raw_images/")
    captured_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Image from {self.device} at {self.captured_at}"

    class Meta:
        ordering = ["-captured_at"]


class ClassificationResult(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    raw_image = models.OneToOneField(RawImage, on_delete=models.CASCADE, related_name="result")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="classifications")
    label = models.CharField(max_length=255)
    confidence = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    classified_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.label} ({self.confidence:.2%}) - {self.device}"

    class Meta:
        ordering = ["-classified_at"]
