import streamlit as st
from PIL import Image
import os
from ocr import extract_text_from_image
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지 사진을 업로드하면 중국어 학습 자료를 만들어드려요!")

# ===== 🔥 추가된 부분 1: session_state 초기화 (새로고침해도 데이터 유지) =====
if "study_result" not in st.session_state:
    st.session_state.study_result = None

# ===== 파일 업로드만! (기존과 동일) =====
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
                # ===== 🔥 추가된 부분 2: 결과를 session_state에 저장 =====
                st.session_state.study_result = study_material
                st.markdown(study_material)
    
    if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")

if st.session_state.study_result:
    st.markdown("---")
    st.markdown(st.session_state.study_result)
    
    # 다운로드 버튼 추가
    st.download_button(
        label="📥 학습 자료 다운로드 (텍스트 파일)",
        data=st.session_state.study_result,
        file_name="chinese_study_material.txt",
        mime="text/plain",
        key="download_study"
    )
