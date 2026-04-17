import { useActivePet } from "../../hooks/useActivePet";
import { SectionCard } from "../Shared/SectionCard";

export function PetDetails() {
  const pet = useActivePet();

  return (
    <div className="grid two-col">
      <SectionCard title="Profile" subtitle="Core pet details that can feed chat personalization later.">
        <dl className="detail-list">
          <div>
            <dt>Name</dt>
            <dd>{pet?.name}</dd>
          </div>
          <div>
            <dt>Species</dt>
            <dd>{pet?.species}</dd>
          </div>
          <div>
            <dt>Breed</dt>
            <dd>{pet?.breed}</dd>
          </div>
          <div>
            <dt>Age</dt>
            <dd>{pet?.age}</dd>
          </div>
          <div>
            <dt>Weight</dt>
            <dd>{pet?.weight}</dd>
          </div>
        </dl>
      </SectionCard>

      <SectionCard title="Breed risks" subtitle="Ready for AKC/API-backed enrichment once backend services arrive.">
        <div className="chip-row">
          {pet?.riskTags.map((tag) => (
            <span key={tag} className="chip">
              {tag}
            </span>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
