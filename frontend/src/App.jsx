import { useState } from "react";
import axios from "axios";

function App() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const askQuestion = async () => {

    const response = await axios.get(
      "http://127.0.0.1:8000/ask-kb",
      {
        params: {
          question: question
        }
      }
    );

    setAnswer(
      response.data.answer
    );
  };

  return (
    <div style={{ padding: "30px" }}>

      <h1>PKOS</h1>

      <input
        type="text"
        value={question}
        onChange={(e) =>
          setQuestion(e.target.value)
        }
        placeholder="Ask a question..."
        style={{
          width: "500px",
          padding: "10px"
        }}
      />

      <button
        onClick={askQuestion}
        style={{
          marginLeft: "10px",
          padding: "10px"
        }}
      >
        Ask
      </button>

      <hr />

      <h3>Answer</h3>

      <p>{answer}</p>

    </div>
  );
}

export default App;