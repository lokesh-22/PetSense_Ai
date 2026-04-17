import { create } from "zustand";
import { pets, chatMessages } from "../mock-data/dashboard";

export const usePetStore = create((set) => ({
  pets,
  activePetId: pets[0]?.id ?? null,
  chatMessages,
  setActivePet: (activePetId) => set({ activePetId }),
  addChatMessage: (message) =>
    set((state) => ({ chatMessages: [...state.chatMessages, message] })),
}));
