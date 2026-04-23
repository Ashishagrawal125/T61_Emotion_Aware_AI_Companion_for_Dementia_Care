"use client";

type HomePageProps = {
  onStart: (mode: string) => void;
};

export default function HomePage({ onStart }: HomePageProps) {
  return (
    <div className="flex flex-col items-center justify-center h-full text-white relative overflow-hidden">

      {/* 🌈 Animated Gradient Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900 via-black to-blue-900 opacity-60" />

      {/* 🔮 Glow Effects */}
      <div className="absolute w-[400px] h-[400px] bg-purple-500 opacity-20 blur-3xl rounded-full top-[-100px] left-[-100px]" />
      <div className="absolute w-[400px] h-[400px] bg-blue-500 opacity-20 blur-3xl rounded-full bottom-[-100px] right-[-100px]" />

      {/* 🧠 Main Content */}
      <div className="z-10 flex flex-col items-center text-center">

        <h1 className="text-6xl font-extrabold mb-4 tracking-wide">
          Clara AI
        </h1>

        <p className="text-lg text-gray-300 mb-10 max-w-xl">
          Your intelligent AI companion that understands your voice, emotions,
          and conversations in real-time.
        </p>

        {/* 🚀 Buttons */}
        <div className="flex gap-5 mb-12">
          <button
            onClick={() => onStart("chat")}
            className="bg-blue-600 px-7 py-3 rounded-xl hover:bg-blue-700 hover:scale-105 transition shadow-xl"
          >
            💬 Chat Assistant
          </button>

          <button
            onClick={() => onStart("voice")}
            className="bg-green-600 px-7 py-3 rounded-xl hover:bg-green-700 hover:scale-105 transition shadow-xl"
          >
            🎤 Voice Mode
          </button>
        </div>

        {/* 🎯 Feature Cards */}
        <div className="grid grid-cols-3 gap-8">

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl hover:scale-105 transition shadow-lg">
            <div className="text-3xl mb-2">💬</div>
            <h3 className="font-semibold text-lg">Smart Chat</h3>
            <p className="text-sm text-gray-300 mt-1">
              Natural AI conversations
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl hover:scale-105 transition shadow-lg">
            <div className="text-3xl mb-2">🎤</div>
            <h3 className="font-semibold text-lg">Voice AI</h3>
            <p className="text-sm text-gray-300 mt-1">
              Speak like a human assistant
            </p>
          </div>

          <div className="bg-white/10 backdrop-blur-md p-6 rounded-2xl hover:scale-105 transition shadow-lg">
            <div className="text-3xl mb-2">😊</div>
            <h3 className="font-semibold text-lg">Emotion AI</h3>
            <p className="text-sm text-gray-300 mt-1">
              Detects and adapts to mood
            </p>
          </div>

        </div>

      </div>
    </div>
  );
}