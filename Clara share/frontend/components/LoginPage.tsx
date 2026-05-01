"use client";

import { useState } from "react";
import { login, register } from "../utils/api";

type Props = {
  onLogin: (caregiver: any) => void;
};

export default function LoginPage({ onLogin }: Props) {
  const [mode, setMode] = useState<"login" | "register">("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("caregiver");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAction = async () => {
    if (mode === "login") {
      if (!email || !password) { setError("Credentials required."); return; }
      try {
        setError(""); setLoading(true);
        const res = await login({ email, password });
        const caregiver = res.caregiver || { name: email, email, role: "caregiver" };
        localStorage.setItem("caregiver", JSON.stringify(caregiver));
        localStorage.setItem("token", res.access_token || "");
        onLogin(caregiver);
      } catch (err: any) { setError(err.message || "Invalid credentials."); }
      finally { setLoading(false); }
    } else {
      if (!name || !email || !password) { setError("Details required."); return; }
      try {
        setError(""); setLoading(true);
        await register({ name, email, password, role });
        setError("✅ Account verified. Proceeding to login.");
        setTimeout(() => setMode("login"), 1500);
      } catch (err: any) { setError(err.message || "Registration failed."); }
      finally { setLoading(false); }
    }
  };

  return (
    <main className="min-h-screen bg-[#0A1F1C] flex items-center justify-center p-6 relative overflow-hidden font-sans">
      
      {/* Dynamic Background Blobs */}
      <div className="absolute top-[-10%] left-[-10%] w-[500px] h-[500px] bg-[#2F6F5E]/20 rounded-full blur-[120px] animate-pulse" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[400px] h-[400px] bg-[#22C55E]/10 rounded-full blur-[100px]" />

      <div className="w-full max-w-md relative z-10">
        
        {/* Branding */}
        <div className="text-center mb-12">
          <div className="w-20 h-20 bg-gradient-to-br from-[#2F6F5E] to-[#22C55E] rounded-[2rem] flex items-center justify-center text-4xl mx-auto mb-6 shadow-[0_20px_50px_rgba(47,111,94,0.4)] rotate-3">
            👩
          </div>
          <h1 className="text-5xl font-black text-white tracking-tighter mb-2">Clara AI</h1>
          <p className="text-white/40 font-medium tracking-wide uppercase text-[10px]">Neural Care Companion Gateway</p>
        </div>

        {/* Auth Card */}
        <div className="bg-white/10 backdrop-blur-3xl border border-white/10 rounded-[3rem] p-10 shadow-2xl relative overflow-hidden">
          
          <div className="flex gap-2 mb-8 bg-black/20 p-1.5 rounded-2xl">
            <button 
              onClick={() => setMode("login")}
              className={`flex-1 py-3 rounded-xl font-bold text-sm transition-all ${mode === "login" ? 'bg-white text-[#21483F] shadow-lg' : 'text-white/40 hover:text-white'}`}
            >
              Sign In
            </button>
            <button 
              onClick={() => setMode("register")}
              className={`flex-1 py-3 rounded-xl font-bold text-sm transition-all ${mode === "register" ? 'bg-white text-[#21483F] shadow-lg' : 'text-white/40 hover:text-white'}`}
            >
              Join Network
            </button>
          </div>

          <div className="space-y-4">
            {mode === "register" && (
              <Input icon="👤" placeholder="Full Name" value={name} onChange={setName} />
            )}
            <Input icon="📧" placeholder="Medical Email" type="email" value={email} onChange={setEmail} />
            <Input icon="🔒" placeholder="Secure Key" type="password" value={password} onChange={setPassword} />
            
            {mode === "register" && (
              <div className="bg-white/5 rounded-2xl p-4 border border-white/10">
                <p className="text-[10px] font-bold text-white/40 uppercase tracking-widest mb-3 px-1">Network Role</p>
                <div className="grid grid-cols-2 gap-2">
                  {["caregiver", "doctor", "family", "patient"].map((r) => (
                    <button
                      key={r}
                      onClick={() => setRole(r)}
                      className={`py-2 rounded-xl text-[10px] font-bold uppercase tracking-wider transition-all border ${role === r ? 'bg-white text-[#21483F] border-white' : 'text-white/40 border-white/10 hover:border-white/30'}`}
                    >
                      {r}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className={`mt-6 p-4 rounded-2xl text-[10px] font-black uppercase tracking-widest text-center ${error.includes('✅') ? 'bg-green-500/10 text-green-400' : 'bg-red-500/10 text-red-400'}`}>
              {error}
            </div>
          )}

          <button
            onClick={handleAction}
            disabled={loading}
            className="w-full mt-8 bg-gradient-to-r from-[#2F6F5E] to-[#22C55E] hover:from-[#22C55E] hover:to-[#2F6F5E] text-white py-5 rounded-[2rem] font-black text-lg shadow-xl transition-all hover:scale-[1.02] active:scale-98 disabled:opacity-50 disabled:grayscale"
          >
            {loading ? "AUTHENTICATING..." : mode === "login" ? "ACCESS NEURAL LINK" : "INITIALIZE ACCOUNT"}
          </button>

          <p className="mt-8 text-center text-white/20 text-[10px] font-bold uppercase tracking-[0.2em]">
            AES-256 Encrypted Care Portal
          </p>
          
          {/* Subtle line decoration */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-white/10 to-transparent" />
        </div>

        <div className="mt-10 flex justify-center gap-8 text-[10px] font-black text-white/20 uppercase tracking-widest">
           <span className="hover:text-white transition-colors cursor-pointer">HIPAA Compliant</span>
           <span className="hover:text-white transition-colors cursor-pointer">Patient Safety First</span>
           <span className="hover:text-white transition-colors cursor-pointer">24/7 Support</span>
        </div>
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&display=swap');
        body { font-family: 'Inter', sans-serif; }
      `}</style>
    </main>
  );
}

function Input({ icon, placeholder, type = "text", value, onChange }: any) {
  return (
    <div className="relative group">
      <div className="absolute left-5 top-1/2 -translate-y-1/2 text-lg opacity-40 group-focus-within:opacity-100 transition-opacity">{icon}</div>
      <input 
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-white/5 border-2 border-transparent focus:border-[#2F6F5E]/30 focus:bg-white/10 rounded-2xl py-5 pl-14 pr-6 text-white font-bold placeholder:text-white/20 outline-none transition-all"
      />
    </div>
  );
}