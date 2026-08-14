import easyocr
from PIL import Image
import numpy as np

# EasyOCR 리더 초기화 (중국어 간체 + 영어)
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)

def extract_text_from_image(image_path):
    """
    EasyOCR을 사용하여 이미지에서 중국어(간체) 텍스트를 추출합니다.
    """
    try:
        # 이미지 열기
        image = Image.open(image_path)
        # numpy 배열로 변환 (EasyOCR이 필요로 하는 형식)
        image_np = np.array(image)
        
        # EasyOCR 실행
        result = reader.readtext(image_np, detail=0, paragraph=False)
        
        # 결과를 하나의 텍스트로 합치기
        if not result:
            return "텍스트를 찾을 수 없습니다. (사진이 흐리거나 중국어가 없을 수 있어요)"
        
        text = '\n'.join(result)
        return text.strip()
    
    except Exception as e:
        return f"OCR 오류: {e}"
