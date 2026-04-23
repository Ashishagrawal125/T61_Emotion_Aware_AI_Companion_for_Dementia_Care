"use client";

import ChatBox from "../components/ChatBox";
import VoiceAssistant from "../components/VoiceAssistant";
import EmotionCamera from "../components/EmotionCamera";
import EmotionDashboard from "../components/EmotionDashboard";
import HomePage from "../components/HomePage";
import { useState } from "react";

export default function Home() {
  const [isHome, setIsHome] = useState(true);
  const [active, setActive] = useState("chat");
  const [emotion, setEmotion] = useState("neutral");
  const [emotionHistory, setEmotionHistory] = useState<string[]>([]);

  return (
    <div className="flex h-screen bg-gradient-to-br from-black to-gray-900 text-white">

      {/* Sidebar */}
      <div className="w-64 bg-gray-950 p-5 border-r border-gray-800 flex flex-col">
        <h1 className="text-2xl font-bold mb-8">Clara AI</h1>

        <div className="space-y-3">
          <button
            onClick={() => {
              setActive("chat");
              setIsHome(false);
            }}
            className={`w-full text-left px-4 py-2 rounded-lg hover:bg-gray-800 ${
              active === "chat" ? "bg-gray-800" : ""
            }`}
          >
            💬 Chat
          </button>

          <button
            onClick={() => {
              setActive("voice");
              setIsHome(false);
            }}
            className={`w-full text-left px-4 py-2 rounded-lg hover:bg-gray-800 ${
              active === "voice" ? "bg-gray-800" : ""
            }`}
          >
            🎤 Voice
          </button>

          <button
            onClick={() => {
              setActive("emotion");
              setIsHome(false);
            }}
            className={`w-full text-left px-4 py-2 rounded-lg hover:bg-gray-800 ${
              active === "emotion" ? "bg-gray-800" : ""
            }`}
          >
            😊 Emotion
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col">

        {/* Top Bar */}
<div className="p-4 border-b border-gray-800 flex justify-between items-center">

  {/* Title */}
  <div className="text-lg font-semibold">
    {isHome && "Welcome to Clara AI"}
    {!isHome && active === "chat" && "Chat Assistant"}
    {!isHome && active === "voice" && "Voice Assistant"}
    {!isHome && active === "emotion" && "Emotion Detection"}
  </div>

  {/* RIGHT SIDE */}
  <div className="flex items-center gap-3">

    {/* 🔥 HOME BUTTON */}
    {!isHome && (
      <button
        onClick={() => setIsHome(true)}
        className="bg-gray-700 px-3 py-1 rounded-lg hover:bg-gray-600 text-sm"
      >
        🏠 Home
      </button>
    )}

    {/* Emotion Badge */}
    {!isHome && (
      <div className="px-3 py-1 rounded-full bg-gray-800 text-sm">
        {emotion === "happy" && "😊 Happy"}
        {emotion === "sad" && "😢 Sad"}
        {emotion === "angry" && "😡 Angry"}
        {emotion === "neutral" && "😐 Neutral"}
      </div>
    )}

  </div>

</div>

        {/* Content */}
        <div className="flex-1 p-4 overflow-hidden">

          {/* 🏠 Home Page */}
          {isHome ? (
            <HomePage
              onStart={(mode: string) => {
                setActive(mode);
                setIsHome(false);
              }}
            />
          ) : (
            <>
              {active === "chat" && <ChatBox emotion={emotion} />}
              {active === "voice" && <VoiceAssistant emotion={emotion} />}
              {active === "emotion" && (
                <div className="grid grid-cols-2 gap-4 h-full">
                  <EmotionCamera
                    onDetect={(e: string) => {
                      setEmotion(e);
                      setEmotionHistory((prev) => [...prev.slice(-20), e]);
                    }}
                  />
                  <EmotionDashboard history={emotionHistory} />
                </div>
              )}
            </>
          )}

        </div>
      </div>
    </div>
  );
}