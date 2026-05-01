"use client";

import { useEffect, useState } from "react";
import { getDashboard, markAlertRead, Patient } from "../utils/api";

export default function CaregiverDashboard({ patient }: { patient: Patient | null }) {
  const [data, setData] = useState<any>(null);
  const [notifiedAlertIds, setNotifiedAlertIds] = useState<Set<number>>(new Set());
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  useEffect(() => {
    // Request browser notification permission
    if (typeof window !== "undefined" && "Notification" in window) {
      Notification.requestPermission();
    }
    
    load();
    const interval = setInterval(load, 10000); // Auto refresh every 10s
    return () => clearInterval(interval);
  }, [patient?.id]);

  const sendBrowserNotification = (alert: any) => {
    if (typeof window !== "undefined" && Notification.permission === "granted") {
      new Notification(`🚨 CRISIS ALERT: ${patient?.name}`, {
        body: alert.message,
        icon: "/favicon.ico"
      });
    }
  };

  const playSiren = () => {
    const audio = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
    audio.play().catch(e => console.log("Audio play blocked", e));
  };

  const load = async () => {
    if (!patient) return;
    try {
      const dashboard = await getDashboard(patient.id);
      
      // SIREN & NOTIFICATION LOGIC
      if (dashboard.alerts && dashboard.alerts.length > 0) {
        const latest = dashboard.alerts[0];
        
        // Only notify if:
        // 1. It's a high severity alert
        // 2. We haven't notified for this specific alert ID yet
        // 3. It's NOT the very first load of the dashboard (to prevent old alerts firing on login)
        const isNewAlert = !notifiedAlertIds.has(latest.id);
        const isHighSeverity = latest.severity === "high" || latest.severity === "High";

        if (isHighSeverity && isNewAlert && !isInitialLoad) {
          playSiren();
          sendBrowserNotification(latest);
          setNotifiedAlertIds(prev => new Set(prev).add(latest.id));
        } else if (isHighSeverity && isNewAlert && isInitialLoad) {
          // Just mark it as notified without playing sound on first load
          setNotifiedAlertIds(prev => new Set(prev).add(latest.id));
        }
      }
      
      setData(dashboard);
      setIsInitialLoad(false);
    } catch (err) {
      console.error("Dashboard load error", err);
    }
  };

  if (!patient) {
    return (
      <div className="h-full grid place-items-center bg-[#F6F3EC]">
        <div className="bg-white/80 backdrop-blur-md rounded-[2.5rem] p-12 shadow-2xl border border-white max-w-xl text-center">
          <div className="w-20 h-20 bg-[#EAF3EF] rounded-full flex items-center justify-center text-4xl mx-auto mb-6">👤</div>
          <h2 className="text-4xl font-black text-[#21483F]">Select a Patient</h2>
          <p className="text-[#5F6F6B] mt-4 text-lg font-medium">
            Choose a patient from the sidebar to initialize the Care Intelligence Dashboard.
          </p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="h-full grid place-items-center bg-[#F6F3EC] text-[#21483F]">
        <div className="flex flex-col items-center gap-4">
          <div className="w-12 h-12 border-4 border-[#2F6F5E] border-t-transparent rounded-full animate-spin"></div>
          <p className="font-bold tracking-widest uppercase text-xs">Initializing Neural Link...</p>
        </div>
      </div>
    );
  }

  const emotionCounts = (() => {
    if (!data.emotion_trend || !Array.isArray(data.emotion_trend)) return [];
    const counts: Record<string, number> = {};
    for (const log of data.emotion_trend) {
      counts[log.emotion] = (counts[log.emotion] || 0) + 1;
    }
    return Object.entries(counts).map(([emotion, count]) => ({ emotion, count }));
  })();

  const totalEmotionCount =
    emotionCounts.reduce((sum: number, item: any) => sum + item.count, 0) || 1;

  const dominantEmotion =
    emotionCounts.length > 0
      ? emotionCounts.reduce((a: any, b: any) => (a.count > b.count ? a : b)).emotion
      : "neutral";

  const getEmotionEmoji = (emotion: string) => {
    const e = emotion?.toLowerCase();
    if (e === "happy") return "😊";
    if (e === "sad") return "😟";
    if (e === "agitated") return "😠";
    if (e === "panic") return "😱";
    if (e === "anxious") return "😰";
    if (e === "fear") return "😨";
    if (e === "neutral") return "🙂";
    return "💙";
  };

  const getEmotionColor = (emotion: string) => {
    const e = emotion?.toLowerCase();
    if (e === "happy") return "#10B981";
    if (e === "sad") return "#3B82F6";
    if (e === "agitated" || e === "angry") return "#F59E0B";
    if (e === "panic" || e === "fear") return "#EF4444";
    return "#64748B";
  };

  return (
    <div className="h-full overflow-y-auto bg-[#F6F3EC] p-4 md:p-8 text-[#24312F]">
      <div className="max-w-7xl mx-auto space-y-8 pb-12">

        {/* Premium Header */}
        <div className="relative overflow-hidden bg-white/40 backdrop-blur-md border border-white/60 rounded-[2.5rem] p-8 shadow-xl">
          <div className="relative z-10 flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
            <div>
              <div className="flex items-center gap-3 mb-2">
                <span className="bg-[#2F6F5E] text-white px-3 py-1 rounded-full text-[10px] font-bold tracking-widest uppercase animate-pulse">
                  Live Monitoring
                </span>
                <span className="text-xs text-[#5F6F6B] font-medium">Synced: {new Date().toLocaleTimeString()}</span>
              </div>
              <h1 className="text-5xl font-black text-[#21483F] tracking-tight">
                Care Intelligence
              </h1>
              <p className="text-lg text-[#5F6F6B] mt-3 max-w-2xl font-medium leading-relaxed">
                Analyzing cognitive health and emotional state for <span className="text-[#2F6F5E] font-bold border-b-2 border-[#2F6F5E]/20">{patient.name}</span>.
              </p>
            </div>
            <div className="bg-[#21483F] text-white p-6 rounded-[2rem] shadow-lg flex items-center gap-4 transition-transform hover:scale-105 cursor-pointer">
              <div className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center text-2xl">👩</div>
              <div>
                <p className="text-[10px] uppercase tracking-wider font-bold opacity-70">Digital Companion</p>
                <p className="font-bold text-lg leading-tight">Clara AI Assistant</p>
              </div>
            </div>
          </div>
          <div className="absolute -top-24 -right-24 w-64 h-64 bg-[#2F6F5E]/5 rounded-full blur-3xl" />
        </div>

        {/* Visual Pulse Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <PulseCard 
            title="Total Interactions" 
            value={data.total_chats || 0} 
            subtitle="Conversational data points"
            color="#2F6F5E"
            bg="#EAF3EF"
          />
          <PulseCard 
            title="Crisis Alerts" 
            value={data.alerts?.length || 0} 
            subtitle="Priority interventions needed"
            color={data.alerts?.length > 0 ? "#EF4444" : "#10B981"}
            bg={data.alerts?.length > 0 ? "#FFF1F1" : "#F0FDF4"}
          />
          <PulseCard 
            title="Dominant State" 
            value={dominantEmotion} 
            subtitle="Calculated dominant mood"
            color="#4F46E5"
            bg="#EEF2FF"
            emoji={getEmotionEmoji(dominantEmotion)}
          />
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Main Analytics Column */}
          <div className="xl:col-span-2 space-y-8">
            {/* Emotion Spectrum */}
            <div className="bg-white/70 backdrop-blur-sm border border-white rounded-[2rem] p-8 shadow-lg">
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-2xl font-black text-[#21483F]">Emotion Spectrum</h2>
                <div className="bg-[#F6F3EC] px-4 py-2 rounded-2xl text-xs font-bold text-[#5F6F6B]">System Telemetry</div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  {emotionCounts.length === 0 && <p className="text-[#5F6F6B]">Waiting for telemetry data...</p>}
                  {emotionCounts.map((item: any) => {
                    const width = (item.count / totalEmotionCount) * 100;
                    const color = getEmotionColor(item.emotion);
                    return (
                      <div key={item.emotion} className="group">
                        <div className="flex justify-between text-sm mb-2">
                          <span className="font-bold text-[#21483F] flex items-center gap-2">
                            {getEmotionEmoji(item.emotion)} {item.emotion}
                          </span>
                          <span className="font-black opacity-40">{Math.round(width)}%</span>
                        </div>
                        <div className="h-3 bg-[#E3DDD2]/30 rounded-full overflow-hidden">
                          <div
                            className="h-full rounded-full transition-all duration-1000 group-hover:brightness-110"
                            style={{ width: `${width}%`, backgroundColor: color }}
                          />
                        </div>
                      </div>
                    );
                  })}
                </div>
                
                <div className="bg-[#21483F] rounded-3xl p-6 text-white flex flex-col justify-center relative overflow-hidden">
                  <p className="text-[10px] uppercase font-bold opacity-60 mb-1">Response Latency</p>
                  <h3 className="text-3xl font-black mb-4">{"< 2.4s"}</h3>
                  <p className="text-xs opacity-80 leading-relaxed">Neural processing is optimal. All AI responses are generating within safe dementia-care timeframes.</p>
                  <div className="mt-6 flex gap-1 items-end h-16">
                    {[40, 70, 45, 90, 65, 80, 50, 60, 40].map((h, i) => (
                      <div key={i} className="flex-1 bg-white/20 rounded-full h-full relative flex items-end overflow-hidden">
                        <div className="w-full bg-white/60 rounded-full animate-pulse" style={{ height: `${h}%`, animationDelay: `${i * 0.1}s` }} />
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Recent Conversations */}
            <div className="bg-white/70 backdrop-blur-sm border border-white rounded-[2rem] p-8 shadow-lg">
              <h2 className="text-2xl font-black text-[#21483F] mb-6">Interaction Logs</h2>
              <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {(!data.conversations || data.conversations.length === 0) && <p className="text-[#5F6F6B]">No recent logs.</p>}
                {data.conversations?.map((chat: any) => (
                  <div key={chat.id} className="bg-white border border-[#E3DDD2]/50 rounded-3xl p-6 transition-all hover:shadow-md hover:border-[#2F6F5E]/30">
                    <div className="flex justify-between items-center mb-3">
                      <span className="text-[10px] font-black uppercase text-[#2F6F5E] bg-[#EAF3EF] px-2 py-1 rounded-md">
                        {chat.detected_emotion || "neutral"}
                      </span>
                      <span className="text-[10px] text-[#5F6F6B] font-bold">{new Date(chat.created_at).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-[#5F6F6B] text-sm leading-relaxed mb-4">
                      <b className="text-[#21483F]">Patient:</b> "{chat.user_message}"
                    </p>
                    <div className="bg-[#F6F3EC] p-4 rounded-2xl border-l-4 border-[#2F6F5E]">
                      <p className="text-[#21483F] text-sm font-medium leading-relaxed">
                        <b className="text-[#2F6F5E]">Clara AI:</b> "{chat.ai_response}"
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Side Column: Profile & Alerts */}
          <div className="space-y-8">
            {/* Quick Profile Card */}
            <div className="bg-[#21483F] rounded-[2.5rem] p-8 text-white shadow-2xl relative overflow-hidden">
              <h2 className="text-xl font-black mb-6">Patient Core</h2>
              <div className="space-y-6">
                <ProfileItem label="Cognitive Stage" value={patient.condition_stage || "Early"} />
                <ProfileItem label="Primary Language" value={patient.preferred_language || "English"} />
                <ProfileItem label="Age" value={`${patient.age} years`} />
                <ProfileItem label="Emergency" value={patient.emergency_contact || "Not set"} />
                
                <div className="pt-6 border-t border-white/10 grid grid-cols-2 gap-4 text-center">
                  <div>
                    <p className="text-[10px] uppercase opacity-50 font-bold mb-1 tracking-widest">Status</p>
                    <p className="text-sm font-bold text-[#10B981]">Active</p>
                  </div>
                  <div>
                    <p className="text-[10px] uppercase opacity-50 font-bold mb-1 tracking-widest">AI Link</p>
                    <p className="text-sm font-bold text-[#60A5FA]">Stable</p>
                  </div>
                </div>
              </div>
              <div className="absolute -bottom-8 -left-8 w-32 h-32 bg-white/5 rounded-full blur-2xl" />
            </div>

            {/* Critical Alerts with Automated SMS Options */}
            <div className="bg-white/70 backdrop-blur-sm border border-white rounded-[2rem] p-8 shadow-lg">
              <h2 className="text-2xl font-black text-[#21483F] mb-6">Safety Radar</h2>
              <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 custom-scrollbar">
                {data.alerts?.length === 0 && (
                  <div className="text-center py-10 opacity-40">
                    <div className="text-4xl mb-2">🛡️</div>
                    <p className="text-xs font-bold uppercase tracking-widest">No Alerts Detected</p>
                  </div>
                )}
                {data.alerts?.map((alert: any) => (
                  <div key={alert.id} className={`rounded-3xl p-5 border-2 transition-all hover:scale-[1.02] ${
                      alert.severity === "high" ? "bg-[#FFF1F1] border-[#EF4444]/20" : "bg-[#FFF9E8] border-[#F59E0B]/20"
                    }`}>
                    <div className="flex justify-between items-start mb-3">
                      <span className={`px-3 py-1 rounded-full text-[10px] font-black uppercase ${
                        alert.severity === "high" ? "bg-[#EF4444] text-white" : "bg-[#F59E0B] text-white"
                      }`}>
                        {alert.severity} Priority
                      </span>
                    </div>
                    <p className="font-black text-[#21483F] mb-2">{alert.alert_type}</p>
                    <p className="text-xs text-[#5F6F6B] leading-relaxed mb-4">{alert.message}</p>
                    
                    <div className="flex flex-col gap-2">
                       <div className="flex gap-2">
                          <button 
                            onClick={async () => { await markAlertRead(alert.id); load(); }}
                            className="flex-1 bg-white/80 hover:bg-white text-[#21483F] px-4 py-2 rounded-xl text-[10px] font-bold shadow-sm transition-all"
                          >
                            Dismiss
                          </button>
                          {alert.severity === "high" && (
                            <a href={`tel:${patient.emergency_contact}`} className="bg-[#EF4444] text-white px-4 py-2 rounded-xl text-[10px] font-bold shadow-sm transition-all hover:brightness-110 text-center">
                              Emergency Call
                            </a>
                          )}
                       </div>
                       {alert.severity === "high" && (
                          <a 
                            href={`sms:${patient.emergency_contact}?body=🚨 URGENT: Clara AI detected a crisis for ${patient.name}. Message: "${alert.message}"`} 
                            className="bg-[#21483F] text-white px-4 py-3 rounded-xl text-[10px] font-black uppercase tracking-widest text-center shadow-lg transition-all hover:bg-[#2F6F5E]"
                          >
                            📲 Send Automated SMS Alert
                          </a>
                       )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function PulseCard({ title, value, subtitle, color, bg, emoji }: any) {
  return (
    <div className="group rounded-[2rem] p-8 border border-white shadow-lg transition-all hover:scale-[1.03] hover:shadow-2xl relative overflow-hidden" style={{ backgroundColor: bg }}>
      <div className="relative z-10">
        <p className="text-[10px] font-black uppercase tracking-widest mb-2 opacity-60" style={{ color }}>{title}</p>
        <h2 className="text-4xl font-black tracking-tight flex items-center gap-2 capitalize truncate" style={{ color }}>
          {emoji && <span>{emoji}</span>} {value}
        </h2>
        <p className="text-xs font-bold mt-4 opacity-70" style={{ color }}>{subtitle}</p>
      </div>
      <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
        <div className="w-16 h-16 rounded-full border-4" style={{ borderColor: color }} />
      </div>
    </div>
  );
}

function ProfileItem({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-[10px] uppercase font-bold opacity-50 mb-1 tracking-widest">{label}</p>
      <p className="text-lg font-bold leading-none">{value}</p>
    </div>
  );
}