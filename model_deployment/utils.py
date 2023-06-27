def postprocess_bbox(bbox: list[int]) -> list[int | None]:
    """Postprocess face detector or tracker bbox.

    Args:
        bbox: Initial bbox.

    Returns:
        Postprocessed bbox.
    """
    if bbox[0] < bbox[2] and bbox[1] < bbox[3]:
        return [0 if coord < 0 else coord for coord in bbox]
    return []
