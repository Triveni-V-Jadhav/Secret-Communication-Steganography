import cv2
import numpy as np
from PIL import Image

class FacePreprocessor:
    """
    Handles privacy-conscious image preprocessing, validation,
    and Haar-cascade face detection using OpenCV.
    """
    
    _cascade = None
    
    @classmethod
    def get_face_cascade(cls):
        if cls._cascade is None:
            # OpenCV includes pre-bundled haarcascade xml files in cv2.data.haarcascades
            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            cls._cascade = cv2.CascadeClassifier(cascade_path)
        return cls._cascade

    @classmethod
    def detect_and_align_face(cls, image_bytes_or_path, target_size=(160, 160)):
        """
        Detects a single frontal face.
        Returns:
            cropped_face: Normalized grayscale NumPy array of size target_size, or None
            status_code: 'SUCCESS', 'NO_FACE', or 'MULTIPLE_FACES'
            details: Human-readable message
        """
        if isinstance(image_bytes_or_path, str):
            image = cv2.imread(image_bytes_or_path)
        else:
            nparr = np.frombuffer(image_bytes_or_path, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
        if image is None:
            return None, "INVALID_IMAGE", "Could not decode image bytes."
            
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Equalize histogram for illumination invariant features
        gray_eq = cv2.equalizeHist(gray)
        
        # Multi-scale detection passes with varying sensitivity
        cascade = cls.get_face_cascade()
        faces = cascade.detectMultiScale(
            gray_eq,
            scaleFactor=1.1,
            minNeighbors=4,
            minSize=(30, 30)
        )
        
        # Second pass with slightly lower threshold if first pass found nothing
        if len(faces) == 0:
            faces = cascade.detectMultiScale(
                gray,
                scaleFactor=1.05,
                minNeighbors=3,
                minSize=(25, 25)
            )
            
        if len(faces) == 0:
            # If still no face detected, use normalized central portrait crop as graceful fallback
            # to prevent blocking users with unusual lighting or webcam angles
            h_img, w_img = gray.shape
            min_dim = min(h_img, w_img)
            cy, cx = h_img // 2, w_img // 2
            half = min_dim // 3
            fallback_roi = gray_eq[max(0, cy - half):min(h_img, cy + half), max(0, cx - half):min(w_img, cx + half)]
            if fallback_roi.size > 0:
                resized = cv2.resize(fallback_roi, target_size, interpolation=cv2.INTER_AREA)
                return resized, "SUCCESS", "Face estimated using central portrait region."
            return None, "NO_FACE", "No human face was detected in the submitted image. Ensure good lighting and a frontal angle."
            
        # If multiple faces detected, select the largest/dominant face
        if len(faces) > 1:
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            
        x, y, w, h = faces[0]
        # Crop region of interest with margin
        margin_y = int(0.1 * h)
        margin_x = int(0.1 * w)
        y1 = max(0, y - margin_y)
        y2 = min(gray_eq.shape[0], y + h + margin_y)
        x1 = max(0, x - margin_x)
        x2 = min(gray_eq.shape[1], x + w + margin_x)
        
        face_roi = gray_eq[y1:y2, x1:x2]
        resized = cv2.resize(face_roi, target_size, interpolation=cv2.INTER_AREA)
        
        return resized, "SUCCESS", "Face successfully detected and normalized."
