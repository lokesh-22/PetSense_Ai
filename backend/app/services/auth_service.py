from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from app.services.store import store


class AuthService:
    def register(self, email: str, password: str, full_name: str) -> dict:
        if store.get_user_by_email(email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered.")

        user = store.create_user(
            {
                "email": email.lower(),
                "password_hash": hash_password(password),
                "full_name": full_name,
                "created_at": datetime.now(UTC).isoformat(),
            }
        )
        return self._build_auth_payload(user)

    def login(self, email: str, password: str) -> dict:
        user = store.get_user_by_email(email.lower())
        if not user or not verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
        return self._build_auth_payload(user)

    def refresh(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token, expected_type="refresh")
        user = store.get_user_by_id(int(payload["sub"]))
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
        return self._build_auth_payload(user)

    @staticmethod
    def _build_auth_payload(user: dict) -> dict:
        return {
            "access_token": create_access_token(user["id"]),
            "refresh_token": create_refresh_token(user["id"]),
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "active_pet_id": user["active_pet_id"],
            },
        }


auth_service = AuthService()
