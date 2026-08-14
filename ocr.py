import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

def extract_text_from_image(image_path):
    try:
        image = Image.open(image_path)
        
        # --- 전처리 (인식률 최대화) ---
        image = image.convert('L')  # 흑백
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.5)  # 대비 2.5배
        image = image.filter(ImageFilter.SHARPEN)  # 선명화
        image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)  # 2배 확대
        
        # --- Tesseract 실행 (중국어 간체만 집중!) ---
        custom_config = r'--oem 3 --psm 6 -l chi_sim'
        text = pytesseract.image_to_string(image, config=custom_config)
        
        if not text.strip():
            return "텍스트를 찾을 수 없습니다. (사진이 흐리거나 중국어가 없을 수 있어요)"
        return text.strip()
    except Exception as e:
        return f"OCR 오류: {e}"
