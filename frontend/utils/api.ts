const API_BASE = "http://127.0.0.1:8000";

export type Patient = {
  id: number;
  name: string;
  age: number;
  gender?: string;
  phone?: string;
  condition_stage?: string;
  preferred_language?: string;
  emergency_contact?: string;
  doctor_phone?: string;
  notes?: string;
  family_members?: string;
  likes?: string;
  dislikes?: string;
  favorite_songs?: string;
  hobbies?: string;
  routine?: string;
  comfort_phrases?: string;
};

export async function login(data: { email: string; password: string }) {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email: data.email,
      password: data.password,
    }),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function register(data: {
  name: string;
  email: string;
  password: string;
  role: string;
}) {
  const res = await fetch(`${API_BASE}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      name: data.name,
      email: data.email,
      password: data.password,
      role: data.role,
    }),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getPatients() {
  const res = await fetch(`${API_BASE}/api/patients/`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function createPatient(data: any) {
  const res = await fetch(`${API_BASE}/api/patients/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function updatePatient(patientId: number, data: any) {
  const res = await fetch(`${API_BASE}/api/patients/${patientId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function deletePatient(patientId: number) {
  const res = await fetch(`${API_BASE}/api/patients/${patientId}`, {
    method: "DELETE",
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function sendChat(data: {
  message: string;
  patient_id: number;
  emotion: string;
  language?: string;
}) {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function sendMessageStream(data: {
  message: string;
  patient_id: number;
  emotion: string;
  language?: string;
}) {
  return sendChat(data);
}

export async function detectEmotion(file: Blob, patientId: number) {
  const formData = new FormData();
  formData.append("file", file, "frame.jpg");
  formData.append("patient_id", String(patientId));

  const res = await fetch(`${API_BASE}/api/emotion`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getDashboard(patientId: number) {
  const res = await fetch(`${API_BASE}/api/dashboard/${patientId}`);
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function markAlertRead(alertId: number) {
  const res = await fetch(`${API_BASE}/api/alerts/${alertId}/read`, {
    method: "PUT",
  });

  if (!res.ok) throw new Error(await res.text());
  return res.json();
}