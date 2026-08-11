# ocr.py - Tesseract 버전 (가볍고 빠름)
import pytesseract
from PIL import Image

def extract_text_from_image(image_path):
    """
    이미지에서 중국어(간체) 텍스트를 추출합니다.
    """
    try:
        image = Image.open(image_path)
        # 이미지 품질 개선 (선택사항)
        image = image.resize((image.width * 2, image.height * 2))
        # 중국어 간체 인식 (필요시 'chi_sim+eng'로 변경)
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        if not text.strip():
            return "텍스트를 찾을 수 없습니다. (사진이 흐리거나 중국어가 없을 수 있어요)"
        return text.strip()
    except Exception as e:
        return f"OCR 오류: {e}"

if __name__ == "__main__":
    test_image_path = "test.jpg"  # 테스트용 이미지 경로
    print(extract_text_from_image(test_image_path))