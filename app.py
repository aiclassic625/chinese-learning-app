import streamlit as st
from PIL import Image
import os
import datetime
from ocr import extract_text_from_image
from study_helper import generate_study_material
from supabase import create_client, Client

# ===== Supabase 연결 설정 =====
supabase_url = st.secrets["SUPABASE_URL"]
supabase_key = st.secrets["SUPABASE_ANON_KEY"]
supabase: Client = create_client(supabase_url, supabase_key)

st.set_page_config(page_title="찰칵 중국어", page_icon="📚")
st.title("📸 찰칵 중국어")
st.write("책 페이지 사진을 업로드하면 중국어 학습 자료를 만들어드려요!")

# ===== session_state 초기화 =====
if "study_result" not in st.session_state:
    st.session_state.study_result = None
if "user" not in st.session_state:
    st.session_state.user = None
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ===== 로그인/회원가입 UI (사이드바) =====
def login_signup():
    st.sidebar.title("🔐 로그인 / 회원가입")
    email = st.sidebar.text_input("이메일")
    password = st.sidebar.text_input("비밀번호", type="password")
    mode = st.sidebar.radio("선택", ["로그인", "회원가입"])

    if st.sidebar.button("확인"):
        try:
            if mode == "회원가입":
                response = supabase.auth.sign_up({"email": email, "password": password})
                st.sidebar.success("✅ 회원가입 완료! 이메일로 발송된 인증 링크를 클릭한 후 로그인해주세요.")
            else:
                response = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = response.user
                st.session_state.logged_in = True
                st.sidebar.success(f"✅ {email} 님 환영합니다!")
        except Exception as e:
            st.sidebar.error(f"오류: {e}")

# ===== 로그인 상태 확인 =====
if st.session_state.logged_in:
    st.sidebar.write(f"👋 {st.session_state.user.email}")

    # 디버깅용 ID 표시
    # st.write(f"ID: {st.session_state.user.id}")  # 주석 처리
    
    # ===== 내 학습 기록 보기 =====
    st.sidebar.subheader("📚 내 학습 기록")
    if st.sidebar.button("📖 저장된 자료 보기"):
        try:
            response = supabase.table("study_records")\
                .select("*")\
                .eq("user_id", st.session_state.user.id)\
                .order("created_at", desc=True)\
                .execute()
            
            records = response.data
            if not records:
                st.info("📭 아직 저장된 학습 자료가 없어요.")
            else:
                for idx, record in enumerate(records, 1):
                    with st.expander(f"📄 {idx}. {record['created_at'][:16]} - {record['original_text'][:30]}..."):
                        st.markdown(record['study_material'])
                        st.caption(f"📅 저장일: {record['created_at']}")
        except Exception as e:
            st.error(f"❌ 저장 불러오기 실패! 이유: {e}")
            st.write(f"디버깅: user_id = {st.session_state.user.id}, 타입 = {type(st.session_state.user.id)}")
    
    if st.sidebar.button("로그아웃"):
        st.session_state.user = None
        st.session_state.logged_in = False
else:
    login_signup()
    st.stop()

# ===== 파일 업로드 =====
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
                st.session_state.study_result = study_material
                st.markdown(study_material)

                # ===== Supabase에 저장 =====
                st.write("🔍 저장 시도 중...")
                
                try:
                    data = {
                        "user_id": st.session_state.user.id,
                        "original_text": extracted_text,
                        "study_material": study_material,
                        "created_at": datetime.datetime.now().isoformat()
                    }
                    supabase.table("study_records").insert(data).execute()
                    st.info("💾 학습 자료가 클라우드에 저장되었습니다!")
                except Exception as e:
                    st.error(f"❌ 저장 실패! 이유: {e}")
                    st.write(f"디버깅: user_id = {st.session_state.user.id}, 타입 = {type(st.session_state.user.id)}")
    
    if os.path.exists("temp_image.jpg"):
        os.remove("temp_image.jpg")

# ===== 저장된 결과 표시 및 다운로드 버튼 =====
if st.session_state.study_result:
    st.markdown("---")
    st.markdown(st.session_state.study_result)
    
    st.download_button(
        label="📥 학습 자료 다운로드 (텍스트 파일)",
        data=st.session_state.study_result,
        file_name="chinese_study_material.txt",
        mime="text/plain",
        key="download_study"
    )
