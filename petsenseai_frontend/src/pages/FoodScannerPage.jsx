import { useState } from "react";
import { petsenseApi } from "../api/petsense";
import { SectionCard } from "../components/Shared/SectionCard";

export function FoodScannerPage() {
  const [ingredientsText, setIngredientsText] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleScan() {
    setError("");
    try {
      const response = await petsenseApi.scanFood({ ingredients_text: ingredientsText });
      setResult(response.data);
    } catch {
      setError("Ingredient scan failed.");
    }
  }

  return (
    <div className="page">
      <SectionCard
        title="Ingredient scanner"
        subtitle="Phase 2 food-safety support with local toxic ingredient checks."
      >
        <div className="stack">
          <label className="field">
            <span>Paste ingredients</span>
            <textarea
              rows={6}
              value={ingredientsText}
              onChange={(event) => setIngredientsText(event.target.value)}
              placeholder="Chicken meal, rice, salt, garlic powder..."
            />
          </label>
          {error && <div className="notice error">{error}</div>}
          <button type="button" onClick={handleScan}>
            Scan ingredients
          </button>
        </div>

        <div className="metric-grid">
          {(result?.findings ?? []).map((flag) => (
            <article key={flag.ingredient} className="metric-card">
              <span>{flag.name}</span>
              <strong>{flag.severity}</strong>
              <p>{flag.note}</p>
            </article>
          ))}
          {result && !result.findings.length && (
            <article className="metric-card">
              <span>Status</span>
              <strong>Clear</strong>
              <p>No flagged ingredients were found in this list.</p>
            </article>
          )}
        </div>
      </SectionCard>
    </div>
  );
}
