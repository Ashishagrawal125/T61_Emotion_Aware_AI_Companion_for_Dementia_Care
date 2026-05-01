"use client";

import { useEffect, useState } from "react";
import { getPatients, Patient, createPatient, updatePatient, deletePatient } from "../utils/api";

type Props = {
  selectedPatientId: number | null;
  onSelect: (patient: Patient) => void;
};

const emptyPatient = {
  name: "",
  age: 70,
  gender: "",
  phone: "",
  condition_stage: "mild",
  preferred_language: "English",
  emergency_contact: "",
  doctor_phone: "",
  notes: "",
  family_members: "",
  likes: "",
  dislikes: "",
  favorite_songs: "",
  hobbies: "",
  routine: "",
  comfort_phrases: "",
};

export default function PatientPanel({ selectedPatientId, onSelect }: Props) {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [form, setForm] = useState(emptyPatient);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [message, setMessage] = useState("");

  const loadPatients = async () => {
    try {
      const data = await getPatients();
      setPatients(data);
      if (data.length && !selectedPatientId) onSelect(data[0]);
    } catch {
      setMessage("Connection issue. Please verify backend is active.");
    }
  };

  useEffect(() => {
    loadPatients();
  }, []);

  const startEdit = (p: Patient) => {
    setEditingId(p.id);
    setForm({
      name: p.name || "",
      age: p.age || 70,
      gender: p.gender || "",
      phone: p.phone || "",
      condition_stage: p.condition_stage || "mild",
      preferred_language: p.preferred_language || "English",
      emergency_contact: p.emergency_contact || "",
      doctor_phone: p.doctor_phone || "",
      notes: p.notes || "",
      family_members: p.family_members || "",
      likes: p.likes || "",
      dislikes: p.dislikes || "",
      favorite_songs: p.favorite_songs || "",
      hobbies: p.hobbies || "",
      routine: p.routine || "",
      comfort_phrases: p.comfort_phrases || "",
    });
    onSelect(p);
  };

  const savePatient = async () => {
    try {
      let patient;
      if (editingId) {
        patient = await updatePatient(editingId, form);
        setMessage("Profile updated successfully.");
      } else {
        patient = await createPatient(form);
        setMessage("New patient profile created.");
      }
      setForm(emptyPatient);
      setEditingId(null);
      await loadPatients();
      onSelect(patient);
    } catch (err: any) {
      setMessage(err.message || "Action failed.");
    }
  };

  const handleDelete = async (patientId: number) => {
    if (!window.confirm("Permanently delete this care profile?")) return;
    try {
      await deletePatient(patientId);
      setMessage("Profile removed.");
      await loadPatients();
    } catch (err: any) {
      setMessage("Failed to delete.");
    }
  };

  return (
    <div className="h-full overflow-y-auto bg-[#F6F3EC] p-4 md:p-8 text-[#24312F]">
      <div className="max-w-7xl mx-auto grid grid-cols-1 xl:grid-cols-12 gap-8 pb-12">

        {/* Left Column: Patient Selection (4 cols) */}
        <div className="xl:col-span-5 space-y-6">
          <div className="bg-white/40 backdrop-blur-md border border-white rounded-[2.5rem] p-8 shadow-xl">
            <h2 className="text-3xl font-black text-[#21483F] tracking-tight">Active Profiles</h2>
            <p className="text-[#5F6F6B] mt-2 mb-8 font-medium">Select a patient to initialize the AI companion.</p>

            <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2 custom-scrollbar">
              {patients.length === 0 && (
                <div className="bg-[#2F6F5E]/5 border-2 border-dashed border-[#2F6F5E]/20 rounded-3xl p-10 text-center">
                  <p className="font-bold text-[#21483F]">No patients monitored yet.</p>
                  <p className="text-xs text-[#5F6F6B] mt-2">Initialize a profile using the form.</p>
                </div>
              )}

              {patients.map((p) => (
                <div
                  key={p.id}
                  onClick={() => onSelect(p)}
                  className={`group relative rounded-3xl border-2 p-6 transition-all cursor-pointer hover:scale-[1.02] ${
                    selectedPatientId === p.id
                      ? "bg-[#21483F] text-white border-transparent shadow-2xl"
                      : "bg-white border-white shadow-md hover:border-[#2F6F5E]/30"
                  }`}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className={`w-12 h-12 rounded-2xl flex items-center justify-center text-2xl ${selectedPatientId === p.id ? 'bg-white/20' : 'bg-[#EAF3EF]'}`}>
                      {p.gender === 'Female' ? '👵' : '👴'}
                    </div>
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button onClick={(e) => { e.stopPropagation(); startEdit(p); }} className="p-2 bg-white/20 rounded-lg hover:bg-white/30 text-white"><span className="text-xs">Edit</span></button>
                      <button onClick={(e) => { e.stopPropagation(); handleDelete(p.id); }} className="p-2 bg-red-500/20 rounded-lg hover:bg-red-500/40 text-white"><span className="text-xs">Del</span></button>
                    </div>
                  </div>

                  <h3 className="text-2xl font-black tracking-tight">{p.name}</h3>
                  <p className={`text-sm mt-1 font-medium ${selectedPatientId === p.id ? 'text-white/70' : 'text-[#5F6F6B]'}`}>
                    Age {p.age} • {p.condition_stage || "Mild"} • {p.preferred_language || "English"}
                  </p>
                  
                  {selectedPatientId === p.id && (
                    <div className="mt-4 pt-4 border-t border-white/10 flex gap-4">
                       <span className="bg-white/10 px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider">Active Memory</span>
                       <span className="bg-white/10 px-2 py-1 rounded text-[10px] font-bold uppercase tracking-wider">Syncing Alerts</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Profile Editor (7 cols) */}
        <div className="xl:col-span-7">
          <div className="bg-white rounded-[2.5rem] p-8 md:p-12 shadow-2xl border border-white">
            <div className="flex justify-between items-start mb-8">
               <div>
                  <h2 className="text-4xl font-black text-[#21483F] tracking-tighter">
                    {editingId ? "Refine Memory" : "New Care Profile"}
                  </h2>
                  <p className="text-[#5F6F6B] mt-2 font-medium">Clara uses these details to personalize her companionship.</p>
               </div>
               {editingId && (
                 <button onClick={() => { setEditingId(null); setForm(emptyPatient); }} className="text-[#2F6F5E] font-black text-sm uppercase tracking-widest hover:underline">Cancel Edit</button>
               )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <PremiumField label="Full Name" value={form.name} onChange={(v) => setForm({ ...form, name: v })} placeholder="e.g. Prema Devi" />
              <PremiumField label="Age" value={String(form.age)} onChange={(v) => setForm({ ...form, age: Number(v) })} placeholder="e.g. 72" type="number" />
              <PremiumField label="Gender" value={form.gender} onChange={(v) => setForm({ ...form, gender: v })} placeholder="Female / Male" />
              <PremiumField label="Dementia Stage" value={form.condition_stage} onChange={(v) => setForm({ ...form, condition_stage: v })} placeholder="Mild / Moderate" />
              <PremiumField label="Preferred Language" value={form.preferred_language} onChange={(v) => setForm({ ...form, preferred_language: v })} placeholder="Hindi / English" />
              <PremiumField label="Emergency Phone" value={form.emergency_contact} onChange={(v) => setForm({ ...form, emergency_contact: v })} placeholder="+91..." />
              <PremiumField label="Doctor Phone" value={form.doctor_phone} onChange={(v) => setForm({ ...form, doctor_phone: v })} placeholder="+91..." />
              <PremiumField label="Loved Ones" value={form.family_members} onChange={(v) => setForm({ ...form, family_members: v })} placeholder="Aashi (Daughter), Ramesh (Husband)" />
            </div>

            <div className="mt-8 space-y-6">
               <PremiumTextArea 
                 label="Deep Memory (Likes, Hobbies, Favorites)" 
                 value={form.likes} 
                 onChange={(v: string) => setForm({ ...form, likes: v })} 
                 placeholder="Enter what makes them happy, their favorite old songs, and what they like to talk about..." 
               />
               
               <PremiumTextArea 
                 label="Clinical & Care Notes" 
                 value={form.notes} 
                 onChange={(v: string) => setForm({ ...form, notes: v })} 
                 placeholder="Add specific behavior notes, marital status, or medical history..." 
               />
            </div>

            <div className="mt-10 flex items-center justify-between gap-6">
              <button
                onClick={savePatient}
                className="flex-1 bg-[#21483F] hover:bg-[#2F6F5E] text-white px-8 py-5 rounded-3xl font-black text-lg shadow-2xl transition-all hover:scale-[1.02] active:scale-98"
              >
                {editingId ? "Update Intelligence Link" : "Initialize Care Profile"}
              </button>
            </div>

            {message && (
              <div className="mt-6 p-4 bg-[#EAF3EF] border border-[#2F6F5E]/20 rounded-2xl text-center text-[#2F6F5E] font-bold animate-bounce">
                {message}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function PremiumField({ label, value, onChange, placeholder, type = "text" }: any) {
  return (
    <div className="space-y-2">
      <label className="text-[10px] font-black uppercase tracking-widest text-[#21483F]/60 ml-2">{label}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-[#FAFAF7] border-2 border-transparent focus:border-[#2F6F5E]/30 rounded-2xl px-6 py-4 text-[#21483F] font-bold placeholder:opacity-30 outline-none transition-all"
      />
    </div>
  );
}

function PremiumTextArea({ label, value, onChange, placeholder }: any) {
  return (
    <div className="space-y-2">
      <label className="text-[10px] font-black uppercase tracking-widest text-[#21483F]/60 ml-2">{label}</label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full min-h-[120px] bg-[#FAFAF7] border-2 border-transparent focus:border-[#2F6F5E]/30 rounded-[2rem] px-6 py-5 text-[#21483F] font-bold placeholder:opacity-30 outline-none transition-all resize-none"
      />
    </div>
  );
}