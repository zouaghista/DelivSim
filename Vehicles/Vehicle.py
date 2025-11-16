from Engine.SimulationObject import ActiveSimulationObject
from Messaging.MessageRelay import MessageRelay
from Tasks.TaskRegistry import TaskRegistry


class Vehicle(ActiveSimulationObject):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, vehicle_id: str):
        super().__init__(messageRelay, taskRegistry)
        self._vehicle_id = vehicle_id

    def GetId(self):
        return self._vehicle_id

    def Simulate(self, messages: list[str], time: float):
        #ActiveSimulationObject will have all your helper functions
        pass
