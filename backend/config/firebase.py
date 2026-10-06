import json
import os
from pathlib import Path

import firebase_admin
from dotenv import load_dotenv
from firebase_admin import credentials, firestore


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


def get_db():
    try:
        firebase_admin.get_app()

    except ValueError:
        service_account_json = os.getenv(
            "FIREBASE_SERVICE_ACCOUNT_JSON"
        )

        service_account_path = os.getenv(
            "FIREBASE_SERVICE_ACCOUNT_PATH"
        )

        # 배포 환경: JSON 문자열 사용
        if service_account_json:
            service_account_info = json.loads(
                service_account_json
            )

            cred = credentials.Certificate(
                service_account_info
            )

        # 로컬 환경: JSON 파일 경로 사용
        elif service_account_path:
            credential_path = (
                BASE_DIR / service_account_path
            )

            cred = credentials.Certificate(
                str(credential_path)
            )

        else:
            raise RuntimeError(
                "Firebase 서비스 계정 정보가 없습니다."
            )

        firebase_admin.initialize_app(cred)

    return firestore.client()