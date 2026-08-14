from openai import OpenAI
import streamlit as st

# 🔥 API 키를 secrets에서 안전하게 불러옵니다!
client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    """
    중국어 텍스트를 받아서 문장별로 학습 자료를 생성하는 함수
    """
    if not chinese_text or len(chinese_text.strip()) < 5:
        return "텍스트가 너무 짧습니다. 다시 시도해주세요."

    prompt = f"""
다음 중국어 텍스트를 분석해주세요:

{chinese_text}

각 문장을 번호로 나누고, 병음과 한국어 뜻을 추가해주세요.
단어 분석도 포함해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "You are a Chinese language tutor."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류: {e}"
