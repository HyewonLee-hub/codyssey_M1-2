from datetime import datetime, timezone

from firebase_admin import firestore

from backend.config.firebase import get_db


def get_current_time():
    return datetime.now(timezone.utc)


def create_conversation(data):
    db = get_db()

    doc_ref = db.collection("conversations").document()

    now = get_current_time()

    conversation = {
        "title": data["title"],
        "messages": data["messages"],
        "created_at": now,
        "updated_at": now,
    }

    doc_ref.set(conversation)

    return {
        "id": doc_ref.id,
        **conversation
    }


def get_all_conversations():
    db = get_db()

    docs = (
        db.collection("conversations")
        .order_by(
            "updated_at",
            direction=firestore.Query.DESCENDING
        )
        .stream()
    )

    conversations = []

    for doc in docs:
        data = doc.to_dict()

        conversations.append({
            "id": doc.id,
            "title": data.get("title"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "message_count": len(
                data.get("messages", [])
            )
        })

    return conversations


def get_conversation(conversation_id):
    db = get_db()

    doc_ref = (
        db.collection("conversations")
        .document(conversation_id)
    )

    doc = doc_ref.get()

    if not doc.exists:
        return None

    return {
        "id": doc.id,
        **doc.to_dict()
    }


def append_messages(conversation_id, new_messages):
    db = get_db()

    doc_ref = (
        db.collection("conversations")
        .document(conversation_id)
    )

    doc = doc_ref.get()

    if not doc.exists:
        return None

    data = doc.to_dict()

    messages = data.get("messages", [])
    messages.extend(new_messages)

    doc_ref.update({
        "messages": messages,
        "updated_at": get_current_time()
    })

    return True


def delete_conversation(conversation_id):
    db = get_db()

    doc_ref = (
        db.collection("conversations")
        .document(conversation_id)
    )

    doc = doc_ref.get()

    if not doc.exists:
        return False

    doc_ref.delete()

    return True