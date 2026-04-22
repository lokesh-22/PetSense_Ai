import { apiClient, readStoredSession } from "./client";

export const petsenseApi = {
  register: (payload) => apiClient.post("/auth/register", payload),
  login: (payload) => apiClient.post("/auth/login", payload),
  getMe: () => apiClient.get("/auth/me"),
  getSupportedBreeds: () => apiClient.get("/breed/supported"),
  fetchBreedInfo: (breed, species) =>
    apiClient.get("/breed/fetch", {
      params: { breed, species },
    }),
  getPets: () => apiClient.get("/pets"),
  createPet: (payload) => apiClient.post("/pets", payload),
  updatePet: (petId, payload) => apiClient.put(`/pets/${petId}`, payload),
  deletePet: (petId) => apiClient.delete(`/pets/${petId}`),
  switchActivePet: (petId) => apiClient.post("/pets/active", { pet_id: petId }),
  getDashboard: () => apiClient.get("/health/dashboard"),
  getChatMessages: (petId) => apiClient.get(`/chat/${petId}`),
  streamChatMessage: async (payload, handlers) => {
    const session = readStoredSession();
    const response = await fetch(`${apiClient.defaults.baseURL}/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(session?.access_token ? { Authorization: `Bearer ${session.access_token}` } : {}),
      },
      body: JSON.stringify(payload),
    });

    if (!response.ok || !response.body) {
      throw new Error("Streaming chat request failed.");
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop() ?? "";

      for (const event of events) {
        if (!event.startsWith("data: ")) {
          continue;
        }
        const payloadData = JSON.parse(event.slice(6));
        if (payloadData.type === "metadata") {
          handlers?.onMetadata?.(payloadData);
        } else if (payloadData.type === "token") {
          handlers?.onToken?.(payloadData);
        } else if (payloadData.type === "done") {
          handlers?.onDone?.(payloadData);
        }
      }
    }
  },
  ingestKnowledgeBase: () => apiClient.post("/ingest"),
  analyzeSymptoms: (payload) => apiClient.post("/health/symptoms", payload),
  getWeightOverview: (petId) => apiClient.get(`/health/weight/${petId}`),
  scanFood: (payload) => apiClient.post("/scanner/ingredients", payload),
};
