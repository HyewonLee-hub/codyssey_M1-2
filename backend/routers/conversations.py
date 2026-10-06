from fastapi import APIRouter, HTTPException

from backend.schemas.conversation import ConversationCreate
from backend.services.conversation_service import (
    create_conversation,
    get_all_conversations,
    get_conversation,
    delete_conversation,
)


router = APIRouter(
    prefix="/api/conversations",
    tags=["conversations"]
)


@router.post("")
def save_conversation(
    conversation: ConversationCreate
):
    return create_conversation(
        conversation.model_dump()
    )


@router.get("")
def get_conversations():
    return get_all_conversations()


@router.get("/{id}")
def get_conversation_by_id(id: str):
    result = get_conversation(id)

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="대화를 찾을 수 없습니다."
        )

    return result


@router.delete("/{id}")
def remove_conversation(id: str):
    success = delete_conversation(id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="대화를 찾을 수 없습니다."
        )

    return {
        "message": "대화가 삭제되었습니다.",
        "id": id
    }