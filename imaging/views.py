from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Device
from .models import RawImage, ClassificationResult
from .serializers import CaptureSerializer


@login_required
def capture_page(request):
    devices = Device.objects.filter(owner=request.user)
    return render(request, "capture.html", {"devices": devices})


class CaptureUploadView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CaptureSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        device = serializer.validated_data["device"]
        image = serializer.validated_data["image"]

        raw_image = RawImage.objects.create(
            device=device,
            image=image,
            notes="Captured via phone camera",
        )

        classification = ClassificationResult.objects.create(
            raw_image=raw_image,
            device=device,
            label="Pending Classification",
            confidence=0.0,
            status="pending",
            notes="Awaiting AI classification",
        )

        return Response(
            {
                "message": "Capture uploaded successfully",
                "raw_image_id": raw_image.id,
                "classification_id": classification.id,
            },
            status=status.HTTP_201_CREATED,
        )
