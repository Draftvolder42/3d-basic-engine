from dataclasses import dataclass

@dataclass
class Text:
    text = str
    color = tuple
    font = any