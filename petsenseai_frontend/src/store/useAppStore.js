import { create } from "zustand";
import { readStoredSession, writeStoredSession } from "../api/client";

const initialSession = readStoredSession();

export const useAppStore = create((set) => ({
  session: initialSession,
  pets: [],
  activePetId: initialSession?.user?.active_pet_id ?? null,
  breeds: [],
  chatByPet: {},
  dashboard: null,
  setSession: (session) => {
    writeStoredSession(session);
    set({
      session,
      activePetId: session?.user?.active_pet_id ?? null,
    });
  },
  clearSession: () => {
    writeStoredSession(null);
    set({
      session: null,
      pets: [],
      activePetId: null,
      breeds: [],
      chatByPet: {},
      dashboard: null,
    });
  },
  setPets: (pets, activePetId = null) =>
    set({
      pets,
      activePetId: activePetId ?? pets[0]?.id ?? null,
    }),
  setActivePetId: (activePetId) => set({ activePetId }),
  setBreeds: (breeds) => set({ breeds }),
  setDashboard: (dashboard) => set({ dashboard }),
  setChatMessages: (petId, messages) =>
    set((state) => ({
      chatByPet: {
        ...state.chatByPet,
        [petId]: messages,
      },
    })),
  appendChatMessage: (petId, message) =>
    set((state) => ({
      chatByPet: {
        ...state.chatByPet,
        [petId]: [...(state.chatByPet[petId] ?? []), message],
      },
    })),
}));
