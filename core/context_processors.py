from imaging.models import ClassificationResult, RawImage
from api.models import Device

def dashboard_stats(request):
    if not request.path.startswith('/admin/'):
        return {}
    total_images = RawImage.objects.count()
    total_devices = Device.objects.count()
    garbage_detected = ClassificationResult.objects.filter(label__icontains="Garbage Detected").count()
    no_garbage = ClassificationResult.objects.filter(label__icontains="No").count()
    completed = ClassificationResult.objects.filter(status="completed").count()
    total_classified = garbage_detected + no_garbage
    detection_rate = round((garbage_detected / total_classified * 100) if total_classified > 0 else 0, 1)
    return {
        "stats_total_images": total_images,
        "stats_total_devices": total_devices,
        "stats_garbage": garbage_detected,
        "stats_clean": no_garbage,
        "stats_completed": completed,
        "stats_detection_rate": detection_rate,
    }
