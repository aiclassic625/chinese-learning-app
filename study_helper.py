from openai import OpenAI

client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    try:
        if not chinese_text or len(chinese_text.strip()) < 5:
            return "텍스트가 너무 짧습니다. (최소 5자 이상 필요)"

        prompt = f"""
당신은 중국어 교육 전문가입니다. 다음 중국어 텍스트를 한국어 학습자를 위한 **깔끔한 학습 자료**로 변환해주세요.

[텍스트]
{chinese_text}

⚠️ 반드시 아래 형식을 **정확히** 지켜주세요. 표를 만들지 마세요. 각 문장은 반드시 빈 줄로 분리해주세요.

---

**📌 문장 1**
- **원문:** [중국어 문장]
- **병음:** [병음]
- **해석:** [한국어 뜻]
- **단어 분석:**
  - [단어1] (병음): 뜻 (HSK 급수, 부수, 획수)
  - [단어2] (병음): 뜻 (HSK 급수, 부수, 획수)

**📌 문장 2**
- **원문:** [중국어 문장]
- **병음:** [병음]
- **해석:** [한국어 뜻]
- **단어 분석:**
  - [단어1] (병음): 뜻 (HSK 급수, 부수, 획수)
  - [단어2] (병음): 뜻 (HSK 급수, 부수, 획수)

---

❗ **중요:**
- 모든 문장에 대해 위 형식을 반복하세요.
- 문장과 문장 사이에는 반드시 **빈 줄**을 넣어서 시각적으로 분리하세요.
- 절대 표(테이블)를 사용하지 마세요.
- 깔끔한 텍스트 목록 형식으로 출력하세요.
"""

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "당신은 중국어 교육 전문가입니다. 항상 깔끔하고 읽기 쉽게 가르쳐주세요."},
                {"role": "user", "content": prompt}
            ],
            reasoning_effort="low"  # 응답 속도 향상
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {e}"
