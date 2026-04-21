from django.contrib import admin
from django.utils.html import format_html
from .models import GarbageAlert


@admin.register(GarbageAlert)
class GarbageAlertAdmin(admin.ModelAdmin):
    list_display = ["alert_message", "device", "confidence", "is_read", "created_at", "mark_read_action"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["message"]
    actions = ["mark_all_read"]
    readonly_fields = ["classification", "message", "created_at"]

    def alert_message(self, obj):
        if not obj.is_read:
            return format_html(
                '<span style="color:#dc3545;font-weight:700;">🚨 {}</span>', obj.message
            )
        return format_html('<span style="color:#6c757d;">{}</span>', obj.message)
    alert_message.short_description = "Alert"

    def device(self, obj):
        return obj.classification.device
    device.short_description = "Device"

    def confidence(self, obj):
        return f"{obj.classification.confidence:.1%}"
    confidence.short_description = "Confidence"

    def mark_read_action(self, obj):
        if not obj.is_read:
            return format_html(
                '<a class="btn btn-sm btn-success" href="/admin/alerts/garbagealert/{}/mark-read/">✓ Dismiss</a>',
                obj.pk
            )
        return format_html('<span class="badge badge-secondary">Read</span>')
    mark_read_action.short_description = "Action"
    mark_read_action.allow_tags = True

    @admin.action(description="Mark selected alerts as read")
    def mark_all_read(self, request, queryset):
        queryset.update(is_read=True)
