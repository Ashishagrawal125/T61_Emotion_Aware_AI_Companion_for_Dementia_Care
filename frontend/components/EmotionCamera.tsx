"use client";

import { useRef, useState, useEffect } from "react";

export default function EmotionCamera({ onDetect }: any) {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [emotion, setEmotion] = useState("");
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isTracking, setIsTracking] = useState(false);

  // 🎥 Start Camera
  const startCamera = async () => {
    const mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });
    setStream(mediaStream);

    if (videoRef.current) {
      videoRef.current.srcObject = mediaStream;
    }
  };

  // 🛑 Stop Camera
  const stopCamera = () => {
    stream?.getTracks().forEach((track) => track.stop());
    setStream(null);
    setIsTracking(false);
  };

  // 📸 Capture frame
  const captureFrame = async () => {
    const video = videoRef.current;
    if (!video) return null;

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx?.drawImage(video, 0, 0);

    return new Promise<Blob | null>((resolve) =>
      canvas.toBlob(resolve, "image/jpeg")
    );
  };

  // 🔥 AUTO DETECTION LOOP
  useEffect(() => {
    if (!isTracking) return;

    const interval = setInterval(async () => {
      const blob = await captureFrame();
      if (!blob) return;

      const formData = new FormData();
      formData.append("file", blob, "image.jpg");

      try {
        const res = await fetch("http://127.0.0.1:8000/api/emotion", {
          method: "POST",
          body: formData,
        });

        const data = await res.json();

        setEmotion(data.emotion);
        onDetect(data.emotion);

      } catch (err) {
        console.error("Emotion error:", err);
      }
    }, 3000); // ⏱ every 3 sec

    return () => clearInterval(interval);
  }, [isTracking]);

  return (
    <div className="text-center">
      <video ref={videoRef} autoPlay className="rounded-lg w-80 mx-auto" />

      <div className="mt-3 space-x-2">
        <button onClick={startCamera} className="bg-blue-600 px-3 py-1 rounded">
          Start Camera
        </button>

        <button
          onClick={() => setIsTracking(true)}
          className="bg-green-600 px-3 py-1 rounded"
        >
          Start Tracking
        </button>

        <button onClick={stopCamera} className="bg-red-600 px-3 py-1 rounded">
          Stop Camera
        </button>
      </div>

      {emotion && (
        <div className="mt-4 text-lg">
          Live Emotion: <b>{emotion}</b>
        </div>
      )}
    </div>
  );
}