from Engine.SimulationObject import ActiveSimulationObject
from Messaging.MessageRelay import MessageRelay
from Tasks.TaskRegistry import TaskRegistry


class Structure(ActiveSimulationObject):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, structure_id: str):
        super().__init__(messageRelay, taskRegistry)
        self._structure_id = structure_id
