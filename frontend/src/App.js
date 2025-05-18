import React, { useState, useRef, useEffect } from "react";
import Editor from "@monaco-editor/react";
import "./styles.css";

export default function App() {
  const [code, setCode] = useState(
    `name = input("Enter your name: ")\nage = input("Enter your age: ")\nprint("Hello", name)\nprint("You are", age, "years old")`
  );
  const [consoleContent, setConsoleContent] = useState("");
  const [inputData, setInputData] = useState("");
  const [theme, setTheme] = useState("vs-dark");
  const [isRunning, setIsRunning] = useState(false);

  const consoleRef = useRef(null);

  useEffect(() => {
    if (consoleRef.current) {
      consoleRef.current.scrollTop = consoleRef.current.scrollHeight;
    }
  }, [consoleContent]);

  const runCode = async () => {
    setIsRunning(true);
    setConsoleContent("Running...\n");

    try {
      const response = await fetch("/execute", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, input: inputData }),
      });

      const data = await response.json();
      setConsoleContent(data.output);
    } catch (error) {
      setConsoleContent("[Error] Failed to execute code.");
    }

    setIsRunning(false);
  };

  const downloadFile = () => {
    const blob = new Blob([code], { type: "text/plain" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "code.py";
    a.click();
  };

  const handleUpload = (e) => {
    const reader = new FileReader();
    reader.onload = (evt) => setCode(evt.target.result);
    reader.readAsText(e.target.files[0]);
  };

  const toggleTheme = () => {
    setTheme(theme === "vs-dark" ? "light" : "vs-dark");
  };

  const clearConsole = () => {
    setConsoleContent("");
    setInputData("");
  };

  return (
    <div className="app">
      <div className="toolbar">
        <button onClick={runCode} disabled={isRunning}>▶ Run</button>
        <button onClick={downloadFile}>⬇ Download</button>
        <input type="file" accept=".py" onChange={handleUpload} />
        <button onClick={toggleTheme}>
          {theme === "vs-dark" ? "☀️ Light" : "🌙 Dark"}
        </button>
        <button onClick={clearConsole}>🧹 Clear Console</button>
      </div>

      <div className="container">
        <div className="editor-container">
          <Editor
            height="90vh"
            language="python"
            value={code}
            onChange={(value) => setCode(value || "")}
            theme={theme}
            options={{
              fontSize: 16,
              minimap: { enabled: false },
              wordWrap: "on",
            }}
            readOnly={isRunning}
          />
        </div>

        <div className="console-container">
          <h3>Console</h3>
          <pre ref={consoleRef} className="console">{consoleContent}</pre>
          <textarea
            className="console-input"
            placeholder="Enter input values here (one per line)"
            value={inputData}
            onChange={(e) => setInputData(e.target.value)}
          />
        </div>
      </div>
    </div>
  );
}
