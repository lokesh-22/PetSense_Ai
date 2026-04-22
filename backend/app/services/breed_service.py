from app.data.breed_catalog import BREED_CATALOG, UNIVERSAL_ARTICLES
from app.services.cache_service import cache_service
from app.utils.text import slugify


class BreedService:
    def __init__(self) -> None:
        pass

    def fetch_breed_profile(self, breed: str, species: str) -> dict:
        cache_key = f"breed:{species.lower()}:{slugify(breed)}"
        cached = cache_service.get_json(cache_key)
        if cached:
            return cached

        catalog_entry = BREED_CATALOG.get(breed.lower())
        if not catalog_entry:
            profile = self._fallback_profile(breed, species)
            cache_service.set_json(cache_key, profile)
            return profile
        profile = {
            "breed": breed,
            "species": species.lower(),
            "slug": slugify(breed),
            **catalog_entry,
        }
        profile["embedding_ids"] = [f"{profile['slug']}-{index}" for index, _ in enumerate(profile["articles"], start=1)]
        cache_service.set_json(cache_key, profile)
        return profile

    def list_supported_breeds(self) -> list[dict]:
        return [
            {"breed": breed.title(), "species": data["species"], "risk_tags": data["risk_tags"]}
            for breed, data in sorted(BREED_CATALOG.items())
        ]

    @staticmethod
    def _fallback_profile(breed: str, species: str) -> dict:
        articles = [
            {
                "title": f"{breed} baseline care",
                "source": "PetSense Knowledge Base",
                "topic": "general-care",
                "content": f"{breed} care should be personalized by age, activity, and current symptoms. Monitor appetite, hydration, stool quality, and energy changes, and contact a vet for persistent concerns.",
            }
        ]
        profile = {
            "breed": breed,
            "species": species.lower(),
            "slug": slugify(breed),
            "temperament": ["Companion animal"],
            "life_span": "Varies",
            "weight_range": "Varies",
            "care_plan": {
                "food": "Use age-appropriate balanced food with measured portions.",
                "exercise": "Provide species-appropriate daily movement and enrichment.",
                "water": "Keep fresh water available at all times.",
            },
            "risk_tags": ["Monitor appetite", "Hydration", "Behavior changes"],
            "articles": articles,
        }
        profile["embedding_ids"] = [f"{profile['slug']}-1"]
        return profile


breed_service = BreedService()
