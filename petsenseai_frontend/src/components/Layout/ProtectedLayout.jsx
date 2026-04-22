import { Navigate } from "react-router-dom";
import { useAppStore } from "../../store/useAppStore";
import { AppShell } from "./AppShell";

export function ProtectedLayout() {
  const session = useAppStore((state) => state.session);
  return session ? <AppShell /> : <Navigate to="/login" replace />;
}
