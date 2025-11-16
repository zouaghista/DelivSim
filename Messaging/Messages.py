from dataclasses import dataclass


@dataclass
class MessageRef:
    identifier: str
    timing: float


@dataclass
class GlobalMessage:
    content: str
    RecipientId: str
