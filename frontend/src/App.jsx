import { useState, useEffect,useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [documents, setDocuments] = useState([]);

  const bottomRef = useRef(null);
  const [file, setFile] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {

    bottomRef.current?.scrollIntoView({
      behavior: "smooth"
    });

  }, [messages]);

  useEffect(() => {

    loadDocuments();

  }, []);

  const loadDocuments = async () => {

    try {

      const response = await axios.get(
        "http://127.0.0.1:8000/documents"
      );

      setDocuments(
        response.data.documents
      );

    } catch (error) {

      console.error(error);

    }

  };

const uploadFile = async () => {

    if (!file) return;

    const formData = new FormData();

    formData.append(
      "file",
      file
    );

    try {

      const uploadResponse = await axios.post(
        "http://127.0.0.1:8000/upload",
        formData
      );

      const filename =
        uploadResponse.data.filename;

      await axios.post(
        `http://127.0.0.1:8000/documents/${filename}/index`
      );

      alert(
        "Upload and indexing successful"
      );

      loadDocuments();

    } catch (error) {

      console.error(error);

    }

  };

  const askQuestion = async () => {

    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      content: question
    };

    setMessages(prev => [
      ...prev,
      userMessage
    ]);

    try {

      setLoading(true);

      const response = await axios.get(
        "http://127.0.0.1:8000/ask-kb",
        {
          params: {
            question
          }
        }
      );

      const aiMessage = {
        role: "assistant",
        content: response.data.answer,
        sources: response.data.sources
      };

      setMessages(prev => [
        ...prev,
        aiMessage
      ]);

      setLoading(false);

    } catch (error) {

      console.error(error);

      setLoading(false);

    }

    setQuestion("");
  };

  return (
    <div className="layout">

      <button
        className="toggle-btn"
        onClick={() =>
          setSidebarOpen(!sidebarOpen)
        }
      >
        ☰
      </button>
      <div
        className={
          sidebarOpen
            ? "sidebar"
            : "sidebar closed"
        }
      >
        <h2>Documents</h2>

                <input
          type="file"
          accept=".pdf"
          onChange={(e) =>
            setFile(e.target.files[0])
          }
        />

        <button
          onClick={uploadFile}
        >
          Upload
        </button> 
        {
          documents.map((doc, index) => (

            <div
              key={index}
              className="document-item"
              title={doc.filename}
            >
              📄 {
                doc.filename.length > 25
                  ? doc.filename.substring(0,25)
                    + "..."
                  : doc.filename
              }
            </div>

          ))
        }

      </div>

      <div className="main-content">

      <h1>PKOS</h1>

      <div className="chat-box">

        {
          messages.length === 0 && (
            <div className="empty-state">
              <h2>Welcome to PKOS</h2>

              <p>
                Ask questions about your documents.
              </p>

              <div className="examples">
                <div>• Summarize my resume</div>
                <div>• What internships have I completed?</div>
                <div>• What projects are in my documents?</div>
              </div>
            </div>
          )
        }

        {messages.map((msg, index) => (

          <div
            key={index}
            className={`message ${msg.role}`}
          >

            <strong>
              {msg.role === "user"
                ? "You"
                : "PKOS"}
              :
            </strong>

            {" "}
            {msg.content}

            {
              msg.sources && (
                <div className="sources">

                  <strong>Sources:</strong>

                  {
                    msg.sources.map(
                      (source, i) => (

                        <div key={i}>

                          📄 {source.document}
                          {" "}
                          ({source.score})

                        </div>

                      )
                    )
                  }

                </div>
              )
            }

          </div>

        ))}

        {loading && (

          <div className="message assistant">

            PKOS is thinking...

          </div>

        )}

        <div ref={bottomRef}></div>

      </div>

      <div className="input-row">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) => {

            if (e.key === "Enter") {

              askQuestion();

            }

          }}
          placeholder="Ask something..."
        />

        <button onClick={askQuestion}>
          Send
        </button>
        <button
          onClick={() => setMessages([])}
        >
          Clear
        </button>

      </div>
      
    </div>
  </div>
  );
}

export default App;