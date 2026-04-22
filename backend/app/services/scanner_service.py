import json
from pathlib import Path

from app.core.config import settings


class ScannerService:
    def __init__(self) -> None:
        self.path = Path(settings.toxic_ingredients_path)
        if self.path.exists():
            self.ingredients = json.loads(self.path.read_text(encoding="utf-8"))
        else:
            self.ingredients = []

    def scan(self, ingredients_text: str) -> dict:
        tokens = [part.strip().lower() for part in ingredients_text.replace("\n", ",").split(",") if part.strip()]
        findings = []
        for entry in self.ingredients:
            if entry["name"] in tokens or any(entry["name"] in token for token in tokens):
                findings.append(entry)
        return {
            "ingredients": tokens,
            "findings": findings,
            "safe": not any(item["severity"] == "high" for item in findings),
        }


scanner_service = ScannerService()
