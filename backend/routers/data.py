from fastapi import APIRouter, HTTPException

from backend.schemas.data import DataCreate, DataUpdate
from backend.services.data_service import (
    create_data,
    get_all_data,
    get_data_summary,
    update_data,
    delete_data,
)


router = APIRouter(
    prefix="/api/data",
    tags=["data"]
)


@router.post("")
def add_data(data: DataCreate):
    result = create_data(data.model_dump())

    if result is None:
        raise HTTPException(
            status_code=409,
            detail="해당 날짜의 데이터가 이미 존재합니다."
        )

    return result


@router.get("")
def get_data():
    return get_all_data()

@router.get("/summary")
def get_summary():
    result = get_data_summary()

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="분석할 데이터가 없습니다."
        )

    return result


@router.put("/{id}")
def edit_data(id: str, data: DataUpdate):
    result = update_data(
        id,
        data.model_dump()
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="해당 데이터를 찾을 수 없습니다."
        )

    return result


@router.delete("/{id}")
def remove_data(id: str):
    success = delete_data(id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="해당 데이터를 찾을 수 없습니다."
        )

    return {
        "message": "데이터가 삭제되었습니다.",
        "id": id
    }