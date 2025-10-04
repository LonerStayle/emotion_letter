# --- 필요한 라이브러리들을 가져옵니다 ---
import os
import collections
import datetime
import requests
import base64 # b64_json 데이터를 디코딩하기 위해 필요합니다.

from dotenv import load_dotenv
from openai import OpenAI
import cv2
import numpy as np

# --- 필터 설정 값 ---
BRIGHTNESS_ADJUSTMENT = 30
BLUR_KERNEL_SIZE = 15

# --- 함수 정의 ---

def create_image_prompt(heart_rate, text, gender='male'):
    """
    심박수와 텍스트를 분석하여 이미지 생성 프롬프트를 만듭니다. (이전과 동일)
    """
    if heart_rate < 70:
        style_keywords = "serene, tranquil, calm mood, soft and muted color palette"
    elif 70 <= heart_rate <= 90:
        style_keywords = "heartfelt, warm, nostalgic, golden hour lighting, painterly"
    else:
        style_keywords = "dynamic, vibrant, energetic, bold and contrasting colors"

    keyword_map = { 'Nature': ['공원', '나무', '숲', '꽃', '바다', '하늘', '별', '바람', '햇살', '비', '산'], 'Achievement': ['합격', '성공', '미래', '꿈', '도전', '목표', '시작', '승리'], 'Friendship': ['친구', '우정', '추억', '우리', '함께', '그리움', '따뜻', '대화'], 'Romance': ['사랑', '연인', '커플', '심장', '데이트', '설렘', '마음', '고백'], 'Creativity': ['책', '음악', '그림', '글', '코드', '아이디어', '창조', '작업', '편지'], }
    theme_counts = collections.Counter()
    for theme, words in keyword_map.items():
        theme_counts[theme] += sum(word in text for word in words)
    main_theme = theme_counts.most_common(1)[0][0] if theme_counts else "feelings"
    return (f"An atmospheric and symbolic visual representation of '{main_theme}'. " f"The scene should be abstract and metaphorical. Avoid any letters or text. " f"The artistic style must be: {style_keywords}. " f"Rendered as a hyper-detailed, photorealistic digital painting.")


def generate_image_data(client, prompt):
    """
    OpenAI API를 호출하여 이미지를 생성하고, 그 결과 데이터를 반환합니다.
    URL 또는 b64_json 응답 형식에 모두 대응하도록 수정되었습니다.

    Args:
        client (OpenAI): OpenAI API와 통신하기 위한 클라이언트 객체.
        prompt (str): 이미지 생성을 위한 텍스트 프롬프트.

    Returns:
        bytes: 성공 시 이미지 데이터. 실패 시 None.
    """
    try:
        print("이미지 생성을 요청합니다...")
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1536",
            quality="auto",
            n=1
        )

        image_data = None
        # 1. 먼저 URL이 있는지 확인합니다.
        if response.data[0].url:
            image_url = response.data[0].url
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            image_data = image_response.content
        # 2. URL이 없다면, b64_json 데이터가 있는지 확인합니다.
        elif response.data[0].b64_json:
            image_base64 = response.data[0].b64_json
            image_data = base64.b64decode(image_base64)
        else:
            # 두 가지 형식 모두 데이터가 없는 경우
            print("API 응답에서 이미지 데이터(URL 또는 b64_json)를 찾을 수 없습니다.")
            return None

        print("이미지 데이터 확보 성공.")
        return image_data
        
    except Exception as e:
        print(f"이미지 생성 중 오류 발생: {e}")
        return None


def apply_filters(image_data, brightness, blur_size):
    """
    이미지 데이터에 밝기 및 블러 필터를 순서대로 적용합니다.
    """
    np_array = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    bright_image = cv2.convertScaleAbs(image, alpha=1.0, beta=brightness)
    if blur_size % 2 == 0:
        blur_size += 1
    blurred_image = cv2.GaussianBlur(bright_image, (blur_size, blur_size), 0)
    return blurred_image


# --- 프로그램 실행 부분 ---

load_dotenv()
client = OpenAI()

heart_rate_input = 75
text_input = "이 편지를 쓰는 지금도 내 마음이 떨려. 너를 처음 만났을 때의 설렘, 너와 함께 걷는 길, 나누는 대화, 그 모든 순간을 사랑해."
gender_input = 'female'

final_prompt = create_image_prompt(heart_rate_input, text_input, gender_input)
print(f"생성된 프롬프트: {final_prompt}")

generated_image_bytes = generate_image_data(client, final_prompt)

if generated_image_bytes:
    filtered_image = apply_filters(generated_image_bytes, BRIGHTNESS_ADJUSTMENT, BLUR_KERNEL_SIZE)
    output_dir = "C:/emotion_letter/app/backend/services/letter_image"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"image_{timestamp}.png"
    output_path = os.path.join(output_dir, filename)
    cv2.imwrite(output_path, filtered_image)
    print(f"필터가 적용된 이미지가 '{output_path}' 경로에 저장되었습니다.")
else:
    print("프로세스를 중단합니다.")