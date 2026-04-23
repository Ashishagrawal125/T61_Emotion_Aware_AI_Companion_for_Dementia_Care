"use client";

import { useState, useRef } from "react";
import { sendMessageStream } from "../utils/api";

type Message = {
  role: "user" | "ai";
  content: string;
};

export default function ChatBox({ emotion }: { emotion: string }) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);

  const recognitionRef = useRef<any>(null);

  // 🔊 SPEAK FUNCTION
  const speakText = (text: string) => {
    window.speechSynthesis.cancel(); // stop previous speech
    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";
    speech.rate = 1;
    window.speechSynthesis.speak(speech);
  };

  // ⛔ STOP SPEECH
  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
  };

  // 💬 TEXT SEND
  const handleSend = async () => {
    if (!input) return;

    const userMessage = { role: "user", content: input };
    setMessages((prev: Message[]) => [...prev, userMessage]);

    setInput("");
    setLoading(true);

    let aiText = "";
    const aiIndex = messages.length + 1;

    setMessages((prev: Message[]) => [
      ...prev,
      { role: "ai", content: "" },
    ]);

    await sendMessageStream(input, emotion, (chunk) => {
      aiText += chunk;

      setMessages((prev: Message[]) => {
        const updated = [...prev];
        updated[aiIndex] = {
          role: "ai",
          content: aiText,
        };
        return updated;
      });
    });

    setLoading(false);
    speakText(aiText);
  };

  // 🎤 VOICE ASSISTANT (TOGGLE)
  const handleVoice = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported");
      return;
    }

    // STOP if already listening
    if (isListening && recognitionRef.current) {
      recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "en-US";
    setIsListening(true);

    recognition.onresult = async (event: any) => {
      const transcript = event.results[0][0].transcript;
      setIsListening(false);

      const userMessage = { role: "user", content: transcript };
      setMessages((prev: Message[]) => [...prev, userMessage]);

      let aiText = "";
      const aiIndex = messages.length + 1;

      setMessages((prev: Message[]) => [
        ...prev,
        { role: "ai", content: "" },
      ]);

      setLoading(true);

      await sendMessageStream(input, emotion, (chunk) => {
        aiText += chunk;

        setMessages((prev) => {
          const updated = [...prev];
          updated[aiIndex] = {
            role: "ai",
            content: aiText,
          };
          return updated;
        });
      });

      setLoading(false);
      speakText(aiText);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognition.start();
  };

  return (
    <div className="flex flex-col h-full w-full bg-gray-900 rounded-xl shadow-xl">
      
      {/* Header */}
      <div className="p-4 border-b border-gray-700 font-semibold">
        Clara AI Assistant
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`flex items-start gap-3 ${
              msg.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {msg.role === "ai" && (
              <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center text-sm">
                🤖
              </div>
            )}

            <div
              className={`px-4 py-2 rounded-xl max-w-[70%] ${
                msg.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-gray-700 text-gray-200"
              }`}
            >
              {msg.content}
            </div>

            {msg.role === "user" && (
              <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center text-sm">
                🧑
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="text-gray-400">
            🤖 Clara is typing...
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-gray-700 flex items-center gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your message..."
          className="flex-1 bg-gray-800 text-white p-2 rounded-lg outline-none"
        />

        {/* ⛔ STOP SPEAK */}
        <button
          onClick={stopSpeaking}
          className="bg-red-600 px-3 py-2 rounded-lg hover:bg-red-700"
        >
          ⛔
        </button>

        {/* 🎤 MIC TOGGLE */}
        <button
          onClick={handleVoice}
          className={`px-3 py-2 rounded-lg ${
            isListening ? "bg-red-600" : "bg-gray-700"
          }`}
        >
          {isListening ? "🛑" : "🎤"}
        </button>

        {/* SEND */}
        <button
          onClick={handleSend}
          className="bg-blue-600 px-4 py-2 rounded-lg hover:bg-blue-700"
        >
          Send
        </button>
      </div>
    </div>
  );
}