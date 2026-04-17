import { dailyBrief } from "../../mock-data/dashboard";
import { SectionCard } from "../Shared/SectionCard";

export function ReminderList() {
  return (
    <SectionCard title="Upcoming care" subtitle="Quick reminders surfaced from the dashboard plan.">
      <ul className="list">
        {dailyBrief.reminders.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </SectionCard>
  );
}
