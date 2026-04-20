"""
Garbage/debris classifier using YOLOv8 pretrained model.
Detects floating waste objects relevant to bubble curtain monitoring.
"""
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Objects we care about for river garbage detection
GARBAGE_LABELS = {
    "bottle", "cup", "can", "plastic bag", "backpack", "handbag",
    "suitcase", "umbrella", "bowl", "banana", "apple", "orange",
    "carrot", "hot dog", "pizza", "donut", "cake", "chair",
    "potted plant", "vase", "scissors", "toothbrush", "hair drier",
    "teddy bear", "sports ball", "frisbee", "skateboard", "surfboard",
    "boat", "box", "bag",
}

_model = None

def get_model():
    """Load YOLOv8 model once and reuse."""
    global _model
    if _model is None:
        try:
            from ultralytics import YOLO
            _model = YOLO("yolov8n.pt")  # nano = fastest, good for prototype
            logger.info("YOLOv8 model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load YOLOv8 model: {e}")
            raise
    return _model


def classify_image(image_path: str) -> dict:
    """
    Run YOLOv8 on an image and return classification result.

    Returns:
        {
            "label": str,        # top detected label or "No Garbage Detected"
            "confidence": float, # 0.0 - 1.0
            "status": str,       # "completed" or "failed"
            "notes": str,        # all detections summary
        }
    """
    try:
        model = get_model()
        results = model(image_path, verbose=False)

        detections = []
        garbage_detections = []

        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls)]
                confidence = float(box.conf)
                detections.append(f"{label} ({confidence:.1%})")
                if label.lower() in GARBAGE_LABELS:
                    garbage_detections.append((label, confidence))

        # Sort garbage detections by confidence
        garbage_detections.sort(key=lambda x: x[1], reverse=True)

        if garbage_detections:
            top_label, top_conf = garbage_detections[0]
            all_garbage = ", ".join([f"{l} ({c:.1%})" for l, c in garbage_detections])
            return {
                "label": f"Garbage Detected: {top_label}",
                "confidence": top_conf,
                "status": "completed",
                "notes": f"Garbage found: {all_garbage}. All detections: {', '.join(detections) or 'none'}",
            }
        elif detections:
            return {
                "label": "No Garbage Detected",
                "confidence": 0.95,
                "status": "completed",
                "notes": f"Objects detected but none classified as garbage: {', '.join(detections)}",
            }
        else:
            return {
                "label": "No Objects Detected",
                "confidence": 0.0,
                "status": "completed",
                "notes": "No objects detected in the image.",
            }

    except Exception as e:
        logger.error(f"Classification failed for {image_path}: {e}")
        return {
            "label": "Classification Failed",
            "confidence": 0.0,
            "status": "failed",
            "notes": str(e),
        }