import React, { useEffect, useRef, useState } from "react";

// Single-file chat UI component
// - Uses React hooks only (`useState`, `useEffect`, `useRef`)
// - Inline CSS is injected via a <style> tag so everything stays in one file

export default function App() {
  const [messages, setMessages] = useState([]); // { id, role: 'user'|'assistant', text }
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false); // bot typing indicator
  const messagesEndRef = useRef(null);

  // Auto-scroll to latest message when `messages` or `loading` changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  // Mock bot response: simulate latency and return a canned reply
  const mockBotResponse = async (userText) => {
    setLoading(true);
    // simulate typing delay (1.2 - 1.8s)
    const delay = 1200 + Math.random() * 600;
    await new Promise((res) => setTimeout(res, delay));

    // simple mock reply — you can replace this with an API call later
    const reply = `You said: "${userText}"\n\n(This is a simulated response.)`;

    setMessages((prev) => [
      ...prev,
      { id: Date.now() + 1, role: "assistant", text: reply },
    ]);
    setLoading(false);
  };

  // Send handler: adds user message and triggers bot reply
  const handleSend = () => {
    const trimmed = input.trim();
    if (!trimmed || loading) return;

    const userMsg = { id: Date.now(), role: "user", text: trimmed };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");

    // call mock response (keep it async and non-blocking)
    mockBotResponse(trimmed);
  };

  // keyboard handler: Enter to send, Shift+Enter for newline
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  // inline CSS to keep component single-file
  const css = `
    :root{--bg:#0f1724;--panel:#0b1220;--muted:#9aa4b2;--accent:#7c3aed;--user:#0ea5a4}
    *{box-sizing:border-box}
    body,html,#root{height:100%}
    .chat-app{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:24px;background:linear-gradient(180deg,#071028 0%, #04111b 100%)}
    .chat-panel{width:100%;max-width:920px;background:linear-gradient(180deg,rgba(255,255,255,0.02),transparent);border-radius:14px;box-shadow:0 8px 30px rgba(2,6,23,0.6);overflow:hidden;display:flex;flex-direction:column}
    .chat-header{display:flex;align-items:center;gap:12px;padding:18px 20px;border-bottom:1px solid rgba(255,255,255,0.03)}
    .bot-avatar{width:44px;height:44px;border-radius:9px;background:linear-gradient(135deg,var(--accent),#4f46e5);display:flex;align-items:center;justify-content:center;color:white;font-weight:700;font-size:18px}
    .header-title{display:flex;flex-direction:column}
    .title{font-weight:600;color:#e6eef8}
    .status{font-size:12px;color:var(--muted);display:flex;align-items:center;gap:8px}
    .status .dot{width:8px;height:8px;border-radius:99px;background:#34d399;box-shadow:0 0 6px rgba(52,211,153,0.12)}
    .chat-body{padding:20px;flex:1;overflow:auto;background:linear-gradient(180deg,transparent,rgba(255,255,255,0.01));display:flex;flex-direction:column;gap:12px}
    .empty-state{margin:auto;text-align:center;color:var(--muted);padding:40px}
    .message-row{display:flex}
    .message{max-width:75%;padding:12px 14px;border-radius:12px;line-height:1.4;box-shadow:0 6px 18px rgba(2,6,23,0.5)}
    .message.user{margin-left:auto;background:linear-gradient(90deg,rgba(14,165,164,0.12),rgba(124,58,237,0.06));border:1px solid rgba(14,165,164,0.12);color:#dff7f6}
    .message.assistant{margin-right:auto;background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.02);color:#e6eef8}
    .meta{font-size:11px;color:var(--muted);margin-top:6px}
    .typing{display:flex;align-items:center;gap:8px}
    .dots{width:36px;height:12px;display:flex;align-items:center;gap:4px}
    .dot-anim{width:8px;height:8px;border-radius:99px;background:rgba(255,255,255,0.6);opacity:0.4;animation:blink 1s infinite}
    .dot-anim:nth-child(2){animation-delay:0.12s}
    .dot-anim:nth-child(3){animation-delay:0.24s}
    @keyframes blink{0%{transform:translateY(0);opacity:0.25}50%{transform:translateY(-6px);opacity:1}100%{transform:translateY(0);opacity:0.25}}

    .chat-input{display:flex;padding:14px;border-top:1px solid rgba(255,255,255,0.03);gap:12px;background:linear-gradient(180deg,transparent,rgba(255,255,255,0.01))}
    .input-area{flex:1;display:flex;align-items:center;gap:12px}
    textarea.input{width:100%;min-height:44px;max-height:140px;padding:10px 12px;border-radius:10px;border:1px solid rgba(255,255,255,0.03);background:transparent;color:#e6eef8;resize:none;font-size:14px}
    .send-btn{background:var(--accent);color:white;padding:10px 14px;border-radius:10px;border:none;font-weight:600;cursor:pointer;box-shadow:0 6px 18px rgba(124,58,237,0.18)}
    .send-btn:disabled{opacity:0.5;cursor:not-allowed;box-shadow:none}

    @media (max-width:640px){
      .chat-panel{border-radius:10px;margin:8px}
      .chat-header{padding:12px}
      .chat-body{padding:14px}
      .chat-input{padding:10px}
    }
  `;

  return (
    <div className="chat-app">
      <style>{css}</style>
      <div className="chat-panel" role="region" aria-label="Chat interface">
        <header className="chat-header">
          <div className="bot-avatar">DB</div>
          <div className="header-title">
            <div className="title">Doxa Bot</div>
            <div className="status">
              <span className="dot" /> Online
            </div>
          </div>
        </header>

        <main className="chat-body">
          {messages.length === 0 && !loading ? (
            <div className="empty-state">
              <h3 style={{ margin: 0, color: "#e6eef8" }}>
                Welcome to Doxa Bot
              </h3>
              <p style={{ marginTop: 8 }}>
                Start the conversation — ask a question or send a message.
              </p>
            </div>
          ) : (
            messages.map((m) => (
              <div
                className="message-row"
                key={m.id}
                style={{
                  justifyContent: m.role === "user" ? "flex-end" : "flex-start",
                }}
              >
                <div className={`message ${m.role}`}>
                  <div style={{ whiteSpace: "pre-wrap" }}>{m.text}</div>
                </div>
              </div>
            ))
          )}

          {/* typing indicator */}
          {loading && (
            <div
              className="message-row"
              style={{ justifyContent: "flex-start" }}
            >
              <div className="message assistant">
                <div className="typing">
                  <strong style={{ marginRight: 8, opacity: 0.9 }}>
                    Doxa Bot
                  </strong>
                  <div className="dots">
                    <div className="dot-anim" />
                    <div className="dot-anim" />
                    <div className="dot-anim" />
                  </div>
                </div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </main>

        <div className="chat-input">
          <div className="input-area">
            <textarea
              className="input"
              placeholder={
                loading ? "Waiting for response..." : "Type a message"
              }
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={loading}
            />
          </div>
          <div>
            <button
              className="send-btn"
              onClick={handleSend}
              disabled={loading || input.trim() === ""}
              aria-disabled={loading || input.trim() === ""}
            >
              {loading ? "..." : "Send"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
