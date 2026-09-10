from math import log1p


def score_from_count(count: int, sample_size: int) -> float:
    """Small transparent MVP scoring helper.

    This is not a probability of being victimized.
    It is a normalized activity indicator intended for experimentation.
    """
    if count <= 0:
        return 0.0
    denominator = max(sample_size, 1)
    ratio = count / denominator
    score = min(100.0, 100.0 * (log1p(count) / log1p(denominator)))
    return round(score, 2)
