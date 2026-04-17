import { HeroPanel } from "../components/Dashboard/HeroPanel";
import { InsightGrid } from "../components/Dashboard/InsightGrid";
import { ReminderList } from "../components/Dashboard/ReminderList";

export function DashboardPage() {
  return (
    <div className="page">
      <HeroPanel />
      <div className="grid two-col">
        <ReminderList />
        <InsightGrid />
      </div>
    </div>
  );
}
