import os
from google.cloud import vision
import io

def extract_text_from_image(image_path):
    try:
        # 🔥 여기에 방금 복사한 API 키를 넣으세요!
        API_KEY = "AIzaSyApHgEC3TuAxV3L-voiI_GYNqSeXq4Yexw"
        
        client = vision.ImageAnnotatorClient(
            client_options={"api_key": API_KEY}
        )

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = client.document_text_detection(image=image)
        if response.full_text_annotation:
            text = response.full_text_annotation.text
            if not text.strip():
                return "텍스트를 찾을 수 없습니다. (사진이 흐리거나 중국어가 없을 수 있어요)"
            return text.strip()
        else:
            return "텍스트를 찾을 수 없습니다."
    except Exception as e:
        return f"OCR 오류: {e}"
