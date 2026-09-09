from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .models import QualityAssessment


def _deskew(image: np.ndarray, angle: float) -> np.ndarray:
    if abs(angle) < 0.05:
        return image
    h, w = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_CUBIC,
                          borderMode=cv2.BORDER_REPLICATE)


def _crop_borders(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.threshold(gray, 245, 255, cv2.THRESH_BINARY_INV)[1]
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return image
    x, y, w, h = cv2.boundingRect(max(contours, key=cv2.contourArea))
    pad = 8
    x, y = max(0, x - pad), max(0, y - pad)
    return image[y:min(image.shape[0], y + h + 2 * pad),
                 x:min(image.shape[1], x + w + 2 * pad)]


def _sauvola(gray: np.ndarray) -> np.ndarray:
    try:
        from skimage.filters import threshold_sauvola
        threshold = threshold_sauvola(gray, window_size=31, k=0.2)
        return (gray > threshold).astype(np.uint8) * 255
    except ImportError:
        # Safe fallback when scikit-image is not installed.
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, 31, 11)


def restore_image(input_path: str | Path, output_path: str | Path,
                   quality: QualityAssessment, use_super_resolution: bool = False) -> Path:
    image = cv2.imread(str(input_path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Unable to read image: {input_path}")

    image = _deskew(image, quality.skew_angle)
    image = _crop_borders(image)
    image = cv2.fastNlMeansDenoisingColored(image, None, 7, 7, 7, 21)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = cv2.cvtColor(cv2.merge((clahe.apply(l), a, b)), cv2.COLOR_LAB2BGR)
    gray = cv2.cvtColor(enhanced, cv2.COLOR_BGR2GRAY)
    binary = _sauvola(gray)

    # Super-resolution is opt-in and only allowed when quality assessment says
    # it is necessary. Real-ESRGAN is loaded lazily because it is heavyweight.
    if use_super_resolution and quality.super_resolution_required:
        try:
            from realesrgan import RealESRGAN
            import torch
            model = RealESRGAN(torch.device("cuda" if torch.cuda.is_available() else "cpu"), scale=2)
            model.load_weights("weights/RealESRGAN_x2.pth", download=False)
            rgb = cv2.cvtColor(binary, cv2.COLOR_GRAY2RGB)
            binary = cv2.cvtColor(np.asarray(model.predict(rgb)), cv2.COLOR_RGB2GRAY)
        except (ImportError, FileNotFoundError):
            # Never fail the entire pipeline because optional SR is unavailable.
            pass

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    if not cv2.imwrite(str(output), binary):
        raise IOError(f"Unable to write restored image: {output}")
    return output
