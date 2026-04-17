import { usePetStore } from "../store/usePetStore";

export function useActivePet() {
  const pets = usePetStore((state) => state.pets);
  const activePetId = usePetStore((state) => state.activePetId);
  return pets.find((pet) => pet.id === activePetId) ?? pets[0] ?? null;
}
