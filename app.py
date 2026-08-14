import streamlit as st
from PIL import Image
import os
from ocr import extract_text_from_image
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("갤러리에서 책 페이지 사진을 선택하면 중국어 학습 자료를 만들어드려요!")

# 파일 업로드
uploaded_file = st.file_uploader("갤러리에서 사진을 선택하세요", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 이미지 미리보기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("🚀 학습 자료 생성하기"):
        # 1. 임시 파일로 저장
        with open("temp_image.jpg", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # 2. OCR로 텍스트 추출
        with st.spinner("📖 이미지에서 텍스트를 추출하는 중..."):
            extracted_text = extract_text_from_image("temp_image.jpg")
        
        # 3. OCR 결과 확인
        if "오류" in extracted_text:
            st.error(f"OCR 오류: {extracted_text}")
        else:
            st.success("✅ 텍스트 추출 완료!")
            with st.expander("📝 추출된 텍스트 보기"):
                st.write(extracted_text)
            
            # 4. DeepSeek으로 학습 자료 생성
            with st.spinner("🧠 DeepSeek이 학습 자료를 생성하는 중..."):
                study_material = generate_study_material(extracted_text)
            
            if "오류" in study_material:
                st.error(f"학습 자료 생성 오류: {study_material}")
            else:
                st.success("🎉 학습 자료 생성 완료!")
                st.markdown(study_material)
        
        # 임시 파일 정리
        if os.path.exists("temp_image.jpg"):
            os.remove("temp_image.jpg")
