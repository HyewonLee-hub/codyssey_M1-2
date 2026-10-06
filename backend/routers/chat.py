from fastapi import APIRouter, HTTPException

from backend.schemas.chat import ChatRequest
from backend.services.ai_service import generate_ai_response
from backend.services.conversation_service import (
    append_messages,
    create_conversation,
    get_conversation,
)


router = APIRouter(
    prefix="/api/chat",
    tags=["chat"]
)


@router.post("")
def chat(request: ChatRequest):

    history = []

    # 기존 대화 이어가기
    if request.conversation_id:
        conversation = get_conversation(
            request.conversation_id
        )

        if conversation is None:
            raise HTTPException(
                status_code=404,
                detail="대화를 찾을 수 없습니다."
            )

        history = conversation.get(
            "messages",
            []
        )

    try:
        ai_result = generate_ai_response(
            request.message,
            history
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    answer = ai_result["answer"]

    new_messages = [
        {
            "role": "user",
            "content": request.message
        },
        {
            "role": "assistant",
            "content": answer
        }
    ]

    # 기존 대화면 이어서 저장
    if request.conversation_id:

        append_messages(
            request.conversation_id,
            new_messages
        )

        conversation_id = (
            request.conversation_id
        )

    # 새로운 대화면 새 Document 생성
    else:

        title = request.message.strip()

        if len(title) > 30:
            title = title[:30] + "..."

        conversation = create_conversation({
            "title": title,
            "messages": new_messages
        })

        conversation_id = conversation["id"]

    return {
        "conversation_id": conversation_id,
        "answer": answer
    }