from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

from .models import QualityAssessment


def _blur_score(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    # Normalize variance of Laplacian to a useful 0..1 heuristic.
    score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    return round(min(score / 500.0, 1.0), 4)


def _estimate_skew(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                            minLineLength=max(100, image.shape[1] // 5), maxLineGap=20)
    if lines is None:
        return 0.0
    angles = []
    for x1, y1, x2, y2 in lines[:, 0]:
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        if abs(angle) <= 15:
            angles.append(angle)
    return round(float(np.median(angles)) if angles else 0.0, 3)


def _noise_level(image: np.ndarray) -> float:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    median = cv2.medianBlur(gray, 3)
    residual = cv2.absdiff(gray, median)
    return round(float(np.mean(residual)) / 32.0, 4)


def assess_quality(path: str | Path) -> QualityAssessment:
    image = cv2.imread(str(path), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Unable to read image: {path}")

    blur = _blur_score(image)
    skew = _estimate_skew(image)
    noise = _noise_level(image)
    height, width = image.shape[:2]

    # Conservative heuristic: restoration is only triggered when the scan
    # has meaningful blur/skew/noise. This deliberately avoids SR by default.
    problems = int(blur < 0.25) + int(abs(skew) > 1.0) + int(noise > 0.18)
    quality = "good" if problems == 0 else "fair" if problems == 1 else "poor"
    sr_required = width < 1200 or height < 1600 or blur < 0.15

    return QualityAssessment(
        blur_score=blur,
        skew_angle=skew,
        noise_level=noise,
        width=width,
        height=height,
        dpi=None,
        quality=quality,
        super_resolution_required=bool(sr_required and quality == "poor"),
    )
