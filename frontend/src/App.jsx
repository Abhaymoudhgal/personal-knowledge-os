import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

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
        content: response.data.answer
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
    <div className="container">

      <h1>PKOS</h1>

      <div className="chat-box">

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

          </div>

        ))}

        {loading && (

          <div className="message assistant">

            PKOS is thinking...

          </div>

        )}

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

      </div>

    </div>
  );
}

export default App;