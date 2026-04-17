import { apiClient } from "./client";

export const petsenseApi = {
  getPets: () => apiClient.get("/pets"),
  getDashboard: () => apiClient.get("/health/dashboard"),
  sendChatMessage: (payload) => apiClient.post("/chat", payload),
  analyzeSymptoms: (payload) => apiClient.post("/health/symptoms", payload),
  scanFood: (payload) => apiClient.post("/scanner/ingredients", payload),
};
