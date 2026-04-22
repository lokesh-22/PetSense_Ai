import { useEffect, useState } from "react";
import { petsenseApi } from "../api/petsense";
import { SectionCard } from "../components/Shared/SectionCard";
import { useActivePet } from "../hooks/useActivePet";
import { useAppStore } from "../store/useAppStore";

export function PetProfilePage() {
  const activePet = useActivePet();
  const pets = useAppStore((state) => state.pets);
  const breeds = useAppStore((state) => state.breeds);
  const setPets = useAppStore((state) => state.setPets);
  const setActivePetId = useAppStore((state) => state.setActivePetId);
  const [editingPetId, setEditingPetId] = useState(null);
  const [breedPreview, setBreedPreview] = useState(null);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    name: "",
    species: "dog",
    breed: "Labrador Retriever",
    age_years: 3,
    weight_kg: 25,
    notes: "",
  });

  useEffect(() => {
    if (!editingPetId) {
      return;
    }
    const pet = pets.find((item) => item.id === editingPetId);
    if (pet) {
      setForm({
        name: pet.name,
        species: pet.species,
        breed: pet.breed,
        age_years: pet.age_years,
        weight_kg: pet.weight_kg,
        notes: pet.notes ?? "",
      });
    }
  }, [editingPetId, pets]);

  async function refreshPets() {
    const response = await petsenseApi.getPets();
    setPets(response.data);
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError("");

    try {
      if (editingPetId) {
        await petsenseApi.updatePet(editingPetId, form);
      } else {
        await petsenseApi.createPet(form);
      }
      await refreshPets();
      setEditingPetId(null);
      setForm({
        name: "",
        species: "dog",
        breed: "Labrador Retriever",
        age_years: 3,
        weight_kg: 25,
        notes: "",
      });
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Saving pet profile failed.");
    }
  }

  async function handlePreviewBreed() {
    setError("");
    try {
      const response = await petsenseApi.fetchBreedInfo(form.breed, form.species);
      setBreedPreview(response.data);
    } catch {
      setError("Breed preview failed.");
    }
  }

  async function handleSwitch(petId) {
    await petsenseApi.switchActivePet(petId);
    setActivePetId(petId);
  }

  async function handleDelete(petId) {
    await petsenseApi.deletePet(petId);
    await refreshPets();
  }

  const availableBreeds = breeds.filter((item) => item.species === form.species);

  return (
    <div className="page">
      <div className="grid two-col">
        <SectionCard
          title={editingPetId ? "Edit pet profile" : "Create pet profile"}
          subtitle="This drives multi-pet support, breed indexing, and personalized guidance."
        >
          <form className="stack" onSubmit={handleSubmit}>
            <label className="field">
              <span>Name</span>
              <input
                value={form.name}
                onChange={(event) => setForm((current) => ({ ...current, name: event.target.value }))}
                placeholder="Mochi"
                required
              />
            </label>
            <label className="field">
              <span>Species</span>
              <select
                value={form.species}
                onChange={(event) =>
                  setForm((current) => ({
                    ...current,
                    species: event.target.value,
                    breed: event.target.value === "dog" ? "Labrador Retriever" : "Persian",
                  }))
                }
              >
                <option value="dog">Dog</option>
                <option value="cat">Cat</option>
              </select>
            </label>
            <label className="field">
              <span>Breed</span>
              <select
                value={form.breed}
                onChange={(event) => setForm((current) => ({ ...current, breed: event.target.value }))}
              >
                {availableBreeds.map((breed) => (
                  <option key={breed.breed} value={breed.breed}>
                    {breed.breed}
                  </option>
                ))}
              </select>
            </label>
            <div className="grid two-col compact-grid">
              <label className="field">
                <span>Age (years)</span>
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={form.age_years}
                  onChange={(event) => setForm((current) => ({ ...current, age_years: Number(event.target.value) }))}
                />
              </label>
              <label className="field">
                <span>Weight (kg)</span>
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={form.weight_kg}
                  onChange={(event) => setForm((current) => ({ ...current, weight_kg: Number(event.target.value) }))}
                />
              </label>
            </div>
            <label className="field">
              <span>Notes</span>
              <textarea
                rows={4}
                value={form.notes}
                onChange={(event) => setForm((current) => ({ ...current, notes: event.target.value }))}
                placeholder="Sensitive stomach, recent limp, indoor-only..."
              />
            </label>
            {error && <div className="notice error">{error}</div>}
            <div className="button-row">
              <button type="submit">{editingPetId ? "Update pet" : "Create pet"}</button>
              <button type="button" className="ghost-button" onClick={handlePreviewBreed}>
                Preview breed knowledge
              </button>
            </div>
          </form>
        </SectionCard>

        <SectionCard title="Multi-pet system" subtitle="Add, switch, edit, and delete pets from one account.">
          <div className="stack">
            {pets.map((pet) => (
              <article key={pet.id} className={`metric-card ${activePet?.id === pet.id ? "highlight" : ""}`}>
                <span>{pet.species}</span>
                <strong>{pet.name}</strong>
                <p>
                  {pet.breed} · {pet.age_years} years · {pet.weight_kg} kg
                </p>
                <div className="chip-row">
                  {pet.breed_profile.risk_tags.map((tag) => (
                    <span key={tag} className="chip">
                      {tag}
                    </span>
                  ))}
                </div>
                <div className="button-row top-gap">
                  <button type="button" onClick={() => handleSwitch(pet.id)}>
                    Set active
                  </button>
                  <button type="button" className="ghost-button" onClick={() => setEditingPetId(pet.id)}>
                    Edit
                  </button>
                  <button type="button" className="ghost-button danger-button" onClick={() => handleDelete(pet.id)}>
                    Delete
                  </button>
                </div>
              </article>
            ))}
            {!pets.length && <p>No pets yet. Create one to start phase 1.</p>}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Breed profile preview" subtitle="Preview what gets fetched, embedded, and stored for the selected breed.">
        {breedPreview ? (
          <div className="stack">
            <div className="metric-grid">
              <article className="metric-card">
                <span>Breed</span>
                <strong>{breedPreview.breed}</strong>
              </article>
              <article className="metric-card">
                <span>Life span</span>
                <strong>{breedPreview.life_span}</strong>
              </article>
              <article className="metric-card">
                <span>Weight range</span>
                <strong>{breedPreview.weight_range}</strong>
              </article>
            </div>
            <div className="chip-row">
              {breedPreview.risk_tags.map((tag) => (
                <span key={tag} className="chip">
                  {tag}
                </span>
              ))}
            </div>
            <div className="stack">
              {breedPreview.articles.map((article) => (
                <article key={article.title} className="metric-card">
                  <span>{article.topic}</span>
                  <strong>{article.title}</strong>
                  <p>{article.content}</p>
                </article>
              ))}
            </div>
          </div>
        ) : (
          <p>Use “Preview breed knowledge” to inspect the profile and documents that will be stored.</p>
        )}
      </SectionCard>
    </div>
  );
}
