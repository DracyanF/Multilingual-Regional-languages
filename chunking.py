def chunk_text(text, max_chars=1800):
    chunks = []
    buffer = ""

    for line in text.split("\n"):
        if len(buffer) + len(line) <= max_chars:
            buffer += line + "\n"
        else:
            chunks.append(buffer)
            buffer = line + "\n"

    if buffer.strip():
        chunks.append(buffer)

    return chunks
