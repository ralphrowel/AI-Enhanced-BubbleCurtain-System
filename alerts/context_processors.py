def alert_count(request):
    if not request.path.startswith('/admin/'):
        return {}
    if not request.user.is_authenticated:
        return {}
    try:
        from alerts.models import GarbageAlert
        unread = GarbageAlert.objects.filter(is_read=False).count()
        recent_alerts = GarbageAlert.objects.filter(is_read=False).order_by("-created_at")[:5]
        return {
            "unread_alerts": unread,
            "recent_alerts": recent_alerts,
        }
    except Exception:
        return {}
