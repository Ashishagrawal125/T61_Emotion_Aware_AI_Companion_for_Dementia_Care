from collections import Counter

def summarize_emotions(emotion_list: list[str]) -> dict:
    if not emotion_list:
        return {"dominant": "unknown", "count": 0, "distribution": {}}
    counts = Counter(emotion_list)
    dominant, count = counts.most_common(1)[0]
    return {"dominant": dominant, "count": count, "distribution": dict(counts)}
