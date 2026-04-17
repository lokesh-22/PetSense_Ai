import { useActivePet } from "../../hooks/useActivePet";
import { SectionCard } from "../Shared/SectionCard";

const metrics = [
  { label: "Weight trend", value: "+0.4 kg", note: "Slightly above ideal pace" },
  { label: "Hydration", value: "Good", note: "No alerts in recent logs" },
  { label: "Next vaccine", value: "28 days", note: "Booster reminder scheduled" },
];

export function HealthSummary() {
  const pet = useActivePet();

  return (
    <SectionCard
      title={`${pet?.name ?? "Pet"} health overview`}
      subtitle="Starter dashboard blocks for progress charts, reminders, and symptom severity."
    >
      <div className="metric-grid">
        {metrics.map((metric) => (
          <div key={metric.label} className="metric-card">
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <p>{metric.note}</p>
          </div>
        ))}
      </div>
    </SectionCard>
  );
}
