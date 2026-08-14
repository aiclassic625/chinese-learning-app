import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def extract_text_from_image(image_path):
    """
    이미지에서 중국어(간체) 텍스트를 추출합니다.
    - 이미지 전처리(회색조, 대비 강화, 샤프닝)로 인식률을 높였습니다.
    """
    try:
        # 1. 이미지 열기
        image = Image.open(image_path)
        
        # 2. 이미지 전처리 (인식률 향상의 핵심!)
        # 2-1. 흑백(그레이스케일) 변환
        image = image.convert('L')
        
        # 2-2. 대비 2배 강화
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)
        
        # 2-3. 샤프닝(선명도) 적용
        image = image.filter(ImageFilter.SHARPEN)
        
        # 2-4. 크기 2배 확대 (작은 글씨 인식률 향상)
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
        
        # 3. Tesseract 실행 (중국어 간체 + 영어 동시 인식)
        #    --psm 6: 페이지에 하나의 텍스트 블록이 있다고 가정 (책 페이지에 최적)
        custom_config = r'--oem 3 --psm 6 -l chi_sim'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        # 4. 결과 정리
        if not text.strip():
            return "텍스트를 찾을 수 없습니다. (사진이 흐리거나 중국어가 없을 수 있어요)"
        
        return text.strip()
    
    except Exception as e:
        return f"OCR 오류: {e}"
