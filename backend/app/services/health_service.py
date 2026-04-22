from datetime import UTC, datetime

from fastapi import HTTPException, status

from app.services.store import store


URGENT_KEYWORDS = {"difficulty breathing", "seizure", "collapse", "blood", "cannot stand"}
WARNING_KEYWORDS = {"vomiting", "diarrhea", "limping", "lethargy", "not eating"}


class HealthService:
    def get_dashboard(self, user: dict) -> dict:
        pets = store.list_pets(user["id"])
        active_pet = None
        if user.get("active_pet_id"):
            active_pet = store.get_pet(user["active_pet_id"])
        if not active_pet and pets:
            active_pet = pets[0]

        if not active_pet:
            return {"active_pet": None, "planner": None, "timeline": [], "weight_logs": []}

        planner = self._build_daily_care_plan(active_pet)
        weight_logs = store.list_weight_logs(active_pet["id"])
        timeline = [
            {"label": "Profile created", "status": "Completed", "date": active_pet["created_at"][:10]},
            {"label": "Daily care plan", "status": "Ready", "date": datetime.now(UTC).date().isoformat()},
            {"label": "Breed knowledge indexed", "status": "Ready", "date": datetime.now(UTC).date().isoformat()},
        ]
        return {
            "active_pet": active_pet,
            "planner": planner,
            "timeline": timeline,
            "weight_logs": weight_logs,
        }

    def analyze_symptoms(self, user_id: int, pet_id: int, symptoms: str, duration: str) -> dict:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")

        normalized = symptoms.lower()
        severity = "low"
        if any(keyword in normalized for keyword in URGENT_KEYWORDS):
            severity = "urgent"
        elif any(keyword in normalized for keyword in WARNING_KEYWORDS):
            severity = "medium"

        recommendations = [
            "Track appetite, water intake, energy, and bathroom habits.",
            "Avoid introducing new food or intense exercise until symptoms settle.",
        ]
        if severity == "medium":
            recommendations.append("Arrange a same-day or next-day vet check if symptoms continue.")
        if severity == "urgent":
            recommendations = [
                "Seek urgent veterinary care now.",
                "Keep your pet warm, quiet, and transport-ready.",
            ]

        return {
            "severity": severity,
            "duration": duration,
            "possible_causes": pet["breed_profile"]["risk_tags"][:3],
            "recommendations": recommendations,
            "disclaimer": "This is informational only and not a diagnosis.",
        }

    def build_weight_overview(self, pet_id: int, user_id: int) -> dict:
        pet = store.get_pet(pet_id)
        if not pet or pet["owner_id"] != user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pet not found.")
        logs = store.list_weight_logs(pet_id)
        healthy_range = pet["breed_profile"].get("weight_range", "Varies")
        return {"pet_id": pet_id, "healthy_range": healthy_range, "logs": logs}

    @staticmethod
    def _build_daily_care_plan(pet: dict) -> dict:
        care_plan = pet["breed_profile"]["care_plan"]
        return {
            "food": care_plan["food"],
            "exercise": care_plan["exercise"],
            "water": care_plan["water"],
            "notes": f"Tailored for {pet['breed']} at {pet['age_years']} years and {pet['weight_kg']} kg.",
        }


health_service = HealthService()
