from openai import OpenAI

client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    try:
        if not chinese_text or len(chinese_text.strip()) < 5:
            return "텍스트가 너무 짧습니다."

        prompt = f"""
다음은 중국어 텍스트입니다. 한국어 학습자를 위한 **깔끔한 텍스트 형식**의 학습 자료를 만들어주세요.

[텍스트]
{chinese_text}

반드시 아래 형식으로 출력해주세요:

---

1. 중국어 원문: [원문 문장]
2. 병음 (Pinyin): [병음]
3. 한국어 번역: [번역]
4. HSK 4급 이상 단어/표현 상세 분석 (글자 단위 해부):
   - [단어1] (병음): HSK 급수. 품사. 뜻.
     - (한자 분석) [글자1] (뜻) + [글자2] (뜻)
   - [단어2] (병음): HSK 급수. 품사. 뜻.

---

... (모든 문장에 대해 위 형식을 반복)

**주의: 절대 표를 만들지 마세요. 항상 깔끔한 텍스트 목록 형식으로 출력해주세요.**
"""

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "당신은 중국어 교육 전문가입니다. 깔끔하고 간결하게 가르쳐주세요."},
                {"role": "user", "content": prompt}
            ],
            reasoning_effort="low"  # 🚀 응답 속도 향상
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {e}"
