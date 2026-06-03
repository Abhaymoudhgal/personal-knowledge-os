import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages]);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const response = await axios.get("http://127.0.0.1:8000/ask-kb", {
        params: {
          question,
        },
      });

      const aiMessage = {
        role: "assistant",
        content: response.data.answer,
      };

      setMessages((prev) => [...prev, aiMessage]);
      setLoading(false);
    } catch (error) {
      console.error(error);
      setLoading(false);
    }

    setQuestion("");
  };

  return (
    <div className="layout">
      {/* SIDEBAR (Cleaned up, no upload logic) */}
      <div className={`sidebar ${sidebarOpen ? "" : "closed"}`}>
        <div className="sidebar-header">
          <h2>PKOS Menu</h2>
        </div>
        <div className="sidebar-info">
          <p>Document uploading and indexing is handled server-side in this version.</p>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="main-content">
        {/* TOP BAR */}
        <div className="top-bar">
          <button
            className="toggle-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle Sidebar"
          >
            ☰
          </button>
          <h1>PKOS</h1>
        </div>

        {/* CHAT INTERFACE */}
        <div className="chat-box">
          {messages.length === 0 && (
            <div className="empty-state">
              <h2>Welcome to PKOS</h2>
              <p>Ask questions about your knowledge base.</p>
              <div className="examples">
                <div>• Where did Abhay intern?</div>
                <div>• Summarize the main document</div>
                <div>• What projects are listed?</div>
              </div>
            </div>
          )}

          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <strong>{msg.role === "user" ? "You" : "PKOS"}:</strong>{" "}
              {msg.content}
            </div>
          ))}

          {loading && (
            <div className="message assistant loading">
              PKOS is thinking<span className="dots">...</span>
            </div>
          )}

          <div ref={bottomRef}></div>
        </div>

        {/* INPUT AREA */}
        <div className="input-row">
          <input
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askQuestion();
              }
            }}
            placeholder="Ask something..."
          />
          <button className="primary-btn" onClick={askQuestion}>
            Send
          </button>
          {/* CLEAR BUTTON */}
          <button className="secondary-btn" onClick={() => setMessages([])}>
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;