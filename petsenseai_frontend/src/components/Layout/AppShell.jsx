import { NavLink, Outlet } from "react-router-dom";
import { useActivePet } from "../../hooks/useActivePet";
import { usePetStore } from "../../store/usePetStore";

const navigation = [
  { to: "/", label: "Dashboard" },
  { to: "/chat", label: "AI Chat" },
  { to: "/health", label: "Health" },
  { to: "/scanner", label: "Food Scanner" },
  { to: "/pet-profile", label: "Pet Profile" },
];

export function AppShell() {
  const pets = usePetStore((state) => state.pets);
  const setActivePet = usePetStore((state) => state.setActivePet);
  const activePet = useActivePet();

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Pet Health Assistant</p>
          <h1>PetSense AI</h1>
          <p className="sidebar-copy">
            Frontend scaffold for personalized pet guidance, chat, scanning, and health tracking.
          </p>
        </div>

        <nav className="nav">
          {navigation.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) => (isActive ? "nav-link active" : "nav-link")}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div className="pet-switcher">
          <label htmlFor="pet-select">Active pet</label>
          <select
            id="pet-select"
            value={activePet?.id}
            onChange={(event) => setActivePet(event.target.value)}
          >
            {pets.map((pet) => (
              <option key={pet.id} value={pet.id}>
                {pet.name} · {pet.species}
              </option>
            ))}
          </select>
        </div>
      </aside>

      <main className="content">
        <Outlet />
      </main>
    </div>
  );
}
