from openai import OpenAI

client = OpenAI(
    api_key="여기에_여러분의_DeepSeek_API_키를_넣으세요",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    """
    중국어 텍스트를 받아서 문장별로 학습 자료를 생성하는 함수
    - 번체자가 포함된 문장만 간체 변환 줄을 추가로 표시
    - 이미 간체인 문장은 변환 줄 생략
    """
    prompt = f"""
다음은 중국어 텍스트입니다. (번체자와 간체자가 혼용되어 있어도 됩니다)

[텍스트]
{chinese_text}

아래 형식으로 **모든 문장을** 번호를 붙여서 출력해주세요.

**중요 지침:**
- **✍️ 간체 변환:** 줄은 해당 문장에 **번체자가 포함되어 있을 때만** 출력하세요.
- 이미 간체자로만 구성된 문장이라면 **이 줄을 완전히 생략**하세요.

---

**📌 문장 [번호]:**

**🔤 원문:** [원문 그대로 출력]
**✍️ 간체 변환:** [해당 문장에 번체자가 있을 경우에만 출력]
**🔊 병음:** [병음]
**🇰🇷 해석:** [한국어 뜻]
**📖 단어 분석:**  
- [단어1]: [뜻] (병음: [병음], HSK 급수: [급수], 부수: [부수], 획수: [획수])  
- [단어2]: [뜻] (병음: [병음], HSK 급수: [급수], 부수: [부수], 획수: [획수])  

---

... (모든 문장에 대해 위 형식을 반복)

형식은 깔끔하게 마크다운을 사용해주세요.
"""
    try:
        response = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[
                {"role": "system", "content": "당신은 중국어 교육 전문가입니다. 번체자와 간체자에 모두 능숙하며, 한국어 학습자를 위해 친절하고 자세하게 가르쳐줍니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"오류 발생: {e}"
