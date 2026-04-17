import { SectionCard } from "../Shared/SectionCard";

export function SymptomForm() {
  return (
    <SectionCard
      title="Symptom checker"
      subtitle="This form is staged for a future rules-based or ML-backed severity endpoint."
    >
      <div className="stack">
        <label className="field">
          <span>Symptoms</span>
          <textarea rows={5} placeholder="Vomiting, lethargy, loss of appetite..." />
        </label>
        <label className="field">
          <span>Duration</span>
          <input type="text" placeholder="Since this morning" />
        </label>
        <button type="button">Analyze symptoms</button>
      </div>
    </SectionCard>
  );
}
