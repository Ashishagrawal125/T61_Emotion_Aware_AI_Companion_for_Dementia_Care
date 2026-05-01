"use client";

import { useEffect, useState } from "react";
import LoginPage from "../components/LoginPage";
import ChatBox from "../components/ChatBox";
import VoiceAssistant from "../components/VoiceAssistant";
import EmotionCamera from "../components/EmotionCamera";
import PatientPanel from "../components/PatientPanel";
import CaregiverDashboard from "../components/CaregiverDashboard";
import HomePage from "../components/HomePage";
import { getPatients, Patient } from "../utils/api";

type Tab = "home" | "patients" | "chat" | "voice" | "emotion" | "dashboard";

export default function Home() {
  const [caregiver, setCaregiver] = useState<any>(null);
  const [active, setActive] = useState<Tab>("home");
  const [emotion, setEmotion] = useState("neutral");
  const [selectedPatient, setSelectedPatient] = useState<Patient | null>(null);
  const [dashboardKey, setDashboardKey] = useState(0);

  useEffect(() => {
    const saved = localStorage.getItem("caregiver");
    if (saved) setCaregiver(JSON.parse(saved));
  }, []);

  useEffect(() => {
    async function loadPatients() {
      try {
        const patients = await getPatients();
        if (patients.length > 0) {
          setSelectedPatient(patients[0]);
        }
      } catch {
        console.log("Backend not connected");
      }
    }
    if (caregiver) loadPatients();
  }, [caregiver]);

  if (!caregiver) {
    return <LoginPage onLogin={setCaregiver} />;
  }

  const allNavItems: { key: Tab; label: string; icon: string }[] = [
    { key: "home", label: "Home", icon: "🏠" },
    { key: "patients", label: "Patient Profiles", icon: "👤" },
    { key: "chat", label: "Comfort Chat", icon: "💬" },
    { key: "voice", label: "Voice Support", icon: "🎤" },
    { key: "emotion", label: "Emotion Check", icon: "⚖️" },
    { key: "dashboard", label: "Care Intelligence", icon: "📊" },
  ];

  const navItems = allNavItems.filter((item) => {
    if (caregiver?.role === "patient") {
      return ["home", "chat", "voice", "emotion"].includes(item.key);
    }
    return true; // Caregiver, Doctor, Family see everything
  });

  return (
    <main className="h-screen bg-[#F6F3EC] text-[#24312F] overflow-hidden flex font-sans">
      
      {/* Premium Sidebar (Hidden on Mobile) */}
      <aside className="hidden lg:flex w-80 bg-gradient-to-b from-[#21483F] to-[#2F6F5E] p-8 flex-col shadow-2xl relative overflow-hidden shrink-0">
        <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
          <div className="absolute -top-20 -left-20 w-64 h-64 bg-white rounded-full blur-3xl" />
        </div>

        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-10">
             <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center text-xl shadow-lg">👩</div>
             <h1 className="text-3xl font-black text-white tracking-tighter">Clara AI</h1>
          </div>

          <div className="bg-white/10 backdrop-blur-md rounded-3xl p-5 border border-white/10 mb-8 transition-all hover:bg-white/15">
            <p className="text-[10px] font-black text-white/50 uppercase tracking-widest mb-1">{caregiver.role || "User"}</p>
            <h2 className="text-xl font-bold text-white truncate">{caregiver.name}</h2>
            <button
              onClick={() => { localStorage.clear(); setCaregiver(null); }}
              className="mt-4 text-[10px] font-black text-white/60 hover:text-white uppercase tracking-widest transition-colors"
            >
              Sign Out →
            </button>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => (
              <button
                key={item.key}
                onClick={() => setActive(item.key)}
                className={`w-full flex items-center gap-4 px-6 py-4 rounded-2xl font-bold transition-all ${
                  active === item.key
                    ? "bg-white text-[#21483F] shadow-xl translate-x-2"
                    : "text-white/70 hover:text-white hover:bg-white/5"
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                <span className="text-sm">{item.label}</span>
              </button>
            ))}
          </nav>
        </div>

        <div className="mt-auto relative z-10 pt-8 border-t border-white/10">
           <p className="text-[10px] font-black text-white/40 uppercase tracking-widest mb-3">Live Status</p>
           <div className="bg-white/10 rounded-2xl p-4 flex items-center justify-between">
              <span className="text-xs font-bold text-white capitalize">{emotion}</span>
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse shadow-[0_0_10px_rgba(74,222,128,0.5)]" />
           </div>
        </div>
      </aside>

      {/* Content Area */}
      <section className="flex-1 flex flex-col overflow-hidden relative">
        <header className="bg-white/80 backdrop-blur-md border-b border-[#E3DDD2] px-10 py-6 flex justify-between items-center z-20">
          <div>
            <h2 className="text-2xl font-black text-[#21483F] tracking-tight">
              {navItems.find(n => n.key === active)?.label}
            </h2>
            <div className="flex items-center gap-3 mt-1">
               <span className="flex items-center gap-1.5 text-[10px] font-black text-[#10B981] uppercase tracking-wider">
                  <span className="w-1.5 h-1.5 bg-[#10B981] rounded-full" />
                  Neural Link Active
               </span>
               <span className="text-[10px] font-bold text-[#5F6F6B] uppercase tracking-wider opacity-40">•</span>
               <span className="text-[10px] font-bold text-[#5F6F6B] uppercase tracking-wider">
                  Patient: {selectedPatient?.name || "None"}
               </span>
            </div>
          </div>

          <button
            onClick={() => setDashboardKey((k) => k + 1)}
            className="w-12 h-12 bg-[#F6F3EC] rounded-2xl flex items-center justify-center text-xl transition-all hover:scale-110 active:scale-95 shadow-sm border border-white"
            title="Sync Data"
          >
            🔄
          </button>
        </header>

        <div className="flex-1 overflow-hidden pb-20 lg:pb-0">
          {active === "home" && (
            <HomePage onStart={(mode) => setActive(mode as Tab)} />
          )}

          {active === "patients" && (
            <PatientPanel
              selectedPatientId={selectedPatient?.id || null}
              onSelect={setSelectedPatient}
            />
          )}

          {active === "chat" && (
            <ChatBox emotion={emotion} patient={selectedPatient} />
          )}

          {active === "voice" && <VoiceAssistant emotion={emotion} />}

          {active === "emotion" && (
            <EmotionCamera
              patient={selectedPatient}
              onDetect={setEmotion}
              onDashboardRefresh={() => setDashboardKey((k) => k + 1)}
            />
          )}

          {active === "dashboard" && (
            <CaregiverDashboard key={dashboardKey} patient={selectedPatient} />
          )}
        </div>

        {/* Mobile Bottom Navigation */}
        <nav className="lg:hidden fixed bottom-0 left-0 w-full bg-white border-t border-[#E3DDD2] flex justify-around p-3 z-30 shadow-[0_-10px_30px_rgba(0,0,0,0.05)]">
          {navItems.map((item) => (
            <button
              key={item.key}
              onClick={() => setActive(item.key)}
              className={`flex flex-col items-center gap-1 transition-all ${
                active === item.key ? "text-[#2F6F5E] scale-110" : "text-[#5F6F6B] opacity-50"
              }`}
            >
              <span className="text-2xl">{item.icon}</span>
              <span className="text-[8px] font-black uppercase tracking-tighter">{item.label.split(' ')[0]}</span>
            </button>
          ))}
          <button
            onClick={() => { localStorage.clear(); setCaregiver(null); }}
            className="flex flex-col items-center gap-1 text-red-400 opacity-50"
          >
            <span className="text-2xl">🚪</span>
            <span className="text-[8px] font-black uppercase tracking-tighter">Exit</span>
          </button>
        </nav>
      </section>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(33, 72, 63, 0.1); border-radius: 10px; }
      `}</style>
    </main>
  );
}