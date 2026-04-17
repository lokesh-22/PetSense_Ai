import { symptomInsights, timeline } from "../../mock-data/dashboard";
import { SectionCard } from "../Shared/SectionCard";

export function InsightGrid() {
  return (
    <div className="grid two-col">
      <SectionCard title="Signals" subtitle="Placeholder cards for the AI-assisted modules.">
        <div className="stack">
          {symptomInsights.map((item) => (
            <article key={item.title} className={`insight insight-${item.tone}`}>
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          ))}
        </div>
      </SectionCard>

      <SectionCard title="Health timeline" subtitle="This area is ready for backend events and reminders.">
        <div className="timeline">
          {timeline.map((entry) => (
            <div key={`${entry.label}-${entry.date}`} className="timeline-row">
              <strong>{entry.label}</strong>
              <span>{entry.date}</span>
              <em>{entry.status}</em>
            </div>
          ))}
        </div>
      </SectionCard>
    </div>
  );
}
