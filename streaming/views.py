from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def stream_broadcaster(request, room_name):
    """Phone opens this page to broadcast its camera."""
    return render(request, "stream_broadcast.html", {"room_name": room_name})

@login_required
def stream_viewer(request, room_name):
    """Laptop opens this page to watch the phone camera."""
    return render(request, "stream_view.html", {"room_name": room_name})
