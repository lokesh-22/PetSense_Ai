import { HealthSummary } from "../components/HealthTracker/HealthSummary";
import { SymptomForm } from "../components/SymptomChecker/SymptomForm";

export function HealthPage() {
  return (
    <div className="page">
      <HealthSummary />
      <SymptomForm />
    </div>
  );
}
