import React, { useState, useRef, useEffect } from "react"
import assistantService from './AssistantService'
import ReactMarkdown from "react-markdown";


const App = () => {
    const [uiState, setUiState] = useState("idle")
    const [question, setQuestion] = useState("");
    const [assistantResponse, setAssistantResponse] = useState("");
    const [feedback, setFeedback] = useState("");
    const [threadId, setThreadId] = useState(null);
    const [history, setHistory] = useState([]);



}

export default App