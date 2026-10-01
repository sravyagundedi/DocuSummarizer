import re
from dataclasses import dataclass
from langchain_text_splitters import RecursiveCharacterTextSplitter

SPEAKER_RE = re.compile(r"(?m)^(?:\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*)?([A-Za-z][\w .'-]{0,60}):\s+")

@dataclass
class Chunk:
    index: int
    text: str
    word_count: int

def normalize_speaker_turns(text):
    lines = [x.strip() for x in text.splitlines() if x.strip()]
    turns, current = [], ""
    for line in lines:
        if SPEAKER_RE.match(line):
            if current:
                turns.append(current)
            current = line
        else:
            current = (current + " " + line).strip() if current else line
    if current:
        turns.append(current)
    return turns or [text]

def build_chunks(text, chunk_size=9000, overlap=800):
    turns = normalize_speaker_turns(text)
    chunks, current, current_len = [], [], 0
    for turn in turns:
        if len(turn) > chunk_size:
            if current:
                chunks.append("\n".join(current))
                current, current_len = [], 0
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size,
                chunk_overlap=min(overlap, chunk_size // 10),
                separators=[". ", "? ", "! ", "\n", " ", ""],
            )
            chunks.extend(splitter.split_text(turn))
            continue
        if current and current_len + len(turn) + 2 > chunk_size:
            chunks.append("\n".join(current))
            carry, carry_len = [], 0
            for previous in reversed(current):
                if carry_len + len(previous) + 2 > overlap:
                    break
                carry.insert(0, previous)
                carry_len += len(previous) + 2
            current, current_len = carry, carry_len
        current.append(turn)
        current_len += len(turn) + 2
    if current:
        chunks.append("\n".join(current))
    return [Chunk(i+1, x.strip(), len(x.split())) for i, x in enumerate(chunks) if x.strip()]
