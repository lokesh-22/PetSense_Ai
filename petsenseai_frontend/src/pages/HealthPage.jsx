import { useState } from "react";
import { petsenseApi } from "../api/petsense";
import { SectionCard } from "../components/Shared/SectionCard";
import { useActivePet } from "../hooks/useActivePet";

export function HealthPage() {
  const activePet = useActivePet();
  const [form, setForm] = useState({ symptoms: "", duration: "" });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleAnalyze(event) {
    event.preventDefault();
    if (!activePet) {
      return;
    }
    setError("");
    try {
      const response = await petsenseApi.analyzeSymptoms({
        pet_id: activePet.id,
        symptoms: form.symptoms,
        duration: form.duration,
      });
      setResult(response.data);
    } catch {
      setError("Symptom analysis failed.");
    }
  }

  return (
    <div className="page">
      <SectionCard
        title="Health overview"
        subtitle="Phase 2 features include a rule-based symptom checker and breed-specific care planner."
      >
        {activePet ? (
          <div className="metric-grid">
            <article className="metric-card">
              <span>Breed risks</span>
              <strong>{activePet.breed_profile.risk_tags.join(", ")}</strong>
            </article>
            <article className="metric-card">
              <span>Food plan</span>
              <strong>{activePet.breed_profile.care_plan.food}</strong>
            </article>
            <article className="metric-card">
              <span>Exercise plan</span>
              <strong>{activePet.breed_profile.care_plan.exercise}</strong>
            </article>
          </div>
        ) : (
          <p>Create a pet to unlock health guidance.</p>
        )}
      </SectionCard>

      <SectionCard title="Symptom checker" subtitle="Severity scoring based on the updated docs and urgent-care rules.">
        <form className="stack" onSubmit={handleAnalyze}>
          <label className="field">
            <span>Symptoms</span>
            <textarea
              rows={5}
              value={form.symptoms}
              onChange={(event) => setForm((current) => ({ ...current, symptoms: event.target.value }))}
              placeholder="Vomiting, limping, lethargy, not eating..."
            />
          </label>
          <label className="field">
            <span>Duration</span>
            <input
              value={form.duration}
              onChange={(event) => setForm((current) => ({ ...current, duration: event.target.value }))}
              placeholder="Started this morning"
            />
          </label>
          {error && <div className="notice error">{error}</div>}
          <button type="submit">Analyze symptoms</button>
        </form>

        {result && (
          <div className="stack top-gap">
            <div className="metric-card">
              <span>Severity</span>
              <strong>{result.severity}</strong>
              <p>{result.disclaimer}</p>
            </div>
            <div className="metric-card">
              <span>Possible risk context</span>
              <strong>{result.possible_causes.join(", ")}</strong>
            </div>
            <ul className="list">
              {result.recommendations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          </div>
        )}
      </SectionCard>
    </div>
  );
}
