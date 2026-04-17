import { ingredientFlags } from "../mock-data/dashboard";
import { SectionCard } from "../components/Shared/SectionCard";

export function FoodScannerPage() {
  return (
    <div className="page">
      <SectionCard
        title="Ingredient scanner"
        subtitle="Upload and OCR can be wired here later. The UI is ready for flagged ingredient results."
      >
        <div className="stack">
          <label className="field">
            <span>Paste ingredients</span>
            <textarea rows={6} placeholder="Chicken meal, rice, salt, garlic powder..." />
          </label>
          <button type="button">Scan ingredients</button>
        </div>

        <div className="metric-grid">
          {ingredientFlags.map((flag) => (
            <article key={flag.ingredient} className="metric-card">
              <span>{flag.ingredient}</span>
              <strong>{flag.severity}</strong>
              <p>{flag.note}</p>
            </article>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
