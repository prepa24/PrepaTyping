
def calculate_accuracy(target, typed):
    """
    Calculate typing accuracy as a percentage.
    """
    if not typed:
        return 100.0

    correct = 0

    for index, character in enumerate(typed):
        if index < len(target):
            if character == target[index]:
                correct += 1

    return (correct / len(typed)) * 100


def calculate_wpm(typed, elapsed_seconds):
    """
    Calculate gross words per minute.
    Five characters count as one standard word.
    """
    if elapsed_seconds <= 0:
        return 0

    minutes = elapsed_seconds / 60
    words = len(typed) / 5

    return round(words / minutes)
