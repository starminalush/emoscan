from collections import Counter


def get_statictics_of_emotion(emotions: list[str]) -> dict[str, float]:
    """Calculate proportion of emotions.

    Args:
        emotions: List of recognized emotions.

    Returns:
        Dict containing emotion and its percentage relative to all elements of the input list.
    """
    counter = Counter(emotions)
    if counter.total() > 0:
        emotion_proportion = {
            emotion: count / counter.total() * 100 for emotion, count in counter.items()
        }
        return dict(
            sorted(
                emotion_proportion.items(),
                key=lambda emotion_data: emotion_data[1],
                reverse=True,
            )
        )
    return {}
