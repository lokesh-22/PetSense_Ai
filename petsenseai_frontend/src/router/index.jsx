import { createBrowserRouter } from "react-router-dom";
import { ProtectedLayout } from "../components/Layout/ProtectedLayout";
import { ChatPage } from "../pages/ChatPage";
import { DashboardPage } from "../pages/DashboardPage";
import { FoodScannerPage } from "../pages/FoodScannerPage";
import { HealthPage } from "../pages/HealthPage";
import { LoginPage } from "../pages/LoginPage";
import { PetProfilePage } from "../pages/PetProfilePage";
import { NotFoundPage } from "../pages/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/",
    element: <ProtectedLayout />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "chat", element: <ChatPage /> },
      { path: "health", element: <HealthPage /> },
      { path: "scanner", element: <FoodScannerPage /> },
      { path: "pet-profile", element: <PetProfilePage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);
