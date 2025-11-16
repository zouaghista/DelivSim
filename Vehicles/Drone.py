from Messaging.MessageRelay import MessageRelay
from Tasks.Task import GenericTask
from Tasks.TaskRegistry import TaskRegistry
from Vehicles.Vehicle import Vehicle


class DroneVehicle(Vehicle):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, state: dict[str, any], vehicle_id: str):
        super(DroneVehicle, self).__init__(messageRelay, taskRegistry, vehicle_id)
        assert 0 <= state['metadata']["charge"] <= 100
        assert "location" in state['metadata'].keys()
        assert state['metadata']["speed"] > 0
        assert state['metadata']["chargeToUnitCost"] > 0
        state['charge'] = state['metadata']["charge"]
        state['speed'] = state['metadata']["speed"]
        state['location'] = state['metadata']["location"]
        state['chargeToUnitCost'] = state['metadata']["chargeToUnitCost"]
        del state['metadata']
        self.UpdateState(state)

    def Simulate(self, messages: list[str], time: float):
        if len(self.GetAllTasks()) == 0:
            print("adding new task")
            flyDroneTask = FlyDroneTask(self, {"target": [10,10]})
            self.RegisterTask(flyDroneTask)


class FlyDroneTask(GenericTask):

    def simulateTask(self, deltaTime: float) -> bool:
        speed = self._vehicle.GetState("speed")
        chargeToUnitCost = self._vehicle.GetState("chargeToUnitCost")
        location = self._vehicle.GetState("location")
        charge = self._vehicle.GetState("charge")
        current_x, current_y = location
        target_x, target_y = self._target
        dir_x = target_x - current_x
        dir_y = target_y - current_y
        dist_sq = dir_x * dir_x + dir_y * dir_y
        if dist_sq < 0.01:
            return True
        magnitude = dist_sq ** 0.5
        norm_x = dir_x / magnitude
        norm_y = dir_y / magnitude
        step = speed * deltaTime
        new_x = current_x + norm_x * step
        new_y = current_y + norm_y * step
        distance_traveled = step
        charge_used = distance_traveled * chargeToUnitCost
        new_charge = max(charge - charge_used, 0)
        new_state = {
            "location": [new_x, new_y],
            "charge": new_charge
        }
        print(new_state)
        self._vehicle.UpdateState(new_state)
        return False

    def finalizeTask(self):
        print("passed")
        self._vehicle.UpdateState({
            "location": self._target
        })

    def __init__(self, vehicle: Vehicle, params: dict[str, any]):
        super().__init__(vehicle, params)
        assert len(params['target']) == 2
        self._target = params['target']
