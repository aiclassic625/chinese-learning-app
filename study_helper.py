from openai import OpenAI

# DeepSeek 클라이언트
client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    try:
        # 텍스트가 비어있으면 오류 반환
        if not chinese_text or len(chinese_text.strip()) < 5:
            return "텍스트가 너무 짧습니다. 다시 시도해주세요."

        prompt = f"""
다음 중국어 텍스트를 분석해주세요:

{chinese_text}

각 문장을 번호로 나누고, 병음과 한국어 뜻을 추가해주세요.
단어 분석도 포함해주세요.
"""

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
