import { useState } from "react";
import axios from "axios";
import "./App.css";

 const API_URL = "https://pdf-chatbot-ho7j.onrender.com";

function App() {
  const [file, setFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]); // { role: "user"|"bot", text: string, sources?: [] }
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploadStatus("Uploading...");
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`${API_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadStatus(`✅ ${res.data.message} (${res.data.chunks_stored} chunks)`);
    } catch (err) {
      setUploadStatus("❌ Upload failed: " + err.message);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    const userMessage = { role: "user", text: question };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setQuestion("");

    try {
      const res = await axios.post(`${API_URL}/chat`, { question });
      const botMessage = {
        role: "bot",
        text: res.data.answer,
        sources: res.data.sources,
      };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Error: " + err.message },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h1>📄 PDF Chatbot</h1>

      <div style={{ marginBottom: 20, padding: 15, border: "1px solid #ccc", borderRadius: 8 }}>
        <h3>1. Upload a PDF</h3>
        <input type="file" accept="application/pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} style={{ marginLeft: 10 }}>Upload</button>
        <p>{uploadStatus}</p>
      </div>

      <div style={{ border: "1px solid #ccc", borderRadius: 8, padding: 15, minHeight: 300 }}>
        <h3>2. Ask a question</h3>
        <div style={{ marginBottom: 15 }}>
          {messages.map((msg, i) => (
            <div
              key={i}
              style={{
                textAlign: msg.role === "user" ? "right" : "left",
                margin: "10px 0",
              }}
            >
              <b>{msg.role === "user" ? "You" : "Bot"}:</b> {msg.text}
              {msg.sources && (
                <details style={{ fontSize: 12, color: "#666", marginTop: 4 }}>
                  <summary>Sources ({msg.sources.length})</summary>
                  {msg.sources.map((s, j) => (
                    <p key={j}>{s.slice(0, 150)}...</p>
                  ))}
                </details>
              )}
            </div>
          ))}
          {loading && <p><i>Thinking...</i></p>}
        </div>

        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
          placeholder="Ask something about the PDF..."
          style={{ width: "80%", padding: 8 }}
        />
        <button onClick={handleAsk} style={{ padding: 8, marginLeft: 10 }}>
          Send
        </button>
      </div>
    </div>
  );
}

export default App;