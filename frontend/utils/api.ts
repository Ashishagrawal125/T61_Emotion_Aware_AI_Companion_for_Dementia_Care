export async function sendMessageStream(
  message: string,
  emotion: string,
  onChunk: (chunk: string) => void
) {
  const res = await fetch("http://localhost:8000/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message,
      emotion,
    }),
  });

  const reader = res.body?.getReader();
  const decoder = new TextDecoder("utf-8");

  if (!reader) {
    console.error("Reader not found");
    return;
  }

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    onChunk(chunk);
  }
}