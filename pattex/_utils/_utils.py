def _length_check(text: str, length: int) -> bool:
    """
    Check if the length of the text is less than or equal to the specified length.
    Args:
        text (str): _description_
        length (int): _description_

    Returns:
        bool: True if the length of the text is less than or equal to the specified length, False otherwise.
    """
    return len(text) <= length