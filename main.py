from Engine.SimulationEngine import SimulationEngine
from Messaging.MessageManager import MessageManager
from ScenarioInterpreter import ScenarioInterpreter
from Tasks.TaskRegistry import TaskRegistry

# Simulation example, you will overwrite the Vehicle.py Class and write your own logic
time = 0


def TimingFunc(recipient: str, sender: str) -> tuple[bool, float]:
    return True, time


scenarioInterpreter = ScenarioInterpreter("Input.json", "output.json")
messageManager = MessageManager(TimingFunc)
taskRegistry = TaskRegistry()
simulationEngine = SimulationEngine(messageManager, taskRegistry)

for vehicle in scenarioInterpreter.GetVehicles():
    pass

for structure in scenarioInterpreter.GetStructures():
    pass

clientOrders = scenarioInterpreter.GetOrders()


