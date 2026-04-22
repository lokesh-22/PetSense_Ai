import { useEffect, useState } from "react";
import { petsenseApi } from "../api/petsense";
import { SectionCard } from "../components/Shared/SectionCard";
import { useActivePet } from "../hooks/useActivePet";
import { useAppStore } from "../store/useAppStore";

export function DashboardPage() {
  const [error, setError] = useState("");
  const activePet = useActivePet();
  const dashboard = useAppStore((state) => state.dashboard);
  const setDashboard = useAppStore((state) => state.setDashboard);

  useEffect(() => {
    let cancelled = false;

    async function loadDashboard() {
      if (!activePet) {
        setDashboard(null);
        return;
      }

      try {
        const response = await petsenseApi.getDashboard();
        if (!cancelled) {
          setDashboard(response.data);
        }
      } catch {
        if (!cancelled) {
          setError("Dashboard could not be loaded.");
        }
      }
    }

    loadDashboard();
    return () => {
      cancelled = true;
    };
  }, [activePet, setDashboard]);

  if (!activePet) {
    return (
      <div className="page">
        <SectionCard title="Create your first pet" subtitle="Login is ready. The next step is profile creation.">
          <p>Head to Pet Profile and add your first dog or cat to unlock the phase 1 and phase 2 flows.</p>
        </SectionCard>
      </div>
    );
  }

  const planner = dashboard?.planner;

  return (
    <div className="page">
      <SectionCard
        title={`Hello, ${activePet.name}`}
        subtitle={`${activePet.breed} care is now connected to stored breed documents and a local vector retrieval flow.`}
        tone="hero"
      >
        <p className="hero-summary">
          Focus today on {activePet.breed_profile.risk_tags.join(", ").toLowerCase()} and keep notes ready for chat follow-ups.
        </p>
        <div className="chip-row">
          {activePet.breed_profile.risk_tags.map((tag) => (
            <span key={tag} className="chip">
              {tag}
            </span>
          ))}
        </div>
      </SectionCard>

      <div className="grid two-col">
        <SectionCard title="Daily care planner" subtitle="Phase 2 logic built from breed, age, and weight.">
          {planner ? (
            <div className="stack">
              <div className="metric-card">
                <span>Food</span>
                <strong>{planner.food}</strong>
              </div>
              <div className="metric-card">
                <span>Exercise</span>
                <strong>{planner.exercise}</strong>
              </div>
              <div className="metric-card">
                <span>Water</span>
                <strong>{planner.water}</strong>
              </div>
              <p>{planner.notes}</p>
            </div>
          ) : (
            <p>Planner data will appear after the backend is reachable.</p>
          )}
        </SectionCard>

        <SectionCard title="Health timeline" subtitle="Early phase timeline from profile and indexing events.">
          <div className="timeline">
            {(dashboard?.timeline ?? []).map((entry) => (
              <div key={`${entry.label}-${entry.date}`} className="timeline-row">
                <strong>{entry.label}</strong>
                <span>{entry.date}</span>
                <em>{entry.status}</em>
              </div>
            ))}
            {!dashboard?.timeline?.length && <p>No timeline data yet.</p>}
          </div>
        </SectionCard>
      </div>

      <SectionCard title="Weight history" subtitle="Phase 2 readiness for growth and trend tracking.">
        <div className="metric-grid">
          {(dashboard?.weight_logs ?? []).map((entry) => (
            <article key={entry.id} className="metric-card">
              <span>Logged weight</span>
              <strong>{entry.weight_kg} kg</strong>
              <p>{entry.logged_at.slice(0, 10)}</p>
            </article>
          ))}
          {!dashboard?.weight_logs?.length && <p>No weight logs yet.</p>}
        </div>
        {error && <div className="notice error">{error}</div>}
      </SectionCard>
    </div>
  );
}
