import uuid
from typing import Callable
from Messaging.MessageRelay import MessageRelay
from Messaging.Messages import GlobalMessage, MessageRef


class MessageManager:

    def __init__(self, timingFunction: Callable[[str, str], tuple[bool, float]]):
        self._messageContext = {}
        self._relays: dict[str, MessageRelay] = {}
        self._timing_function = timingFunction
        self._elapsed_time = 0

    def SetTime(self, time: float):
        self._elapsed_time = time

    def GetTime(self) -> float:
        return self._elapsed_time

    def NewRelay(self, identifier: str) -> MessageRelay:
        assert identifier not in self._relays.keys()
        newRelay = MessageRelay(self, identifier)
        self._relays[identifier] = newRelay
        return newRelay

    def FetchMessage(self, msgIdentifier: str) -> str:
        message = self._messageContext.pop(msgIdentifier)
        return message.content

    def ReceiveMessage(self, messageContent: str, senderId: str, recipientId: str):
        messageId = str(uuid.uuid4())
        newMessage = GlobalMessage(messageContent, recipientId)
        timing = self._timing_function(recipientId, senderId)
        if timing[0]:
            self._relays[recipientId]._registerMessage(MessageRef(messageId, timing[1]))
        self._messageContext[messageId] = newMessage
