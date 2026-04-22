import json
from contextlib import contextmanager

import psycopg
from psycopg.rows import dict_row

from app.core.config import settings


class AppStore:
    def __init__(self) -> None:
        self.database_url = settings.database_url
        self._initialized = False

    @contextmanager
    def connection(self):
        conn = psycopg.connect(self.database_url, row_factory=dict_row)
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def _ensure_tables(self) -> None:
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id BIGSERIAL PRIMARY KEY,
                        email TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        full_name TEXT NOT NULL,
                        active_pet_id BIGINT NULL,
                        created_at TEXT NOT NULL
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS pets (
                        id BIGSERIAL PRIMARY KEY,
                        owner_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        name TEXT NOT NULL,
                        species TEXT NOT NULL,
                        breed TEXT NOT NULL,
                        age_years DOUBLE PRECISION NOT NULL,
                        weight_kg DOUBLE PRECISION NOT NULL,
                        notes TEXT NOT NULL DEFAULT '',
                        breed_profile_json JSONB NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS chat_messages (
                        id BIGSERIAL PRIMARY KEY,
                        user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                        pet_id BIGINT NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
                        role TEXT NOT NULL,
                        content TEXT NOT NULL,
                        sources_json JSONB NOT NULL,
                        created_at TEXT NOT NULL
                    );
                    """
                )
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS weight_logs (
                        id BIGSERIAL PRIMARY KEY,
                        pet_id BIGINT NOT NULL REFERENCES pets(id) ON DELETE CASCADE,
                        weight_kg DOUBLE PRECISION NOT NULL,
                        logged_at TEXT NOT NULL
                    );
                    """
                )
        self._initialized = True

    def ensure_initialized(self) -> None:
        if not self._initialized:
            self._ensure_tables()

    def get_user_by_email(self, email: str):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                row = cursor.fetchone()
        return dict(row) if row else None

    def get_user_by_id(self, user_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
                row = cursor.fetchone()
        return dict(row) if row else None

    def create_user(self, payload: dict):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO users (email, password_hash, full_name, created_at)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        payload["email"],
                        payload["password_hash"],
                        payload["full_name"],
                        payload["created_at"],
                    ),
                )
                user_id = cursor.fetchone()["id"]
        return self.get_user_by_id(user_id)

    def update_user_active_pet(self, user_id: int, pet_id: int | None):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("UPDATE users SET active_pet_id = %s WHERE id = %s", (pet_id, user_id))
        return self.get_user_by_id(user_id)

    def create_pet(self, payload: dict):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO pets (
                        owner_id, name, species, breed, age_years, weight_kg,
                        notes, breed_profile_json, created_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s::jsonb, %s)
                    RETURNING id
                    """,
                    (
                        payload["owner_id"],
                        payload["name"],
                        payload["species"],
                        payload["breed"],
                        payload["age_years"],
                        payload["weight_kg"],
                        payload.get("notes", ""),
                        json.dumps(payload["breed_profile"]),
                        payload["created_at"],
                    ),
                )
                pet_id = cursor.fetchone()["id"]
        return self.get_pet(pet_id)

    def update_pet(self, pet_id: int, owner_id: int, payload: dict):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE pets
                    SET name = %s, species = %s, breed = %s, age_years = %s,
                        weight_kg = %s, notes = %s, breed_profile_json = %s::jsonb
                    WHERE id = %s AND owner_id = %s
                    """,
                    (
                        payload["name"],
                        payload["species"],
                        payload["breed"],
                        payload["age_years"],
                        payload["weight_kg"],
                        payload.get("notes", ""),
                        json.dumps(payload["breed_profile"]),
                        pet_id,
                        owner_id,
                    ),
                )
        return self.get_pet(pet_id)

    def delete_pet(self, pet_id: int, owner_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM pets WHERE id = %s AND owner_id = %s", (pet_id, owner_id))

    def get_pet(self, pet_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pets WHERE id = %s", (pet_id,))
                row = cursor.fetchone()
        return self._serialize_pet(row) if row else None

    def list_pets(self, owner_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM pets WHERE owner_id = %s ORDER BY created_at ASC", (owner_id,))
                rows = cursor.fetchall()
        return [self._serialize_pet(row) for row in rows]

    def add_chat_message(self, payload: dict):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO chat_messages (user_id, pet_id, role, content, sources_json, created_at)
                    VALUES (%s, %s, %s, %s, %s::jsonb, %s)
                    """,
                    (
                        payload["user_id"],
                        payload["pet_id"],
                        payload["role"],
                        payload["content"],
                        json.dumps(payload.get("sources", [])),
                        payload["created_at"],
                    ),
                )

    def list_chat_messages(self, pet_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM chat_messages WHERE pet_id = %s ORDER BY id ASC", (pet_id,))
                rows = cursor.fetchall()
        return [
            {
                "id": row["id"],
                "role": row["role"],
                "content": row["content"],
                "sources": row["sources_json"],
                "created_at": row["created_at"],
            }
            for row in rows
        ]

    def add_weight_log(self, pet_id: int, weight_kg: float, logged_at: str):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO weight_logs (pet_id, weight_kg, logged_at) VALUES (%s, %s, %s)",
                    (pet_id, weight_kg, logged_at),
                )

    def list_weight_logs(self, pet_id: int):
        self.ensure_initialized()
        with self.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT * FROM weight_logs WHERE pet_id = %s ORDER BY logged_at ASC",
                    (pet_id,),
                )
                rows = cursor.fetchall()
        return [dict(row) for row in rows]

    @staticmethod
    def _serialize_pet(row):
        data = dict(row)
        data["breed_profile"] = data.pop("breed_profile_json")
        return data


store = AppStore()
