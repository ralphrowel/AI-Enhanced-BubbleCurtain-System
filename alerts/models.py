from django.db import models
from imaging.models import ClassificationResult


class GarbageAlert(models.Model):
    classification = models.OneToOneField(
        ClassificationResult,
        on_delete=models.CASCADE,
        related_name="alert"
    )
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Garbage Alert"
        verbose_name_plural = "Garbage Alerts"

    def __str__(self):
        return f"Alert: {self.classification.label} @ {self.created_at:%Y-%m-%d %H:%M}"
