from google.cloud import vision
from typing import Dict, Any, List
import os, cv2
import numpy as np
import matplotlib.pyplot as plt

# 서비스 계정 키 환경변수 등록
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
    "C:/emotion_letter/app/tests/data/vision-key.json"
)


# 단어 단위
def run_gcp_ocr_words(image_path: str) -> List[Dict[str, Any]]:
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    words = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = "".join([s.text for s in word.symbols])
                    vertices = [(v.x, v.y) for v in word.bounding_box.vertices]
                    xs = [v[0] for v in vertices if v[0] is not None]
                    ys = [v[1] for v in vertices if v[1] is not None]
                    if xs and ys:
                        words.append(
                            {
                                "text": word_text,
                                "coords": (min(xs), min(ys), max(xs), max(ys)),
                            }
                        )
    return words


# 줄 단위
def run_gcp_ocr_lines(image_path: str) -> List[Dict[str, Any]]:
    client = vision.ImageAnnotatorClient()
    with open(image_path, "rb") as f:
        content = f.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    if response.error.message:
        raise Exception(f"Vision API Error: {response.error.message}")

    lines = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                # 문단(줄) 단위 텍스트와 전체 좌표 묶기
                line_text = ""
                all_vertices = []

                for word in paragraph.words:
                    word_text = "".join([s.text for s in word.symbols])
                    line_text += word_text + " "
                    all_vertices.extend(
                        [(v.x, v.y) for v in word.bounding_box.vertices]
                    )

                if not line_text.strip():
                    continue

                # 전체 문단을 포함하는 bounding box 계산
                xs = [v[0] for v in all_vertices if v[0] is not None]
                ys = [v[1] for v in all_vertices if v[1] is not None]
                if not xs or not ys:
                    continue

                x_min, y_min, x_max, y_max = min(xs), min(ys), max(xs), max(ys)

                lines.append(
                    {"text": line_text.strip(), "coords": (x_min, y_min, x_max, y_max)}
                )

    return lines


# crop 함수
def crop_regions(
    image_path: str, boxes: List[Dict[str, Any]], padding: int = 10
) -> List[Dict[str, Any]]:
    img = cv2.imread(image_path)
    h, w, _ = img.shape
    crops = []

    for box in boxes:
        x_min, y_min, x_max, y_max = box["coords"]
        x_min = max(0, x_min - padding)
        y_min = max(0, y_min - padding)
        x_max = min(w, x_max + padding)
        y_max = min(h, y_max + padding)

        crop = img[y_min:y_max, x_min:x_max]
        if crop.size == 0:
            continue

        crops.append(
            {"text": box["text"], "image": crop, "coords": (x_min, y_min, x_max, y_max)}
        )
    return crops


# 투명 배경 변환
def make_transparent_clean(crop: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

    # 글자 픽셀만 추출 (Otsu threshold 반전)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 작은 점/노이즈 제거
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 외곽선 부드럽게 (GaussianBlur → 알파 채널 부드럽게)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)

    # BGR + 알파 합치기
    b, g, r = cv2.split(crop)
    rgba = cv2.merge([b, g, r, mask])
    return rgba


# 알파 블렌딩
def overlay_image_alpha(bg: np.ndarray, fg: np.ndarray, x: int, y: int) -> np.ndarray:
    h, w = fg.shape[:2]
    if y + h > bg.shape[0] or x + w > bg.shape[1]:
        return bg

    roi = bg[y : y + h, x : x + w]
    fg_bgr = fg[:, :, :3]
    alpha = fg[:, :, 3] / 255.0

    for c in range(3):
        roi[:, :, c] = (1 - alpha) * roi[:, :, c] + alpha * fg_bgr[:, :, c]

    bg[y : y + h, x : x + w] = roi
    return bg


def fit_to_background(orig_w, orig_h, bg_w, bg_h):
    """
    OCR 원본과 편지지 배경의 비율 차이를 자동으로 맞춰주는 함수
    - 원본 비율을 유지하면서 배경에 맞게 스케일링
    - 남는 여백은 중앙 정렬
    """
    # 비율 계산
    scale_x = bg_w / orig_w
    scale_y = bg_h / orig_h

    # 가장 작은 스케일 선택 (비율 유지)
    scale = min(scale_x, scale_y)

    # 비율 유지된 실제 크기
    new_w = int(orig_w * scale)
    new_h = int(orig_h * scale)

    # 중앙 정렬 여백 계산
    offset_x = (bg_w - new_w) // 2
    offset_y = (bg_h - new_h) // 2

    return scale, offset_x, offset_y


def overlay_on_background(bg_path, line_crops, orig_w, orig_h):
    # 1. 배경 이미지 불러오기
    bg = cv2.imread(bg_path)
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2RGB)
    bg_h, bg_w, _ = bg.shape

    # 2. 비율 자동 맞추기 (원본→배경)
    scale, offset_x, offset_y = fit_to_background(orig_w, orig_h, bg_w, bg_h)

    # 3. 합성
    bg_copy = bg.copy()
    for c in line_crops:
        rgba_line = make_transparent_clean(c["image"])
        x_min, y_min, x_max, y_max = c["coords"]

        # 좌표 스케일 + 오프셋 적용
        x = int(x_min * scale) + offset_x
        y = int(y_min * scale) + offset_y

        bg_copy = overlay_image_alpha(bg_copy, rgba_line, x, y)

    return bg_copy


# 시각화 도구
def visualize_crops(crops: List[Dict[str, Any]], n: int = 5):
    plt.figure(figsize=(15, 6))
    for i, c in enumerate(crops[:n]):
        plt.subplot(1, n, i + 1)
        plt.imshow(cv2.cvtColor(c["image"], cv2.COLOR_BGR2RGB))
        plt.title(c["text"])
        plt.axis("off")
    plt.show()
