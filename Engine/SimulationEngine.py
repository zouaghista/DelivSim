from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Messaging.MessageManager import MessageManager
    from Structures import Structure
    from Tasks.TaskRegistry import TaskRegistry
    from Vehicles import Vehicle


class SimulationEngine:

    def __init__(self, messageManager: "MessageManager", taskRegistry: "TaskRegistry"):
        self._messageManager = messageManager
        self._taskRegistry = taskRegistry
        self._vehicles: list["Vehicle"] = []
        self._structures: list["Structure"] = []

    def AddVehicle(self, vehicle: "Vehicle"):
        self._vehicles.append(vehicle)

    def AddStructure(self, structure: "Structure"):
        self._structures.append(structure)

    def SimulateStep(self, deltaTime: float):
        self._taskRegistry.SimulateAllTasks(deltaTime)
        for structure in self._structures:
            structure._simulateTurn(deltaTime)
        for vehicle in self._vehicles:
            vehicle._simulateTurn(deltaTime)
