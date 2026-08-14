import requests
import base64

def extract_text_from_image(image_path):
    try:
        api_key = "AIzaSyApHgEC3TuAxV3L-voiI_GYNqSeXq4Yexw"
        
        with open(image_path, "rb") as image_file:
            image_content = image_file.read()
        
        # ✅ base64 인코딩 (이 방식이 더 안전함)
        encoded_image = base64.b64encode(image_content).decode("utf-8")
        
        url = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"
        
        payload = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "TEXT_DETECTION"
                        }
                    ]
                }
            ]
        }
        
        response = requests.post(url, json=payload)
        result = response.json()
        
        # 🔍 디버깅을 위해 응답 전체를 출력 (오류 파악용)
        if "error" in result:
            return f"API 오류: {result['error']['message']}"
        
        if "responses" in result and result["responses"]:
            text_annotations = result["responses"][0].get("textAnnotations", [])
            if text_annotations:
                return text_annotations[0]["description"].strip()
        
        return "텍스트를 찾을 수 없습니다."
    
    except Exception as e:
        return f"OCR 오류: {e}"
