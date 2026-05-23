import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Link, useLocation } from "react-router-dom";

import ChatBotPanel from "./ChatBotPanel";

import "./FloatingAIAssistant.css";

function FloatingAIAssistant() {
  const { pathname } = useLocation();
  const chatRef = useRef(null);
  const [open, setOpen] = useState(false);

  const hideWidget = pathname === "/ai";

  useEffect(() => {
    if (!open) return undefined;
    const chat = chatRef.current;
    return () => chat?.abortOnUnmount?.();
  }, [open]);

  if (hideWidget) return null;

  const toggleOpen = () => {
    setOpen((v) => !v);
  };

  const widget = (
    <div className="ai-float-root" role="presentation">
      {open ? (
        <section className="ai-float-panel" aria-label="CollabAI ChatBot">
          <header className="ai-float-header">
            <div className="ai-float-header-brand">
              <span className="ai-float-logo" aria-hidden>
                C
              </span>
              <div>
                <strong>CollabAI ChatBot</strong>
                <span className="ai-float-status">General chat</span>
              </div>
            </div>
            <div className="ai-float-header-actions">
              <button
                type="button"
                className="ai-float-icon-btn"
                title="Clear chat"
                aria-label="Clear chat"
                onClick={() => chatRef.current?.clearChat?.()}
              >
                🧹
              </button>
              <Link
                to="/ai"
                className="ai-float-icon-btn"
                title="Open AI Assistant (project RAG)"
                aria-label="Open AI Assistant"
              >
                ↗
              </Link>
              <button
                type="button"
                className="ai-float-icon-btn ai-float-icon-btn--close"
                aria-label="Close chatbot"
                onClick={() => setOpen(false)}
              >
                ✕
              </button>
            </div>
          </header>
          <ChatBotPanel ref={chatRef} />
        </section>
      ) : null}

      <div className="ai-float-trigger">
        {!open ? (
          <span className="ai-float-hint" role="tooltip">
            Chat with CollabAI here
          </span>
        ) : null}

        <button
          type="button"
          className={`ai-float-fab${open ? " ai-float-fab--active" : ""}`}
          aria-label={open ? "Close ChatBot" : "Open ChatBot"}
          aria-expanded={open}
          onClick={toggleOpen}
        >
          <span className="ai-float-fab-logo" aria-hidden>
            C
          </span>
          <span className="ai-float-online" aria-hidden />
        </button>
      </div>
    </div>
  );

  return createPortal(widget, document.body);
}

export default FloatingAIAssistant;
