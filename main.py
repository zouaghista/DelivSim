from Engine.SimulationEngine import SimulationEngine
from Messaging.MessageManager import MessageManager
from Messaging.MessageRelay import MessageRelay
from ScenarioInterpreter import ScenarioInterpreter
from Tasks.TaskRegistry import TaskRegistry
from Vehicles.Drone import DroneVehicle

# Simulation example, you will overwrite the Vehicle.py Class and write your own logic
time = 0


def TimingFunc(recipient: str, sender: str) -> tuple[bool, float]:
    return True, time


scenarioInterpreter = ScenarioInterpreter("Example/ScenarioExample.json", "output.json")
messageManager = MessageManager(TimingFunc)
taskRegistry = TaskRegistry()
simulationEngine = SimulationEngine(messageManager, taskRegistry)

vid = 0
for vehicle in scenarioInterpreter.GetVehicles():
    message_relay = MessageRelay(messageManager, "rv" + str(vid))
    new_vehicle = DroneVehicle(message_relay, taskRegistry, vehicle, "v" + str(vid))
    simulationEngine.AddVehicle(new_vehicle)

sid = 0
for structure in scenarioInterpreter.GetStructures():
    pass

#clientOrders = scenarioInterpreter.GetOrders()
deltaTime = scenarioInterpreter.GetDeltaTime()
while True:
    simulationEngine.SimulateStep(deltaTime)
