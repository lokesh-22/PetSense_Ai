import { useAppStore } from "../store/useAppStore";

export function useActivePet() {
  const pets = useAppStore((state) => state.pets);
  const activePetId = useAppStore((state) => state.activePetId);
  return pets.find((pet) => pet.id === activePetId) ?? pets[0] ?? null;
}
