from openai import OpenAI

# DeepSeek 클라이언트 초기화 (본인의 API 키로 교체)
client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    """
    중국어 텍스트를 학습 자료로 변환합니다.
    - 번체자 → 간체 변환 포함
    - HSK 4급 이상 단어만 한 글자씩 뜻 풀이
    - 부수/획수 제외
    """
    try:
        if not chinese_text or len(chinese_text.strip()) < 5:
            return "텍스트가 너무 짧습니다. (최소 5자 이상 필요)"

        prompt = f"""
중국어 텍스트를 학습 자료로 변환해주세요.

텍스트:
{chinese_text}

출력 형식 (반드시 아래와 같이 정확히 작성해주세요):

---

**📌 문장 1**
- **원문:** [중국어 문장]
- **병음:** [전체 병음]
- **해석:** [한국어 뜻]
- **📝 간체 변환:** (원문이 번체일 경우에만 추가)

- **HSK 4급 이상 단어 분석 (한 글자씩 뜻 풀이):**
  - [단어] (병음): 뜻
    - (한자 풀이) [첫째 글자]: [그 글자의 뜻] + [둘째 글자]: [그 글자의 뜻]

---

**📌 문장 2**
- **원문:** [중국어 문장]
- **병음:** [병음]
- **해석:** [한국어 뜻]

- **HSK 4급 이상 단어 분석:**
  - [단어] (병음): 뜻
    - (한자 풀이) [첫째 글자]: [뜻] + [둘째 글자]: [뜻]

---

- **간체 변환 항목은 원문이 번체(正體字/繁體字)일 때만 추가하세요. 원문이 간체(简体字)면 이 항목을 완전히 생략하세요.**
- HSK 4급 이상 단어만 추출하세요.
- **부수, 횟수(획수)는 절대 표시하지 마세요.**
- 각 단어의 한 글자씩 뜻 풀이만 제공하세요.
- 모든 문장에 대해 위 형식을 반복하세요.
- 표는 사용하지 마세요.
"""

        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "당신은 중국어 교육 전문가입니다. 항상 깔끔하고 읽기 쉽게 가르쳐주세요."},
                {"role": "user", "content": prompt}
            ],
            reasoning_effort="low"  # 속도 향상
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"오류 발생: {e}"
