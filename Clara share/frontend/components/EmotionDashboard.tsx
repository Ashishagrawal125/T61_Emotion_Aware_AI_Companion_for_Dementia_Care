"use client";

export default function EmotionDashboard({ history }: { history: string[] }) {
  const countEmotion = (type: string) =>
    history.filter((e) => e === type).length;

  const data = [
    { label: "😊 Happy", value: countEmotion("happy") },
    { label: "😢 Sad", value: countEmotion("sad") },
    { label: "😡 Angry", value: countEmotion("angry") },
    { label: "😐 Neutral", value: countEmotion("neutral") },
  ];

  return (
    <div className="p-4 space-y-6">

      {/* 🔹 Title */}
      <h2 className="text-xl font-bold">Emotion Dashboard</h2>

      {/* 🔹 Graph */}
      <div className="bg-gray-800 p-4 rounded-lg">
        {data.map((item, i) => (
          <div key={i} className="mb-3">
            <div className="flex justify-between text-sm">
              <span>{item.label}</span>
              <span>{item.value}</span>
            </div>

            <div className="w-full bg-gray-700 h-3 rounded">
              <div
                className="bg-blue-500 h-3 rounded"
                style={{ width: `${item.value * 10}%` }}
              />
            </div>
          </div>
        ))}
      </div>

      {/* 🔹 Timeline */}
      <div className="bg-gray-800 p-4 rounded-lg">
        <h3 className="mb-3 font-semibold">Recent Emotions</h3>

        <div className="flex gap-2 flex-wrap">
          {history.slice(-10).map((e, i) => (
            <span
              key={i}
              className="px-2 py-1 bg-gray-700 rounded text-sm"
            >
              {e}
            </span>
          ))}
        </div>
      </div>

    </div>
  );
}