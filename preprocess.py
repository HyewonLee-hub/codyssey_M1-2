from pathlib import Path

import pandas as pd


# 원본 파일과 결과 파일 경로
INPUT_PATH = Path("data") / "일별_평균_대기오염도정보_2025.csv"
OUTPUT_PATH = Path("data") / "seoul_pm10_2025.csv"


# 서울 25개 자치구
DISTRICTS = [
    "강남구", "강동구", "강북구", "강서구", "관악구",
    "광진구", "구로구", "금천구", "노원구", "도봉구",
    "동대문구", "동작구", "마포구", "서대문구", "서초구",
    "성동구", "성북구", "송파구", "양천구", "영등포구",
    "용산구", "은평구", "종로구", "중구", "중랑구"
]


# 1. CSV 파일 읽기
# CSV → pandas DataFrame으로 읽어오는 거
# DataFrame은 쉽게 말해 Python 안에서 다룰 수 있는 엑셀 표 같은 자료구조
df = pd.read_csv(INPUT_PATH, encoding="cp949")

print("원본 데이터 크기:", df.shape)


# 2. 25개 자치구 데이터만 선택
# 원본 데이터에 있는 50개 측정소 중에서 우리가 지정한 25개 자치구만 필터링하는 코드
df = df[df["측정소명"].isin(DISTRICTS)].copy()

print("자치구 필터링 후 데이터 크기:", df.shape)


# 3. 날짜 형식 변환
df["측정일시"] = pd.to_datetime(
    df["측정일시"].astype(str),
    format="%Y%m%d"
)


# 4. PM10 값을 숫자로 변환
df["미세먼지농도(㎍/㎥)"] = pd.to_numeric(
    df["미세먼지농도(㎍/㎥)"],
    # 숫자로 변환할 수 없는 값이 있으면 프로그램을 바로 터뜨리는 대신 NaN, 즉 결측값으로 바꾸라는 의미
    errors="coerce"
)


# 5. 날짜별 PM10 평균 계산
# aggregation
daily_pm10 = (
    df.groupby("측정일시", as_index=False)
    ["미세먼지농도(㎍/㎥)"]
    .mean()
)


# 6. 과제에서 사용할 형태로 변경
daily_pm10 = daily_pm10.rename(
    columns={
        "측정일시": "date",
        "미세먼지농도(㎍/㎥)": "value"
    }
)

daily_pm10["value"] = daily_pm10["value"].round(2)
daily_pm10["date"] = daily_pm10["date"].dt.strftime("%Y-%m-%d")

daily_pm10["memo"] = "서울 25개 자치구 PM10 일평균"


# 7. 결과 CSV 저장
daily_pm10.to_csv(
    OUTPUT_PATH,
    index=False,
    encoding="utf-8-sig"
)


# 8. 결과 확인
print("\n전처리 완료!")
print("결과 데이터 개수:", len(daily_pm10))
print("\n앞 5개 데이터:")
print(daily_pm10.head())

print("\n결측치 개수:")
print(daily_pm10.isnull().sum())

print(f"\n저장 위치: {OUTPUT_PATH}")