from Engine.SimulationObject import ActiveSimulationObject
from Messaging.MessageRelay import MessageRelay
from Tasks.TaskRegistry import TaskRegistry


class Structure(ActiveSimulationObject):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, state: dict[str, any],
                 structure_id: str):
        super().__init__(messageRelay, taskRegistry, structure_id)
