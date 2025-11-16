from bisect import bisect_left
from Messaging.Messages import MessageRef
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Messaging.MessageManager import MessageManager


class MessageRelay:

    def __init__(self, messageManager: "MessageManager", identifier: str):
        self._messageManager = messageManager
        self._messages: list[MessageRef] = []
        self._id = identifier

    def _registerMessage(self, message: MessageRef):
        index = bisect_left([m.timing for m in self._messages], message.timing)
        self._messages.insert(index, message)

    def GetMessages(self, timing: float) -> list[str]:
        current_messages = []
        for message in self._messages:
            if message.timing <= timing:
                current_messages.append(self._messageManager.FetchMessage(message.identifier))
        return current_messages

    def SendMessage(self, messageContent: str, recipientId: str):
        self._messageManager.ReceiveMessage(messageContent, self._id, recipientId)
