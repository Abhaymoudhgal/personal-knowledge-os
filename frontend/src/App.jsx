import { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [documents, setDocuments] = useState([]);

  const bottomRef = useRef(null);

  useEffect(() => {
    loadDocuments();
  }, []);

  const loadDocuments = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/documents");
      setDocuments(response.data.documents || []); 
    } catch (error) {
      console.error("Error fetching documents:", error);
    }
  };

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

      // NEW: We are now capturing the sources from the backend
      const aiMessage = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources || [], 
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
      {/* SIDEBAR */}
      <div className={`sidebar ${sidebarOpen ? "" : "closed"}`}>
        <div className="sidebar-header">
          <h2>PKOS</h2>
        </div>
        
        <div className="document-list-container">
          <h3 className="doc-list-title">Indexed Documents</h3>
          
          <div className="document-list">
            {documents.length === 0 ? (
              <p className="no-docs-msg">No documents found.</p>
            ) : (
              documents.map((doc, index) => (
                <div key={index} className="document-item" title={doc.filename}>
                  📄 {doc.filename.length > 25 ? doc.filename.substring(0, 25) + "..." : doc.filename}
                </div>
              ))
            )}
          </div>
        </div>
      </div>

      {/* MAIN CONTENT */}
      <div className="main-content">
        <div className="top-bar">
          <button
            className="toggle-btn"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            aria-label="Toggle Sidebar"
          >
            ☰
          </button>
          <h1>PKOS Chat</h1>
        </div>

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
              
              {/* NEW: Render sources if they exist */}
              {msg.sources && msg.sources.length > 0 && (
                <div className="sources">
                  <strong>Sources:</strong>
                  {msg.sources.map((source, i) => (
                    <div key={i} className="source-item">
                      📄 {source.document || source.filename || "Unknown Document"}
                      {/* Optional: Add score if your backend returns it */}
                      {source.score && ` (Confidence: ${source.score})`}
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}

          {loading && (
            <div className="message assistant loading">
              PKOS is thinking<span className="dots">...</span>
            </div>
          )}

          <div ref={bottomRef}></div>
        </div>

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
          <button className="secondary-btn" onClick={() => setMessages([])}>
            Clear
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;