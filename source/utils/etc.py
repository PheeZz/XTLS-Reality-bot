def is_text_int_number(text: str) -> bool:
    try:
        int(text)
    except ValueError:
        return False
    else:
        return True
