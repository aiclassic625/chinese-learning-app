from openai import OpenAI

# DeepSeek 클라이언트 초기화
client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    """
    중국어 텍스트를 받아서 문장별로 학습 자료를 생성하는 함수
    """
    # UTF-8 인코딩 보정
    if isinstance(chinese_text, str):
        chinese_text = chinese_text.encode('utf-8', errors='ignore').decode('utf-8')

    prompt = f"""
다음은 중국어 텍스트입니다. 한국어 학습자를 위한 친절한 중국어 학습 자료를 만들어주세요.

[텍스트]
{chinese_text}

반드시 다음 형식으로 출력해주세요:

---

**📌 문장 1:** [원문 중국어 문장]  
**🔊 병음:** [병음]  
**🇰🇷 해석:** [한국어 뜻]  
**📖 단어 분석:**  
- [단어1]: [뜻] (병음: [병음], HSK 급수: [급수], 부수: [부수], 획수: [획수])  

---

... (모든 문장에 대해 위 형식을 반복)

형식은 깔끔하게 마크다운을 사용해주세요.
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "당신은 중국어 교육 전문가입니다. 항상 친절하고 자세하게 가르쳐주세요."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {e}"
