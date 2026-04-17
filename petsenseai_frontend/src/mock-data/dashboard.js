export const pets = [
  {
    id: "pet-1",
    name: "Mochi",
    species: "Dog",
    breed: "Labrador Retriever",
    age: "4 years",
    weight: "26.4 kg",
    riskTags: ["Joint care", "Weight management", "Ear health"],
  },
  {
    id: "pet-2",
    name: "Olive",
    species: "Cat",
    breed: "Domestic Shorthair",
    age: "2 years",
    weight: "4.8 kg",
    riskTags: ["Dental care", "Hydration"],
  },
];

export const dailyBrief = {
  summary: "Mochi is due for flea prevention in 3 days and has a slightly elevated weight trend this month.",
  reminders: [
    "Flea prevention refill due on Sunday",
    "Weight check scheduled for next week",
    "Ear cleaning recommended after yesterday's swim",
  ],
};

export const timeline = [
  { label: "Vaccination", date: "Apr 02", status: "Completed" },
  { label: "Weight log", date: "Apr 10", status: "Watch" },
  { label: "Deworming", date: "Apr 20", status: "Upcoming" },
];

export const symptomInsights = [
  { title: "Symptom checker", body: "Mild lethargy + low appetite entered yesterday. Monitor hydration and escalate if vomiting begins.", tone: "warning" },
  { title: "Food scanner", body: "No toxic ingredients found in the last scanned treat, but sodium content is high for daily feeding.", tone: "safe" },
  { title: "Vet access", body: "Two emergency clinics are within a 15-minute drive if symptoms worsen.", tone: "info" },
];

export const chatMessages = [
  {
    id: "m1",
    role: "assistant",
    content:
      "I can help with symptoms, diet, breed risks, and health reminders. Tell me what changed with Mochi today.",
  },
  {
    id: "m2",
    role: "user",
    content: "Mochi seems tired after a long walk and skipped breakfast.",
  },
  {
    id: "m3",
    role: "assistant",
    content:
      "That can happen after extra exertion, but keep an eye on hydration, gum color, and whether energy returns within a few hours. If lethargy continues or vomiting starts, contact a vet.",
  },
];

export const ingredientFlags = [
  { ingredient: "Garlic powder", severity: "High", note: "Potentially toxic for dogs and cats." },
  { ingredient: "Salt", severity: "Medium", note: "Too much can worsen dehydration risk." },
  { ingredient: "Chicken meal", severity: "Low", note: "Common protein source; generally acceptable." },
];
