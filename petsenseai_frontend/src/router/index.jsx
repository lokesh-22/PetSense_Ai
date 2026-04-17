import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "../components/Layout/AppShell";
import { ChatPage } from "../pages/ChatPage";
import { DashboardPage } from "../pages/DashboardPage";
import { FoodScannerPage } from "../pages/FoodScannerPage";
import { HealthPage } from "../pages/HealthPage";
import { PetProfilePage } from "../pages/PetProfilePage";
import { NotFoundPage } from "../pages/NotFoundPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
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
