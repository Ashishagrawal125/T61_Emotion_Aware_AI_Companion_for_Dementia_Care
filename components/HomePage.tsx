"use client";

import { useState, useEffect } from "react";

type HomePageProps = {
  onStart: (mode: string) => void;
};

const FEATURE_CARDS = [
  {
    icon: "💬",
    title: "Smart Chat",
    desc: "Empathetic, memory-aware conversations in English, Hindi, and Hinglish.",
    color: "#2F6F5E",
  },
  {
    icon: "🎤",
    title: "Voice Support",
    desc: "Hands-free interaction with natural, high-quality voice synthesis.",
    color: "#6366F1",
  },
  {
    icon: "🧠",
    title: "Cognitive Memory",
    desc: "Clara remembers names, hobbies, and routines for a personal bond.",
    color: "#F59E0B",
  },
  {
    icon: "⚖️",
    title: "Emotion Radar",
    desc: "Real-time AI analysis of stress, anxiety, and panic states.",
    color: "#EF4444",
  },
];

const TIPS = [
  "\"You are safe here, and I am always with you.\"",
  "\"Main yahaan hoon — aap bilkul akele nahi hain.\"",
  "\"I remember your favorite flowers were roses. 🌹\"",
  "\"Let's listen to your favorite song together. 🎵\"",
];

export default function HomePage({ onStart }: HomePageProps) {
  const [tipIndex, setTipIndex] = useState(0);
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(false);
      setTimeout(() => {
        setTipIndex((i) => (i + 1) % TIPS.length);
        setVisible(true);
      }, 500);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="h-full overflow-y-auto bg-[#F6F3EC] p-6 md:p-12 font-sans relative">
      {/* Background Gradients */}
      <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-[#2F6F5E]/5 rounded-full blur-[100px] pointer-events-none" />
      <div className="fixed bottom-0 left-0 w-[400px] h-[400px] bg-[#F59E0B]/5 rounded-full blur-[80px] pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        
        {/* Hero Section */}
        <div className="text-center mb-16">
          <div className="relative inline-block mb-8 group">
            <div className="absolute inset-0 bg-[#2F6F5E]/20 rounded-full blur-2xl group-hover:scale-125 transition-transform duration-1000 animate-pulse" />
            <div className="w-28 h-28 bg-gradient-to-br from-[#21483F] to-[#2F6F5E] rounded-full flex items-center justify-center text-5xl shadow-2xl relative border-4 border-white">
              👩
            </div>
            <div className="absolute -bottom-2 -right-2 bg-white px-3 py-1 rounded-full shadow-md flex items-center gap-1">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-ping" />
              <span className="text-[10px] font-bold text-[#21483F]">ONLINE</span>
            </div>
          </div>

          <h1 className="text-6xl font-black text-[#21483F] tracking-tighter mb-4 leading-tight">
            I am <span className="text-[#2F6F5E]">Clara</span>,<br/>your digital companion.
          </h1>
          
          <div className={`transition-opacity duration-500 text-xl font-medium text-[#5F6F6B] italic h-8 mb-12 ${visible ? 'opacity-100' : 'opacity-0'}`}>
            {TIPS[tipIndex]}
          </div>

          <div className="flex flex-wrap justify-center gap-6">
            <button
              onClick={() => onStart("chat")}
              className="bg-[#21483F] text-white px-10 py-5 rounded-[2rem] font-bold text-lg shadow-2xl transition-all hover:scale-105 active:scale-95 flex items-center gap-3 hover:bg-[#2F6F5E]"
            >
              💬 Start Comfort Chat
            </button>
            <button
              onClick={() => onStart("voice")}
              className="bg-white border-2 border-[#E3DDD2] text-[#21483F] px-10 py-5 rounded-[2rem] font-bold text-lg shadow-xl transition-all hover:scale-105 active:scale-95 flex items-center gap-3 hover:bg-[#F6F3EC]"
            >
              🎤 Voice Support
            </button>
          </div>
        </div>

        {/* Intelligence Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-16">
          <StatBox label="Intelligence" value="GPT-4o / Groq" color="#2F6F5E" />
          <StatBox label="Languages" value="Hindi & English" color="#6366F1" />
          <StatBox label="Response" value="< 2.5 Seconds" color="#F59E0B" />
        </div>

        {/* Feature Grid */}
        <div className="mb-16">
          <h2 className="text-xs font-black text-[#21483F]/40 uppercase tracking-[0.3em] mb-8 text-center">System Capabilities</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {FEATURE_CARDS.map((card, i) => (
              <div 
                key={i} 
                className="bg-white/60 backdrop-blur-md border border-white p-8 rounded-[2.5rem] shadow-lg transition-all hover:scale-[1.03] hover:shadow-2xl group"
                style={{ borderBottom: `4px solid ${card.color}22` }}
              >
                <div className="text-4xl mb-6 transition-transform group-hover:scale-110 duration-300">{card.icon}</div>
                <h3 className="text-lg font-black text-[#21483F] mb-3">{card.title}</h3>
                <p className="text-sm text-[#5F6F6B] leading-relaxed font-medium">{card.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Trust Footer */}
        <div className="bg-[#21483F] rounded-[3rem] p-12 text-white flex flex-col md:flex-row items-center justify-between gap-8 shadow-2xl relative overflow-hidden">
          <div className="relative z-10">
            <h3 className="text-3xl font-black mb-2">Designed for Dementia</h3>
            <p className="text-white/70 max-w-md font-medium leading-relaxed">
              Every pixel and interaction is optimized for patients over 50. Large fonts, warm colors, and a patient AI that never gets tired.
            </p>
          </div>
          <div className="relative z-10 flex gap-4">
             <div className="bg-white/10 px-6 py-4 rounded-3xl border border-white/20 text-center">
                <p className="text-xs font-bold opacity-60 mb-1">ACCURACY</p>
                <p className="text-2xl font-black">98%</p>
             </div>
             <div className="bg-white/10 px-6 py-4 rounded-3xl border border-white/20 text-center">
                <p className="text-xs font-bold opacity-60 mb-1">AVAILABILITY</p>
                <p className="text-2xl font-black">24/7</p>
             </div>
          </div>
          <div className="absolute -right-20 -bottom-20 w-80 h-80 bg-white/5 rounded-full blur-3xl" />
        </div>
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
        body { font-family: 'Inter', sans-serif; }
      `}</style>
    </div>
  );
}

function StatBox({ label, value, color }: any) {
  return (
    <div className="bg-white/50 backdrop-blur-sm border border-white p-6 rounded-[2rem] shadow-sm text-center">
      <p className="text-[10px] font-black uppercase tracking-widest mb-1" style={{ color }}>{label}</p>
      <p className="text-xl font-black text-[#21483F]">{value}</p>
    </div>
  );
}