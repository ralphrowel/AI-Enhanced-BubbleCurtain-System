from django.contrib import admin

from django.contrib import admin
from .models import RawImage, ClassificationResult

@admin.register(RawImage)
class RawImageAdmin(admin.ModelAdmin):
    list_display = ["device", "captured_at", "notes"]
    list_filter = ["device", "captured_at"]
    search_fields = ["device__name"]

@admin.register(ClassificationResult)
class ClassificationResultAdmin(admin.ModelAdmin):
    list_display = ["label", "confidence", "device", "status", "classified_at"]
    list_filter = ["status", "device", "classified_at"]
    search_fields = ["label", "device__name"]