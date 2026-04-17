import { useState } from "react";
import { useActivePet } from "../../hooks/useActivePet";
import { usePetStore } from "../../store/usePetStore";
import { SectionCard } from "../Shared/SectionCard";

export function ChatPanel() {
  const [draft, setDraft] = useState("");
  const activePet = useActivePet();
  const chatMessages = usePetStore((state) => state.chatMessages);
  const addChatMessage = usePetStore((state) => state.addChatMessage);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!draft.trim()) {
      return;
    }

    const userMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: draft,
    };

    addChatMessage(userMessage);
    addChatMessage({
      id: crypto.randomUUID(),
      role: "assistant",
      content: `Stub response for ${activePet?.name ?? "your pet"}: connect this panel to the FastAPI chat endpoint for streaming answers.`,
    });
    setDraft("");
  };

  return (
    <SectionCard
      title="Health chat"
      subtitle="Designed for personalized answers once the backend RAG service is connected."
    >
      <div className="chat-thread">
        {chatMessages.map((message) => (
          <article key={message.id} className={`message message-${message.role}`}>
            <span>{message.role === "assistant" ? "AI" : "You"}</span>
            <p>{message.content}</p>
          </article>
        ))}
      </div>

      <form className="chat-form" onSubmit={handleSubmit}>
        <textarea
          value={draft}
          onChange={(event) => setDraft(event.target.value)}
          placeholder="Describe symptoms, diet concerns, or follow-up questions..."
          rows={4}
        />
        <button type="submit">Send message</button>
      </form>
    </SectionCard>
  );
}
