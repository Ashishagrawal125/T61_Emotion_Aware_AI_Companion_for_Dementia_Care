"use client";

import { useState, useRef } from "react";
import { sendMessageStream } from "../utils/api";

type Status = "idle" | "listening" | "thinking" | "speaking";

export default function VoiceAssistant({ emotion }: { emotion: string }) {
  const [status, setStatus] = useState<Status>("idle");
  const [lastUser, setLastUser] = useState("");
  const [lastAI, setLastAI] = useState("");

  const recognitionRef = useRef<any>(null);

  // 🔊 Speak text (with interrupt)
  const speakText = (text: string) => {
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = "en-US";
    u.rate = 1;
    u.onstart = () => setStatus("speaking");
    u.onend = () => setStatus("idle");
    window.speechSynthesis.speak(u);
  };

  // ⛔ Stop speaking
  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setStatus("idle");
  };

  // 🎤 Start / Stop listening
  const toggleMic = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition ||
      (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Speech Recognition not supported (use Chrome/Edge)");
      return;
    }

    // If currently listening → stop
    if (status === "listening" && recognitionRef.current) {
      recognitionRef.current.stop();
      setStatus("idle");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;

    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    setStatus("listening");

    recognition.onresult = async (event: any) => {
      const transcript = event.results[0][0].transcript;
      setLastUser(transcript);
      setStatus("thinking");

      // Stream AI response
      let aiText = "";
      await sendMessageStream(transcript, emotion, (chunk) => {
        aiText += chunk;
        setLastAI(aiText);
      });

      // Speak after streaming ends
      speakText(aiText);
    };

    recognition.onerror = () => setStatus("idle");
    recognition.onend = () => {
      // If ended without result, reset
      if (status === "listening") setStatus("idle");
    };

    recognition.start();
  };

  // UI helpers
  const statusText =
    status === "idle"
      ? "Tap the mic to start"
      : status === "listening"
      ? "Listening…"
      : status === "thinking"
      ? "Thinking…"
      : "Speaking…";

  const micColor =
    status === "listening"
      ? "bg-red-600"
      : status === "thinking"
      ? "bg-yellow-500"
      : status === "speaking"
      ? "bg-green-600"
      : "bg-gray-700";

  return (
    <div className="flex flex-col items-center justify-center h-full text-white">
      <div className="text-xl mb-6">{statusText}</div>

      {/* Big Mic */}
      <button
        onClick={toggleMic}
        className={`w-28 h-28 rounded-full flex items-center justify-center text-4xl ${micColor} hover:scale-105 transition`}
      >
        {status === "listening" ? "🛑" : "🎤"}
      </button>

      {/* Stop Speech */}
      <button
        onClick={stopSpeaking}
        className="mt-4 bg-red-700 px-4 py-2 rounded-lg hover:bg-red-800"
      >
        ⛔ Stop Speaking
      </button>

      {/* Live transcripts */}
      <div className="mt-8 max-w-xl text-center space-y-3">
        {lastUser && (
          <div className="text-gray-300">
            <span className="opacity-60">You:</span> {lastUser}
          </div>
        )}
        {lastAI && (
          <div className="text-white">
            <span className="opacity-60">Clara:</span> {lastAI}
          </div>
        )}
      </div>
    </div>
  );
}