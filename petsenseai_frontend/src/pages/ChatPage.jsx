import { useEffect, useState } from "react";
import { petsenseApi } from "../api/petsense";
import { SectionCard } from "../components/Shared/SectionCard";
import { useActivePet } from "../hooks/useActivePet";
import { useAppStore } from "../store/useAppStore";

export function ChatPage() {
  const [draft, setDraft] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const activePet = useActivePet();
  const messages = useAppStore((state) =>
    activePet ? state.chatByPet[activePet.id] ?? [] : [],
  );
  const setChatMessages = useAppStore((state) => state.setChatMessages);
  const appendChatMessage = useAppStore((state) => state.appendChatMessage);

  useEffect(() => {
    let cancelled = false;

    async function loadMessages() {
      if (!activePet) {
        return;
      }

      try {
        const response = await petsenseApi.getChatMessages(activePet.id);
        if (!cancelled) {
          setChatMessages(activePet.id, response.data.items);
        }
      } catch {
        if (!cancelled) {
          setError("Chat history could not be loaded.");
        }
      }
    }

    loadMessages();
    return () => {
      cancelled = true;
    };
  }, [activePet, setChatMessages]);

  async function handleSubmit(event) {
    event.preventDefault();
    if (!activePet || !draft.trim()) {
      return;
    }

    setLoading(true);
    setError("");
    const userMessageId = crypto.randomUUID();
    const assistantMessageId = crypto.randomUUID();

    appendChatMessage(activePet.id, {
      id: userMessageId,
      role: "user",
      content: draft,
      sources: [],
    });
    appendChatMessage(activePet.id, {
      id: assistantMessageId,
      role: "assistant",
      content: "",
      sources: [],
    });

    try {
      let streamedContent = "";
      let citations = [];

      await petsenseApi.streamChatMessage(
        {
        pet_id: activePet.id,
        message: draft,
        },
        {
          onMetadata: (payload) => {
            citations = payload.citations ?? [];
          },
          onToken: (payload) => {
            streamedContent += payload.content;
            setChatMessages(
              activePet.id,
              [...(useAppStore.getState().chatByPet[activePet.id] ?? [])].map((message) =>
                message.id === assistantMessageId
                  ? { ...message, content: streamedContent, sources: citations }
                  : message,
              ),
            );
          },
          onDone: (payload) => {
            citations = payload.citations ?? citations;
            setChatMessages(
              activePet.id,
              [...(useAppStore.getState().chatByPet[activePet.id] ?? [])].map((message) =>
                message.id === assistantMessageId
                  ? { ...message, content: streamedContent, sources: citations }
                  : message,
              ),
            );
          },
        },
      );
      setDraft("");
    } catch {
      setError("The backend did not return a chat answer.");
      setChatMessages(
        activePet.id,
        (useAppStore.getState().chatByPet[activePet.id] ?? []).filter((message) => message.id !== assistantMessageId),
      );
    } finally {
      setLoading(false);
    }
  }

  if (!activePet) {
    return (
      <div className="page">
        <SectionCard title="No active pet" subtitle="Create a profile before using chat.">
          <p>The breed-aware RAG chat activates after you add a pet in the profile screen.</p>
        </SectionCard>
      </div>
    );
  }

  return (
    <div className="page">
      <SectionCard
        title="Breed-aware chat"
        subtitle={`This response flow retrieves documents tagged for ${activePet.breed} plus universal care notes.`}
      >
        <div className="chat-thread">
          {messages.map((message, index) => (
            <article key={message.id ?? `${message.role}-${index}`} className={`message message-${message.role}`}>
              <span>{message.role === "assistant" ? "AI" : "You"}</span>
              <p>{message.content}</p>
              {message.sources?.length ? (
                <small>
                  Sources:{" "}
                  {message.sources
                    .map((source) =>
                      typeof source === "string" ? source : `[${source.index}] ${source.title}`,
                    )
                    .join(", ")}
                </small>
              ) : null}
            </article>
          ))}
          {!messages.length && <p>No messages yet. Ask your first question.</p>}
        </div>

        <form className="chat-form" onSubmit={handleSubmit}>
          <textarea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            rows={4}
            placeholder={`Ask about ${activePet.name}'s appetite, limping, grooming, or daily care...`}
          />
          {error && <div className="notice error">{error}</div>}
          <button type="submit" disabled={loading}>
            {loading ? "Thinking..." : "Send message"}
          </button>
        </form>
      </SectionCard>
    </div>
  );
}
