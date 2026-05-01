"use client";

const songs = [
  {
    title: "Ek Pyar Ka Nagma Hai",
    mood: "Calm",
    url: "https://www.youtube.com/results?search_query=Ek+Pyar+Ka+Nagma+Hai",
  },
  {
    title: "Lag Ja Gale",
    mood: "Comfort",
    url: "https://www.youtube.com/results?search_query=Lag+Ja+Gale",
  },
  {
    title: "Tujhse Naraz Nahi Zindagi",
    mood: "Soft",
    url: "https://www.youtube.com/results?search_query=Tujhse+Naraz+Nahi+Zindagi",
  },
  {
    title: "Kabhi Kabhi Mere Dil Mein",
    mood: "Nostalgic",
    url: "https://www.youtube.com/results?search_query=Kabhi+Kabhi+Mere+Dil+Mein",
  },
];

export default function SongPlaylist({ onClose }: { onClose: () => void }) {
  return (
    <div className="fixed inset-0 bg-black/70 grid place-items-center z-50">
      <div className="bg-gray-900 border border-gray-700 rounded-3xl p-6 w-full max-w-2xl text-white">
        <div className="flex justify-between mb-4">
          <h2 className="text-2xl font-bold">Comfort Playlist</h2>
          <button onClick={onClose} className="bg-red-600 px-3 py-2 rounded-xl">
            Close
          </button>
        </div>

        <p className="text-gray-400 mb-4">
          Suggested old songs based on patient preferences.
        </p>

        <div className="space-y-3">
          {songs.map((song) => (
            <a
              key={song.title}
              href={song.url}
              target="_blank"
              className="block bg-gray-800 hover:bg-gray-700 rounded-2xl p-4"
            >
              <div className="font-bold">{song.title}</div>
              <div className="text-sm text-gray-400">Mood: {song.mood}</div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}