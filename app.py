import streamlit as st
from PIL import Image
import os
from ocr import extract_text_from_image
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지 사진을 업로드하면 중국어 학습 자료를 만들어드려요!")

# --- 사이드바에 글자 크기 조절 추가 ---
font_size = st.sidebar.slider("📏 글자 크기", 12, 30, 18)

# --- 파일 업로드 ---
uploaded_file = st.file_uploader("갤러리에서 사진을 선택하세요", type=["jpg", "jpeg", "png", "JPG", "JPEG", "PNG"])

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
            
            with st.spinner("🧠 DeepSeek이 학습 자료를 생성하는 중..."):
                study_material = generate_study_material(extracted_text)
            
            if "오류" in study_material:
                st.error(f"학습 자료 생성 오류: {study_material}")
            else:
                st.success("🎉 학습 자료 생성 완료!")
                
                # 🔥 여기가 핵심! 글자 크기 조절 + 배경 추가
                st.markdown(f"""
                <div style="font-size: {font_size}px; line-height: 2.0; background-color: #f9f9f9; padding: 20px; border-radius: 10px;">
                {study_material}
                </div>
                """, unsafe_allow_html=True)
    
    if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")
