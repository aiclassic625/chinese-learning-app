import streamlit as st
from PIL import Image
import os
import base64
from study_helper import generate_study_material

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지를 찍거나 갤러리에서 선택하면 중국어 학습 자료를 만들어드려요!")

# 탭 구성
tab1, tab2 = st.tabs(["📁 파일 업로드", "📸 카메라 촬영"])

uploaded_file = None

with tab1:
    uploaded_file = st.file_uploader("갤러리에서 사진을 선택하세요", type=["jpg", "jpeg", "png"])

with tab2:
    uploaded_file = st.camera_input("📸 책 페이지를 카메라로 찍어주세요")

if uploaded_file is not None:
    # 이미지 미리보기
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)
    
    if st.button("🚀 학습 자료 생성하기"):
        with st.spinner("DeepSeek이 이미지를 읽고 학습 자료를 생성하는 중... (최대 30초)"):
            # DeepSeek에게 이미지 직접 전달 (OCR 포함)
            try:
                # 이미지를 Base64로 인코딩
                bytes_data = uploaded_file.getvalue()
                base64_image = base64.b64encode(bytes_data).decode('utf-8')
                
                from openai import OpenAI
                client = OpenAI(
                    api_key="sk-9d2da94df409489c8cfd3673b509665b",
                    base_url="https://api.deepseek.com/v1"
                )
                
                response = client.chat.completions.create(
                    model="deepseek-v4-flash",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                },
                                {
                                    "type": "text",
                                    "text": """이 이미지에서 중국어 텍스트를 읽어서 다음 형식으로 학습 자료를 만들어주세요:

--- 
**📌 문장 1:** [원문 중국어 문장]  
**🔊 병음:** [병음]  
**🇰🇷 해석:** [한국어 뜻]  
**📖 단어 분석:**  
- [단어1]: [뜻] (병음: [병음], HSK 급수: [급수], 부수: [부수])  

---

모든 문장에 대해 위 형식을 반복해주세요."""
                                }
                            ]
                        }
                    ]
                )
                
                st.success("🎉 학습 자료 생성 완료!")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"오류 발생: {e}")
