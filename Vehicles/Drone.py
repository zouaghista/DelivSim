from Messaging.MessageRelay import MessageRelay
from Tasks.Task import GenericTask
from Tasks.TaskRegistry import TaskRegistry
from Vehicles.Vehicle import Vehicle


class DroneVehicle(Vehicle):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry, state: dict[str, any], vehicle_id: str):
        super(DroneVehicle, self).__init__(messageRelay, taskRegistry, vehicle_id)
        assert 0 <= state["charge"] <= 100
        assert "location" in state.keys()
        assert state["speed"] > 0
        assert state["chargeToUnitCost"] > 0
        self.UpdateState(state)


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
        self._vehicle.UpdateState(new_state)
        return False

    def finalizeTask(self):
        self._finalization_callback()

    def __init__(self, callback, vehicle: Vehicle, params: dict[str, any]):
        super().__init__(callback, vehicle, params)
        assert len(params['target']) == 2
        self._target = params['target']
