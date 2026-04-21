from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from imaging.models import RawImage, ClassificationResult
from api.models import Device


def home(request):
    return render(request, "home.html")


@login_required
def dashboard(request):
    total_images = RawImage.objects.count()
    total_devices = Device.objects.count()
    garbage_detected = ClassificationResult.objects.filter(label__icontains="Garbage Detected").count()
    no_garbage = ClassificationResult.objects.filter(label__icontains="No").count()
    failed = ClassificationResult.objects.filter(status="failed").count()
    completed = ClassificationResult.objects.filter(status="completed").count()

    recent_results = ClassificationResult.objects.select_related("raw_image", "device").order_by("-classified_at")[:10]

    # Detection rate
    total_classified = garbage_detected + no_garbage
    detection_rate = round((garbage_detected / total_classified * 100) if total_classified > 0 else 0, 1)

    context = {
        "total_images": total_images,
        "total_devices": total_devices,
        "garbage_detected": garbage_detected,
        "no_garbage": no_garbage,
        "failed": failed,
        "completed": completed,
        "recent_results": recent_results,
        "detection_rate": detection_rate,
    }
    return render(request, "dashboard.html", context)
