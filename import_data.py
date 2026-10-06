import pandas as pd

from backend.config.firebase import get_db


CSV_PATH = "data/seoul_pm10_2025.csv"


def import_data():
    # 1. 전처리된 CSV 읽기
    df = pd.read_csv(CSV_PATH)

    print("불러온 데이터 개수:", len(df))

    # 2. Firestore 연결
    db = get_db()

    # 3. Batch 생성
    batch = db.batch()

    # 4. CSV의 각 행을 Firestore Document로 변환
    for _, row in df.iterrows():
        data = {
            "date": str(row["date"]),
            "value": float(row["value"]),
            "memo": str(row["memo"]),
        }

        # 날짜를 Document ID로 사용
        doc_ref = db.collection("data").document(data["date"])

        batch.set(doc_ref, data)

    # 5. Firestore에 한 번에 저장
    batch.commit()

    print("Firestore 데이터 적재 완료!")
    print("저장된 데이터 개수:", len(df))


if __name__ == "__main__":
    import_data()