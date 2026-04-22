import { useEffect, useState } from "react";
import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { petsenseApi } from "../../api/petsense";
import { useActivePet } from "../../hooks/useActivePet";
import { useAppStore } from "../../store/useAppStore";

const navigation = [
  { to: "/", label: "Dashboard" },
  { to: "/chat", label: "AI Chat" },
  { to: "/health", label: "Health" },
  { to: "/scanner", label: "Food Scanner" },
  { to: "/pet-profile", label: "Pet Profile" },
];

export function AppShell() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const session = useAppStore((state) => state.session);
  const pets = useAppStore((state) => state.pets);
  const setPets = useAppStore((state) => state.setPets);
  const breeds = useAppStore((state) => state.breeds);
  const setBreeds = useAppStore((state) => state.setBreeds);
  const setActivePetId = useAppStore((state) => state.setActivePetId);
  const clearSession = useAppStore((state) => state.clearSession);
  const activePet = useActivePet();

  useEffect(() => {
    let cancelled = false;

    async function hydrate() {
      setLoading(true);
      setError("");

      try {
        const [petsResponse, breedsResponse] = await Promise.all([
          petsenseApi.getPets(),
          breeds.length ? Promise.resolve({ data: { items: breeds } }) : petsenseApi.getSupportedBreeds(),
        ]);

        if (cancelled) {
          return;
        }

        setPets(petsResponse.data, session?.user?.active_pet_id);
        if (!breeds.length) {
          setBreeds(breedsResponse.data.items);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError("We couldn't load your workspace. Please log in again.");
          clearSession();
          navigate("/login", { replace: true });
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    hydrate();
    return () => {
      cancelled = true;
    };
  }, [breeds, clearSession, navigate, session?.user?.active_pet_id, setBreeds, setPets]);

  async function handleSwitchPet(nextPetId) {
    setActivePetId(Number(nextPetId));
    try {
      await petsenseApi.switchActivePet(Number(nextPetId));
    } catch {
      setError("Active pet sync failed. Refresh after backend is running.");
    }
  }

  function handleLogout() {
    clearSession();
    navigate("/login", { replace: true });
  }

  if (loading) {
    return <main className="page-shell"><section className="section-card">Loading your pets...</section></main>;
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div>
          <p className="eyebrow">Pet Health Assistant</p>
          <h1>PetSense AI</h1>
          <p className="sidebar-copy">
            Login, onboarding, multi-pet tracking, breed-aware retrieval, and phase 2 care tools.
          </p>
        </div>

        <div className="user-pill">
          <strong>{session?.user?.full_name}</strong>
          <span>{session?.user?.email}</span>
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
            value={activePet?.id ?? ""}
            onChange={(event) => handleSwitchPet(event.target.value)}
          >
            {!pets.length && <option value="">Create your first pet</option>}
            {pets.map((pet) => (
              <option key={pet.id} value={pet.id}>
                {pet.name} · {pet.species}
              </option>
            ))}
          </select>
        </div>

        <button type="button" className="ghost-button" onClick={handleLogout}>
          Log out
        </button>
      </aside>

      <main className="content">
        {error && <div className="notice error">{error}</div>}
        <Outlet />
      </main>
    </div>
  );
}
