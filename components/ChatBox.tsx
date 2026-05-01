"use client";

import { useEffect, useRef, useState, useCallback } from "react";
import { sendChat, Patient } from "../utils/api";

type Props = {
  emotion: string;
  patient: Patient | null;
};

type Message = {
  id: string;
  sender: "user" | "ai";
  text: string;
  timestamp: Date;
};

type Language = "english" | "hindi" | "hinglish";

// ─── Voice Utilities ──────────────────────────────────────────────────────────
function getBestFemaleVoice(lang: Language): SpeechSynthesisVoice | null {
  if (typeof window === "undefined" || !window.speechSynthesis) return null;
  const voices = window.speechSynthesis.getVoices();
  const langCode = lang === "english" ? "en" : "hi";

  const femaleKeywords = [
    "female", "woman", "girl", "zira", "hazel", "samantha",
    "victoria", "karen", "moira", "tessa", "veena", "lekha",
    "kalpana", "heera", "google hindi female", "swara", "natural", "online"
  ];
    
  const maleKeywords = ["male", "man", "boy", "david", "mark", "ravi", "hemant", "madhur"];

  let voice = voices.find(
    (v) =>
      v.lang.toLowerCase().startsWith(langCode) &&
      v.name.toLowerCase().includes("google") &&
      femaleKeywords.some((k) => v.name.toLowerCase().includes(k)) &&
      !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
  );

  if (!voice) {
    voice = voices.find(
      (v) =>
        v.lang.toLowerCase().startsWith(langCode) &&
        femaleKeywords.some((k) => v.name.toLowerCase().includes(k)) &&
        !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  if (!voice && lang !== "english") {
    voice = voices.find((v) => 
      v.lang.toLowerCase().includes("hi") && 
      !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  if (!voice) {
    voice = voices.find((v) =>
      femaleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  return voice || (voices.length > 0 ? voices[0] : null);
}

function speakText(text: string, lang: Language) {
  if (typeof window === "undefined" || !window.speechSynthesis) return;

  // STRIP EMOJIS
  const cleanText = text.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD00-\uDDFF])/g, '');

  if (window.speechSynthesis.speaking) {
    window.speechSynthesis.cancel();
  }

  const utterance = new SpeechSynthesisUtterance(cleanText);
  const voice = getBestFemaleVoice(lang);

  if (voice) {
    utterance.voice = voice;
    utterance.lang = voice.lang;
  } else {
    utterance.lang = lang === "english" ? "en-US" : "hi-IN";
  }
  
  utterance.rate = 1.0;
  utterance.pitch = 1.05;
  utterance.volume = 1;
  
  // EDGE FIX: Speak after a tiny delay
  setTimeout(() => {
    window.speechSynthesis.speak(utterance);
  }, 10);
}

// ─── Emotion → accent color ───────────────────────────────────────────────────
const EMOTION_COLORS: Record<string, string> = {
  happy: "#F59E0B",
  sad: "#6366F1",
  anxious: "#EF4444",
  angry: "#DC2626",
  neutral: "#2F6F5E",
  surprised: "#8B5CF6",
  disgusted: "#65A30D",
  fearful: "#EA580C",
};

const EMOTION_EMOJI: Record<string, string> = {
  happy: "😊", sad: "🥺", anxious: "😟", angry: "😤",
  neutral: "😌", surprised: "😮", disgusted: "😣", fearful: "😨",
};

const GREETINGS: Record<Language, string[]> = {
  english: ["Hello! I'm Clara, your caring companion 💛 How are you feeling today?"],
  hindi: ["नमस्ते! मैं क्लारा हूँ, आपकी प्यारी साथी 💛 आज आप कैसा महसूस कर रहे हैं?"],
  hinglish: ["Namaste! Main Clara hoon, aapki pyaari saathi 💛 Aaj aap kaisa feel kar rahe hain?"],
};

export default function ChatBox({ emotion, patient }: Props) {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [thinking, setThinking] = useState(false);
  const [language, setLanguage] = useState<Language>("english");
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [voiceReady, setVoiceReady] = useState(false);
  
  const endRef = useRef<HTMLDivElement | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const accentColor = EMOTION_COLORS[emotion] || EMOTION_COLORS.neutral;

  useEffect(() => {
    if (typeof window !== "undefined" && window.speechSynthesis) {
      const initVoices = () => {
        const v = window.speechSynthesis.getVoices();
        if (v.length > 0) setVoiceReady(true);
      };
      initVoices();
      window.speechSynthesis.onvoiceschanged = initVoices;
    }
  }, []);

  useEffect(() => {
    const greetings = GREETINGS[language];
    const greeting = greetings[Math.floor(Math.random() * greetings.length)];
    setMessages([{ id: 'greet', sender: "ai", text: greeting, timestamp: new Date() }]);
  }, [language]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, thinking]);

  useEffect(() => {
    const interval = setInterval(() => {
      setIsSpeaking(window.speechSynthesis.speaking);
    }, 500);
    return () => clearInterval(interval);
  }, []);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || thinking) return;

    // BROWSER FIX: Pre-unlock speech engine on click
    const unlockUtterance = new SpeechSynthesisUtterance("");
    window.speechSynthesis.speak(unlockUtterance);

    setInput("");
    setMessages((prev) => [...prev, { id: Date.now().toString(), sender: "user", text, timestamp: new Date() }]);
    setThinking(true);

    try {
      const data = await sendChat({
        message: text,
        patient_id: patient?.id || 1,
        emotion,
        language,
      });

      const reply = data.response || data.reply || (language === "hindi" ? "Main yahaan hoon." : "I am here.");
      setMessages((prev) => [...prev, { id: (Date.now() + 1).toString(), sender: "ai", text: reply, timestamp: new Date() }]);
      
      // Delay to ensure the "unlock" finished
      setTimeout(() => speakText(reply, language), 50);
    } catch (err) {
      const reply = "Connection issue. I am still here.";
      setMessages((prev) => [...prev, { id: (Date.now() + 1).toString(), sender: "ai", text: reply, timestamp: new Date() }]);
      speakText(reply, language);
    } finally {
      setThinking(false);
    }
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setIsSpeaking(false);
  };

  return (
    <div className="h-full flex flex-col bg-[#F6F3EC]" style={{ fontFamily: "'Inter', sans-serif" }}>
      {/* Header */}
      <div className="flex items-center justify-between px-8 py-5 border-b-2 border-black/5">
        <div className="flex items-center gap-4">
          <div className="w-14 h-14 rounded-[1.5rem] bg-gradient-to-br from-[#21483F] to-[#2F6F5E] flex items-center justify-center text-3xl shadow-xl">👩</div>
          <div>
            <h2 className="text-2xl font-black text-[#21483F] tracking-tight">Clara</h2>
            <div className="flex items-center gap-2">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse shadow-[0_0_8px_rgba(34,197,94,0.5)]" />
              <p className="text-xs font-bold text-[#5F6F6B] uppercase tracking-widest">{patient?.name || "Care Mode"} • {emotion}</p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
           <div className={`px-4 py-2 rounded-2xl text-[10px] font-black uppercase tracking-widest ${voiceReady ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
             Voice: {voiceReady ? 'ACTIVE' : 'READYING...'}
           </div>
           <button 
             onClick={() => setLanguage(language === 'english' ? 'hindi' : 'english')}
             className="bg-[#21483F] text-white px-5 py-2 rounded-2xl font-black text-sm transition-all hover:scale-105 active:scale-95 shadow-lg"
           >
             {language === 'english' ? '🇬🇧 ENG' : '🇮🇳 HINDI'}
           </button>
           {isSpeaking && (
             <button onClick={stopSpeaking} className="bg-red-500 text-white px-5 py-2 rounded-2xl font-black text-sm shadow-lg animate-bounce">STOP VOICE</button>
           )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-8 py-6 space-y-6 custom-scrollbar">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
            <div className={`max-w-[80%] p-6 rounded-[2rem] shadow-sm relative group ${msg.sender === "user" ? "bg-[#21483F] text-white rounded-tr-none" : "bg-white text-[#21483F] rounded-tl-none border border-black/5"}`}>
              <p className="text-lg font-medium leading-relaxed">{msg.text}</p>
              <div className="mt-4 flex justify-between items-center opacity-40">
                <span className="text-[10px] font-bold uppercase tracking-widest">{msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                {msg.sender === 'ai' && (
                  <button onClick={() => speakText(msg.text, language)} className="text-[10px] font-black uppercase tracking-widest hover:text-[#2F6F5E] hover:opacity-100 transition-all">🔊 Re-Speak</button>
                )}
              </div>
            </div>
          </div>
        ))}
        {thinking && <div className="text-[#2F6F5E] font-black text-[10px] uppercase tracking-[0.3em] animate-pulse ml-4">Clara is thinking...</div>}
        <div ref={endRef} />
      </div>

      {/* Input */}
      <div className="p-8 bg-white border-t-2 border-black/5">
        <div className="max-w-4xl mx-auto flex gap-4">
          <input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder={language === 'hindi' ? "Apna message likhein..." : "Type your message..."}
            className="flex-1 bg-[#F6F3EC] border-2 border-transparent focus:border-[#2F6F5E]/30 rounded-[1.5rem] px-8 py-4 font-bold text-[#21483F] outline-none transition-all"
          />
          <button
            onClick={handleSend}
            disabled={thinking || !input.trim()}
            className="bg-[#21483F] hover:bg-[#2F6F5E] text-white px-10 py-4 rounded-[1.5rem] font-black shadow-xl transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-50"
          >
            {thinking ? "..." : "SEND"}
          </button>
        </div>
      </div>
    </div>
  );
}