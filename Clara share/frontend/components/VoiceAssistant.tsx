"use client";

import { useState, useRef, useEffect } from "react";
import { sendMessageStream } from "../utils/api";

type Language = "english" | "hindi";

function getBestFemaleVoice(lang: Language): SpeechSynthesisVoice | null {
  const voices = window.speechSynthesis.getVoices();
  const langCode = lang === "hindi" ? "hi" : "en";
  const femaleKeywords = [
    "female", "woman", "girl", "zira", "hazel", "samantha",
    "victoria", "karen", "moira", "tessa", "veena", "lekha",
    "kalpana", "heera", "google hindi female", "swara", "natural", "online"
  ];
  const maleKeywords = ["male", "man", "boy", "david", "mark", "ravi", "hemant", "madhur"];

  // 1. Try to find a high-quality Google female voice for the target language
  let voice = voices.find(
    (v) =>
      v.lang.toLowerCase().startsWith(langCode) &&
      v.name.toLowerCase().includes("google") &&
      femaleKeywords.some((k) => v.name.toLowerCase().includes(k)) &&
      !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
  );

  // 2. Try any strictly female voice for the target language
  if (!voice) {
    voice = voices.find(
      (v) =>
        v.lang.toLowerCase().startsWith(langCode) &&
        femaleKeywords.some((k) => v.name.toLowerCase().includes(k)) &&
        !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  // 3. Try any voice for the target language that is NOT known to be male
  if (!voice) {
    voice = voices.find((v) => 
      v.lang.toLowerCase().includes(langCode) && 
      !maleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  // 4. Try any explicitly female voice
  if (!voice) {
    voice = voices.find((v) =>
      femaleKeywords.some((k) => v.name.toLowerCase().includes(k))
    );
  }

  // 5. Any voice that is not explicitly male
  if (!voice) {
    voice = voices.find((v) => !maleKeywords.some((k) => v.name.toLowerCase().includes(k)));
  }

  return voice || (voices.length > 0 ? voices[0] : null);
}

function speakText(text: string, lang: Language, onEnd?: () => void) {
  window.speechSynthesis.cancel();
  
  // STRIP EMOJIS: Prevent the AI from saying "Yellow Heart" etc.
  const cleanText = text.replace(/([\u2700-\u27BF]|[\uE000-\uF8FF]|\uD83C[\uDC00-\uDFFF]|\uD83D[\uDC00-\uDFFF]|[\u2011-\u26FF]|\uD83E[\uDD00-\uDDFF])/g, '');

  // A small delay helps some browsers (Chrome/Edge) recover from the cancel()
  setTimeout(() => {
    const trySpeak = () => {
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
      if (onEnd) utterance.onend = onEnd;
      window.speechSynthesis.speak(utterance);
    };

    if (window.speechSynthesis.getVoices().length === 0) {
      window.speechSynthesis.addEventListener("voiceschanged", trySpeak, { once: true });
    } else {
      trySpeak();
    }
  }, 100);
}

export default function VoiceAssistant({ emotion }: { emotion: string }) {
  const [status, setStatus] = useState<"idle" | "listening" | "thinking" | "speaking">("idle");
  const [transcript, setTranscript] = useState("");
  const [reply, setReply] = useState("");
  const [language, setLanguage] = useState<Language>("english");
  const [pulseSize, setPulseSize] = useState(1);
  const recognitionRef = useRef<any>(null);
  const pulseRef = useRef<NodeJS.Timeout | null>(null);

  // Animate mic pulse when listening
  useEffect(() => {
    if (status === "listening") {
      pulseRef.current = setInterval(() => {
        setPulseSize((p) => (p === 1 ? 1.15 : 1));
      }, 600);
    } else {
      if (pulseRef.current) clearInterval(pulseRef.current);
      setPulseSize(1);
    }
    return () => { if (pulseRef.current) clearInterval(pulseRef.current); };
  }, [status]);

  const startListening = () => {
    const SpeechRecognition =
      (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognition) {
      alert("Voice input not supported. Please use Chrome or Edge.");
      return;
    }

    if (status === "listening" && recognitionRef.current) {
      recognitionRef.current.stop();
      setStatus("idle");
      return;
    }

    const recognition = new SpeechRecognition();
    recognitionRef.current = recognition;
    recognition.lang = language === "hindi" ? "hi-IN" : "en-US";
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    setStatus("listening");
    setTranscript("");
    setReply("");

    recognition.onstart = () => {
      console.log("Voice recognition started");
    };

    recognition.onresult = async (event: any) => {
      const text = event.results[0][0].transcript;
      setTranscript(text);
      setStatus("thinking");

      try {
        const response = await sendMessageStream({
          message: text,
          emotion,
          patient_id: 1,
          language,
        });

        const aiText =
          response.reply ||
          response.response ||
          (language === "hindi"
            ? "Main yahaan hoon aapke saath. 💛"
            : "I am right here with you. 💛");

        setReply(aiText);
        setStatus("speaking");
        speakText(aiText, language, () => setStatus("idle"));
      } catch (err: any) {
        const fallback =
          language === "hindi"
            ? "Abhi connection mein thodi problem hai. Main yahaan hoon. 💛"
            : "Connection issue right now, but I'm still here with you. 💛";
        setReply(fallback);
        setStatus("speaking");
        speakText(fallback, language, () => setStatus("idle"));
      }
    };

    recognition.onerror = (event: any) => {
      // Use console.warn instead of console.error to prevent Next.js dev overlay
      if (event.error === 'no-speech' || event.error === 'network') {
        console.warn("Speech recognition notice:", event.error);
        setStatus("idle");
        return;
      }
      
      console.error("Speech recognition critical error:", event.error);
      if (event.error === 'not-allowed') {
        alert("Microphone access blocked. Please allow mic access in your browser settings.");
      } else {
        alert("Voice recognition error: " + event.error);
      }
      setStatus("idle");
    };
    recognition.onend = () => {
      console.log("Voice recognition ended");
      if (status === "listening") setStatus("idle");
    };

    try {
      recognition.start();
    } catch (err) {
      console.error("Speech recognition start error:", err);
      setStatus("idle");
    }
  };

  const stopSpeaking = () => {
    window.speechSynthesis.cancel();
    setStatus("idle");
  };

  const toggleLanguage = () =>
    setLanguage((prev) => (prev === "english" ? "hindi" : "english"));

  const statusConfig = {
    idle: {
      label: language === "hindi" ? "बोलने के लिए माइक दबाएं 🎤" : "Tap the mic to speak 🎤",
      color: "#2F6F5E",
      bg: "linear-gradient(135deg, #2F6F5E22, #EAF3EF)",
    },
    listening: {
      label: language === "hindi" ? "सुन रही हूँ... बोलिए! 👂" : "Listening... speak now! 👂",
      color: "#EF4444",
      bg: "linear-gradient(135deg, #EF444422, #FFF0F0)",
    },
    thinking: {
      label: language === "hindi" ? "Clara सोच रही है... 💭" : "Clara is thinking... 💭",
      color: "#F59E0B",
      bg: "linear-gradient(135deg, #F59E0B22, #FFFBEB)",
    },
    speaking: {
      label: language === "hindi" ? "Clara बोल रही है 🗣️" : "Clara is speaking 🗣️",
      color: "#6366F1",
      bg: "linear-gradient(135deg, #6366F122, #EEF2FF)",
    },
  };

  const cfg = statusConfig[status];

  return (
    <div
      className="h-full rounded-3xl flex flex-col items-center justify-center p-8 transition-all duration-700 relative overflow-hidden"
      style={{ background: cfg.bg, fontFamily: "'Inter', 'Segoe UI', sans-serif" }}
    >
      {/* Absolute Stop Button for visibility */}
      {status === "speaking" && (
        <button
          onClick={stopSpeaking}
          className="absolute top-6 right-6 px-4 py-2 rounded-xl font-bold text-white text-xs transition-all hover:scale-105 active:scale-95 shadow-lg flex items-center gap-2 z-50"
          style={{ background: "linear-gradient(135deg, #EF4444, #DC2626)" }}
        >
          🔇 Stop
        </button>
      )}
      {/* Clara avatar */}
      <div
        className="w-24 h-24 rounded-full flex items-center justify-center text-5xl mb-6 shadow-xl"
        style={{
          background: `linear-gradient(135deg, ${cfg.color}, #1a4a3c)`,
          boxShadow: `0 8px 32px ${cfg.color}44`,
          transition: "all 0.4s ease",
        }}
      >
        🙋‍♀️
      </div>

      <h2
        className="text-2xl font-extrabold mb-2 text-center"
        style={{ color: cfg.color, transition: "color 0.4s" }}
      >
        Clara Voice Support
      </h2>

      {/* Status label */}
      <p
        className="text-base font-semibold mb-8 text-center px-4"
        style={{ color: cfg.color, opacity: 0.85 }}
      >
        {cfg.label}
      </p>

      {/* Language toggle */}
      <button
        onClick={toggleLanguage}
        className="mb-6 px-5 py-2 rounded-full font-bold text-sm text-white transition-all hover:scale-105 active:scale-95 shadow-md"
        style={{
          background: language === "hindi"
            ? "linear-gradient(135deg, #FF9933, #FF6600)"
            : "linear-gradient(135deg, #2F6F5E, #1a4a3c)",
        }}
      >
        {language === "hindi" ? "🇮🇳 हिंदी में बात करें" : "🇬🇧 Speak in English"}
      </button>

      {/* Voice Diagnostic */}
      <button
        onClick={() => {
          const v = getBestFemaleVoice(language);
          const allVoices = window.speechSynthesis.getVoices();
          const hiVoices = allVoices.filter(v => v.lang.includes("hi"));
          if (v) {
            alert(`Voice Found: ${v.name}\nTotal Hindi Voices: ${hiVoices.length}\n${hiVoices.length === 0 ? "WARNING: Your system has NO Hindi voices installed. Please check OS settings." : ""}`);
            speakText(language === "hindi" ? "नमस्ते, मैं आपकी आवाज़ चेक कर रही हूँ।" : "Hello, I am testing the voice.", language);
          } else {
            alert("No suitable voice found. Please check browser settings.");
          }
        }}
        className="mb-6 text-xs text-[#5F6F6B] underline hover:text-[#21483F] transition-colors"
      >
        Diagnostic: Test Voice Engine
      </button>

      {/* Microphone button */}
      <div className="relative mb-8">
        {/* Pulse rings when listening */}
        {status === "listening" && (
          <>
            <div
              className="absolute inset-0 rounded-full"
              style={{
                background: "#EF444433",
                animation: "ring 1.5s ease-out infinite",
              }}
            />
            <div
              className="absolute inset-0 rounded-full"
              style={{
                background: "#EF444422",
                animation: "ring 1.5s 0.5s ease-out infinite",
              }}
            />
          </>
        )}
        <button
          onClick={startListening}
          disabled={status === "thinking" || status === "speaking"}
          className="w-36 h-36 rounded-full flex items-center justify-center text-6xl transition-all hover:scale-105 active:scale-95 shadow-2xl relative z-10"
          style={{
            background:
              status === "listening"
                ? "linear-gradient(135deg, #EF4444, #DC2626)"
                : status === "thinking"
                ? "linear-gradient(135deg, #F59E0B, #D97706)"
                : status === "speaking"
                ? "linear-gradient(135deg, #6366F1, #4F46E5)"
                : `linear-gradient(135deg, ${cfg.color}, #1a4a3c)`,
            boxShadow: `0 12px 40px ${cfg.color}55`,
            transform: `scale(${pulseSize})`,
            transition: "transform 0.4s ease, background 0.4s ease",
            cursor:
              status === "thinking" || status === "speaking"
                ? "not-allowed"
                : "pointer",
          }}
        >
          {status === "listening" ? "🔴" : status === "thinking" ? "⏳" : status === "speaking" ? "🔊" : "🎤"}
        </button>
      </div>

      {/* Transcript */}
      {transcript && (
        <div
          className="w-full max-w-md px-5 py-3 rounded-2xl mb-3 text-center"
          style={{
            background: "white",
            border: "2px solid #D8E7E0",
            boxShadow: "0 2px 10px rgba(0,0,0,0.06)",
          }}
        >
          <p className="text-xs font-bold text-[#5F6F6B] mb-1 uppercase tracking-wide">
            {language === "hindi" ? "आपने कहा" : "You said"}
          </p>
          <p className="text-[#21483F] font-medium">{transcript}</p>
        </div>
      )}

      {/* Reply */}
      {reply && (
        <div
          className="w-full max-w-md px-5 py-3 rounded-2xl text-center"
          style={{
            background: `linear-gradient(135deg, ${cfg.color}18, white)`,
            border: `2px solid ${cfg.color}33`,
            boxShadow: `0 4px 16px ${cfg.color}22`,
          }}
        >
          <p className="text-xs font-bold mb-1 uppercase tracking-wide" style={{ color: cfg.color }}>
            {language === "hindi" ? "Clara ने कहा" : "Clara said"}
          </p>
          <p className="text-[#21483F] font-medium leading-relaxed">{reply}</p>
        </div>
      )}

      {/* Stop speaking button */}
      {status === "speaking" && (
        <button
          onClick={stopSpeaking}
          className="mt-5 px-6 py-3 rounded-2xl font-bold text-white text-sm transition-all hover:scale-105 active:scale-95 shadow-lg"
          style={{ background: "linear-gradient(135deg, #EF4444, #DC2626)" }}
        >
          🔇 {language === "hindi" ? "रोकें" : "Stop Speaking"}
        </button>
      )}

      <style>{`
        @keyframes ring {
          0% { transform: scale(1); opacity: 0.6; }
          100% { transform: scale(2.2); opacity: 0; }
        }
      `}</style>
    </div>
  );
}