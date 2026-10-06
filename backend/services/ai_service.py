import os

from dotenv import load_dotenv
from openai import OpenAI

from backend.services.data_service import get_data_summary


load_dotenv()


def generate_ai_response(
    message: str,
    history: list | None = None
):
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL")

    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY 환경 변수가 없습니다."
        )

    if not base_url:
        raise RuntimeError(
            "OPENAI_BASE_URL 환경 변수가 없습니다."
        )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    # Firestore 데이터를 분석한 Summary 가져오기
    summary = get_data_summary()

    if summary is None:
        raise RuntimeError(
            "분석할 데이터가 없습니다."
        )

    # Summary를 시스템 프롬프트에 주입
    system_prompt = f"""
당신은 서울 미세먼지 데이터를 분석하는 AI 비서입니다.

[서울 PM10 데이터 요약]

데이터 기간:
{summary["period"]["start"]} ~ {summary["period"]["end"]}

총 데이터 개수:
{summary["count"]}개

전체 평균 PM10:
{summary["metrics"]["average"]} ㎍/㎥

최대 PM10:
{summary["metrics"]["max"]} ㎍/㎥
날짜:
{summary["metrics"]["max_date"]}

최소 PM10:
{summary["metrics"]["min"]} ㎍/㎥
날짜:
{summary["metrics"]["min_date"]}

최근 7일 평균:
{summary["recent"]["recent_7_days_average"]} ㎍/㎥

직전 7일 평균:
{summary["recent"]["previous_7_days_average"]} ㎍/㎥

최근 변화율:
{summary["recent"]["change_percent"]}%

최근 추세:
{summary["trend"]}

반드시 위 데이터에 근거해서 답변하세요.
데이터에서 확인할 수 없는 내용은 추측하지 말고,
현재 제공된 데이터만으로는 알 수 없다고 답변하세요.
답변은 이해하기 쉬운 한국어로 작성하세요.
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": message
    })


    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
        max_completion_tokens=1000
    )

    return {
        "answer": response.choices[0].message.content
    }