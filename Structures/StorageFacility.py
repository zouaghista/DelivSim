import json

from Structures.Structure import Structure
from Messaging.MessageRelay import MessageRelay
from Tasks.TaskRegistry import TaskRegistry


class StorageFacility(Structure):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, state: dict[str, any],structure_id: str):
        super().__init__(messageRelay, taskRegistry, state,structure_id)
        assert state["type"] == "storage"
        assert "location" in state.keys()
        assert state['contents']
        self.UpdateState(state)

    def Simulate(self, messages: list[str], time: float):
        #I will assume that you send a storage facility a query if it has any items
        #The query is as follows {"milk": 8, "soda": 10}
        #the facility will reply {"milk": 6} if it only has any items of interest and their amount
        #you can also reserve an item by sending {"content":{"milk": 8, "soda": 10}, "reserve": True}
        #all messages should have the sender id attached {"sender":"V1"}
        for message in messages:
            messageObject = json.loads(message)
            print(message)
            sender = messageObject['sender']
            contents = self.GetState("contents")
            query_reply = {}
            for key in messageObject["content"].keys():
                if key in contents.keys():
                    query_reply[key] = min(contents[key], messageObject['content'][key])
            if 'reserve' in messageObject.keys() and messageObject['reserve']:
                for key in query_reply:
                    query_reply[key] = contents[key] - query_reply[key]
                self.UpdateState(query_reply)
                self.Send_message("OK", sender)
                return
            self.Send_message(json.dumps(query_reply), sender)

