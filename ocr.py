import requests
from PIL import Image
import io

def extract_text_from_image(image_path):
    try:
        # 사용자의 API 키를 여기에 넣으세요
        api_key = "AIzaSyApHgEC3TuAxV3L-voiI_GYNqSeXq4Yexw"
        
        # 이미지를 base64로 인코딩
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()
        
        # Vision API 요청 URL
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        
        # 요청 바디 구성
        payload = {
            "requests": [
                {
                    "image": {
                        "content": image_content.decode("latin-1")
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }
        
        # API 호출
        response = requests.post(url, json=payload)
        result = response.json()
        
        # 텍스트 추출
        if "responses" in result and result["responses"]:
            text_annotations = result["responses"][0].get("textAnnotations", [])
            if text_annotations:
                return text_annotations[0]["description"].strip()
        
        return "텍스트를 찾을 수 없습니다."
    
    except Exception as e:
        return f"OCR 오류: {e}"
