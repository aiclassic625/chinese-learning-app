import streamlit as st
from PIL import Image
import os
from ocr import extract_text_from_image
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지를 찍거나 갤러리에서 선택하면 중국어 학습 자료를 만들어드려요!")

# --- 세션 상태 초기화 ---
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# --- 탭 구성 ---
tab1, tab2 = st.tabs(["📁 파일 업로드", "📸 카메라 촬영"])

with tab1:
    uploaded = st.file_uploader("갤러리에서 사진을 선택하세요", type=["jpg", "jpeg", "png", "JPEG", "JPG", "PNG"])
    if uploaded is not None:
        st.session_state.uploaded_file = uploaded

with tab2:
    uploaded = st.camera_input("📸 책 페이지를 카메라로 찍어주세요")
    if uploaded is not None:
        st.session_state.uploaded_file = uploaded

# --- 이미지 처리 (탭 밖에서 session_state로 접근) ---
if st.session_state.uploaded_file is not None:
    with open("temp_image.jpg", "wb") as f:
        f.write(st.session_state.uploaded_file.getbuffer())
    
    image = Image.open(st.session_state.uploaded_file)
    max_size = (800, 800)
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    image.save("temp_image.jpg", "JPEG", quality=85)


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
