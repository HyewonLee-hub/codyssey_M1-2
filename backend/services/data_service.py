from backend.config.firebase import get_db


def create_data(data):
    db = get_db()

    # 날짜를 Document ID로 사용
    doc_id = data["date"]
    doc_ref = db.collection("data").document(doc_id)

    # 같은 날짜가 이미 있는지 확인
    if doc_ref.get().exists:
        return None

    doc_ref.set(data)

    return {
        "message": "데이터가 Firestore에 저장되었습니다.",
        "id": doc_id,
        "data": data
    }


def get_all_data():
    db = get_db()

    docs = (
        db.collection("data")
        .order_by("date")
        .stream()
    )

    data_list = []

    for doc in docs:
        data = doc.to_dict()

        data_list.append({
            "id": doc.id,
            **data
        })

    return data_list


def update_data(doc_id, data):
    db = get_db()

    doc_ref = db.collection("data").document(doc_id)
    doc = doc_ref.get()

    # 해당 문서가 없으면 수정 불가
    if not doc.exists:
        return None

    doc_ref.update(data)

    return {
        "message": "데이터가 수정되었습니다.",
        "id": doc_id,
        "data": {
            "date": doc_id,
            **data
        }
    }


def delete_data(doc_id):
    db = get_db()

    doc_ref = db.collection("data").document(doc_id)
    doc = doc_ref.get()

    # 해당 문서가 없으면 삭제 불가
    if not doc.exists:
        return False

    doc_ref.delete()

    return True


def get_data_summary():
    data_list = get_all_data()

    # 데이터가 없는 경우
    if not data_list:
        return None

    values = [item["value"] for item in data_list]

    # 기본 통계
    count = len(values)
    average = sum(values) / count

    max_item = max(
        data_list,
        key=lambda item: item["value"]
    )

    min_item = min(
        data_list,
        key=lambda item: item["value"]
    )

    # 최근 추세 계산
    trend = "데이터 부족"
    recent_average = None
    previous_average = None
    change_percent = None

    if count >= 14:
        recent_values = values[-7:]
        previous_values = values[-14:-7]

        recent_average = sum(recent_values) / len(recent_values)
        previous_average = sum(previous_values) / len(previous_values)

        if previous_average != 0:
            change_percent = (
                (recent_average - previous_average)
                / previous_average
                * 100
            )

            # 변화율 5%를 기준으로 추세 판단
            if change_percent > 5:
                trend = "증가"
            elif change_percent < -5:
                trend = "감소"
            else:
                trend = "유지"

    return {
        "period": {
            "start": data_list[0]["date"],
            "end": data_list[-1]["date"]
        },
        "count": count,
        "metrics": {
            "average": round(average, 2),
            "max": round(max_item["value"], 2),
            "max_date": max_item["date"],
            "min": round(min_item["value"], 2),
            "min_date": min_item["date"]
        },
        "recent": {
            "recent_7_days_average": (
                round(recent_average, 2)
                if recent_average is not None
                else None
            ),
            "previous_7_days_average": (
                round(previous_average, 2)
                if previous_average is not None
                else None
            ),
            "change_percent": (
                round(change_percent, 2)
                if change_percent is not None
                else None
            )
        },
        "trend": trend
    }