# study_helper.py
from openai import OpenAI

# DeepSeek 클라이언트 초기화 (여러분의 API 키를 입력하세요)
client = OpenAI(
    api_key="sk-9d2da94df409489c8cfd3673b509665b",
    base_url="https://api.deepseek.com/v1"
)

def generate_study_material(chinese_text):
    """
    중국어 텍스트를 받아서 학습 자료를 생성하는 함수
    """
    # DeepSeek에게 보낼 프롬프트를 작성합니다
    prompt = f"""
    다음은 중국어 텍스트입니다. 이 텍스트를 학습 자료로 가공해주세요.

    [텍스트]
    {chinese_text}

    다음 형식으로 출력해주세요:
    1. 각 문장을 번호와 함께 나열하고, 각 문장 아래에 한국어 뜻과 병음을 적어주세요.
    2. HSK 4급 이상의 단어를 추출하여 리스트로 보여주세요.
    3. 추출된 각 단어에 대해 한 글자씩 분석(예: 부수, 획수, 의미 등)을 추가해주세요.

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

# 테스트를 위한 코드
if __name__ == "__main__":
    test_text = "你好，今天天气真好！"
    print(generate_study_material(test_text))