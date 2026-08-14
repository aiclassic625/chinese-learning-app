import streamlit as st
from PIL import Image
import os
from ocr import extract_text_from_image
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지 사진을 업로드하면 중국어 학습 자료를 만들어드려요!")

# --- 파일 업로드 ---
uploaded_file = st.file_uploader("책 페이지 사진을 선택하세요", type=["jpg", "jpeg", "png", "JPEG", "JPG", "PNG"])

if uploaded_file is not None:
    with open("temp_image.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("🚀 학습 자료 생성하기"):
        with st.spinner("📖 이미지에서 텍스트를 추출하는 중..."):
            extracted_text = extract_text_from_image("temp_image.jpg")
        
        if "오류" in extracted_text:
            st.error(f"OCR 오류: {extracted_text}")
        else:
            st.success("✅ 텍스트 추출 완료!")
            with st.expander("📝 추출된 텍스트 보기"):
                st.write(extracted_text)
            
            with st.spinner("🧠 DeepSeek이 학습 자료를 생성하는 중... (최대 30초)"):
                study_material = generate_study_material(extracted_text)
            
            if "오류" in study_material:
                st.error(f"학습 자료 생성 오류: {study_material}")
            else:
                st.success("🎉 학습 자료 생성 완료!")
                st.markdown(study_material)
    
    if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")

# --- 텍스트 직접 입력 (OCR이 어려울 때) ---
with st.expander("✍️ 텍스트 직접 입력 (OCR이 어려울 때)"):
    manual_text = st.text_area("중국어 텍스트를 직접 붙여넣으세요")
    if st.button("직접 입력한 텍스트로 학습 자료 생성"):
        if manual_text.strip():
            with st.spinner("🧠 DeepSeek이 학습 자료를 생성하는 중..."):
                study_material = generate_study_material(manual_text)
                st.markdown(study_material)
        else:
            st.warning("텍스트를 입력해주세요.")
