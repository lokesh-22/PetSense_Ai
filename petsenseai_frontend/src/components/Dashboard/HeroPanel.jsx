import { useActivePet } from "../../hooks/useActivePet";
import { dailyBrief } from "../../mock-data/dashboard";
import { SectionCard } from "../Shared/SectionCard";

export function HeroPanel() {
  const activePet = useActivePet();

  return (
    <SectionCard
      title={`Hello, ${activePet?.name ?? "friend"}`}
      subtitle="A calm snapshot of what matters most today for your active pet."
      tone="hero"
    >
      <p className="hero-summary">{dailyBrief.summary}</p>
      <div className="chip-row">
        {activePet?.riskTags.map((tag) => (
          <span key={tag} className="chip">
            {tag}
          </span>
        ))}
      </div>
    </SectionCard>
  );
}
