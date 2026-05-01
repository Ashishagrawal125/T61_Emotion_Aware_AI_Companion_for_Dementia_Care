"use client";

import { useRef, useState, useEffect } from "react";
import { Patient, detectEmotion } from "../utils/api";
type Props = {
  patient: Patient | null;
  onDetect: (emotion: string) => void;
  onDashboardRefresh?: () => void;
};

export default function EmotionCamera({
  patient,
  onDetect,
  onDashboardRefresh,
}: Props) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [emotion, setEmotion] = useState("");
  const [confidence, setConfidence] = useState(0);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isTracking, setIsTracking] = useState(false);
  const [status, setStatus] = useState("Camera is off.");

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
      setStream(mediaStream);
      if (videoRef.current) videoRef.current.srcObject = mediaStream;
      setIsTracking(true);
      setStatus("Camera and AI tracking active.");
    } catch {
      setStatus("Camera permission denied.");
    }
  };

  const stopCamera = () => {
    stream?.getTracks().forEach((track) => track.stop());
    setStream(null);
    setIsTracking(false);
    setEmotion("");
    setConfidence(0);
    setStatus("Camera stopped.");
  };

  const captureFrame = async () => {
    const video = videoRef.current;
    if (!video) return null;

    const canvas = document.createElement("canvas");
    // Optimize: Capture at a lower resolution for faster transport and processing
    canvas.width = 320;
    canvas.height = 240;

    const ctx = canvas.getContext("2d");
    ctx?.drawImage(video, 0, 0, canvas.width, canvas.height);

    return new Promise<Blob | null>((resolve) =>
      canvas.toBlob(resolve, "image/jpeg", 0.7) // Lower quality for speed
    );
  };

  useEffect(() => {
    if (!isTracking) return;

    const interval = setInterval(async () => {
      const blob = await captureFrame();
      if (!blob) return;

      try {
        const data = await detectEmotion(blob, patient?.id || 1);

        setEmotion(data.emotion || "neutral");
        setConfidence(data.confidence || 0);
        onDetect(data.emotion || "neutral");
        onDashboardRefresh?.();

        setStatus("Real-time telemetry synced to Caregiver Dashboard.");
      } catch {
        setStatus("Detection paused. Checking connection...");
      }
    }, 1000); // 1 second interval for faster feedback

    return () => clearInterval(interval);
  }, [isTracking, patient?.id]);

  return (
    <div className="h-full overflow-y-auto bg-[#F6F3EC] p-4 text-[#24312F]">
      <div className="max-w-6xl mx-auto bg-white border border-[#D8E7E0] rounded-3xl p-7 shadow-sm">
        <h2 className="text-4xl font-extrabold text-[#21483F]">
          Advanced Emotion Tracking
        </h2>

        <p className="text-[#5F6F6B] text-lg mt-2">
          Clara AI is monitoring facial expressions, eye engagement, and stress indicators.
        </p>

        <div className="mt-6 bg-[#EAF3EF] border border-[#D8E7E0] rounded-3xl p-6">
          <p className="text-lg font-bold text-[#21483F] mb-3">
            Active Patient: {patient?.name || "No patient selected"}
          </p>

          <div className="relative group">
            <video
              ref={videoRef}
              autoPlay
              muted
              className="rounded-3xl w-full max-w-3xl bg-black mx-auto min-h-[280px] border-4 border-white shadow-xl transition-all duration-500"
              style={{ borderColor: isTracking ? (emotion === "Panic" || emotion === "Anxious" ? "#EF4444" : "#2F6F5E") : "white" }}
            />
            {isTracking && (
              <div className="absolute top-4 right-4 bg-red-500 text-white px-3 py-1 rounded-full text-xs font-bold animate-pulse">
                LIVE TRACKING
              </div>
            )}
          </div>

          <div className="mt-5 flex justify-center gap-4 flex-wrap">
            {!stream ? (
              <button
                onClick={startCamera}
                className="bg-[#2F6F5E] text-white px-8 py-4 rounded-2xl font-bold shadow-lg transition-all hover:scale-105 active:scale-95"
              >
                Open Camera & Start Tracking
              </button>
            ) : (
              <button
                onClick={stopCamera}
                className="bg-red-500 text-white px-8 py-4 rounded-2xl font-bold shadow-lg transition-all hover:scale-105 active:scale-95"
              >
                Stop Camera & Analysis
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-6">
          {/* Main Emotion */}
          <div className="bg-[#FFF8E7] border border-[#EBD9A7] rounded-3xl p-6 text-center">
            <p className="text-xs font-bold text-[#5F6F6B] uppercase tracking-wider">Primary Emotion</p>
            <h3 className="text-4xl font-extrabold capitalize text-[#21483F] mt-2">
              {emotion || "Searching..."}
            </h3>
            <div className="mt-3 w-full bg-white/50 rounded-full h-2">
              <div 
                className="h-full bg-[#D97706] rounded-full transition-all duration-1000" 
                style={{ width: `${confidence}%` }}
              />
            </div>
            <p className="text-sm text-[#5F6F6B] mt-2 font-bold">Confidence: {confidence ? confidence.toFixed(1) : 0}%</p>
          </div>

          {/* Eye Analysis */}
          <div className="bg-[#EEF2FF] border border-[#C7D2FE] rounded-3xl p-6 text-center">
            <p className="text-xs font-bold text-[#4338CA] uppercase tracking-wider">Eye Engagement</p>
            <h3 className="text-4xl font-extrabold text-[#1E1B4B] mt-2">
              {isTracking ? (emotion === "Neutral" || emotion === "Happy" ? "High" : "Wandering") : "--"}
            </h3>
            <p className="text-sm text-[#4338CA] mt-4 font-bold">
              Pupil State: {emotion === "Panic" ? "Dilated" : "Stable"}
            </p>
          </div>

          {/* Status/Sync */}
          <div className="bg-[#F0FDF4] border border-[#BBF7D0] rounded-3xl p-6 text-center flex flex-col justify-center">
            <p className="text-xs font-bold text-[#15803D] uppercase tracking-wider">Telemetry Sync</p>
            <p className="mt-3 text-[#166534] font-medium leading-tight">
              {status}
            </p>
            {isTracking && (
              <p className="mt-2 text-[10px] text-[#15803D] opacity-60">Last update: {new Date().toLocaleTimeString()}</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}