import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { petsenseApi } from "../api/petsense";
import { useAppStore } from "../store/useAppStore";

export function LoginPage() {
  const navigate = useNavigate();
  const setSession = useAppStore((state) => state.setSession);
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({
    full_name: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();
    setSubmitting(true);
    setError("");

    try {
      const response =
        mode === "login"
          ? await petsenseApi.login({
              email: form.email,
              password: form.password,
            })
          : await petsenseApi.register(form);

      setSession(response.data);
      navigate("/", { replace: true });
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Authentication failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <main className="auth-screen">
      <section className="auth-card">
        <p className="eyebrow">Phase 1 + Phase 2</p>
        <h1>PetSense AI</h1>
        <p className="auth-copy">
          Sign in to create profiles, manage multiple pets, and use breed-aware health support.
        </p>

        <div className="toggle-row">
          <button
            type="button"
            className={mode === "login" ? "toggle-button active" : "toggle-button"}
            onClick={() => setMode("login")}
          >
            Login
          </button>
          <button
            type="button"
            className={mode === "register" ? "toggle-button active" : "toggle-button"}
            onClick={() => setMode("register")}
          >
            Register
          </button>
        </div>

        <form className="stack" onSubmit={handleSubmit}>
          {mode === "register" && (
            <label className="field">
              <span>Full name</span>
              <input
                value={form.full_name}
                onChange={(event) => setForm((current) => ({ ...current, full_name: event.target.value }))}
                placeholder="Alex Morgan"
                required
              />
            </label>
          )}

          <label className="field">
            <span>Email</span>
            <input
              value={form.email}
              onChange={(event) => setForm((current) => ({ ...current, email: event.target.value }))}
              placeholder="you@example.com"
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              value={form.password}
              onChange={(event) => setForm((current) => ({ ...current, password: event.target.value }))}
              placeholder="Minimum 8 characters"
              required
            />
          </label>

          {error && <div className="notice error">{error}</div>}
          <button type="submit" disabled={submitting}>
            {submitting ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
          </button>
        </form>
      </section>
    </main>
  );
}
