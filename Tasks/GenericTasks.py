from Tasks.Task import GenericTask
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from Engine.SimulationObject import ActiveSimulationObject


class GetStockTask(GenericTask):

    def __init__(self, owner: "ActiveSimulationObject", params: dict[str, any]):
        super().__init__(owner, params)
        assert len(params['target']) == 2
        assert "payload" in params.keys()
        self._target = params['target']
        self._time = params.get("timeout", 10)

    def simulateTask(self, deltaTime: float) -> bool:
        if self._owner.GetState('location') == self._target:
            self._time -= deltaTime
            if self._time <= 0:
                return True
        return False

    def finalizeTask(self):
        requested_payload = self._params['payload']
        old_payload = self._owner.GetState('payload')
        storage_facility = self._params["facility"]
        stock = self._owner.GetState("contents")
        for key in requested_payload.keys():
            if key in old_payload.keys():
                old_payload[key] += requested_payload[key]
            else:
                old_payload[key] = requested_payload[key]
            stock[key] -= requested_payload[key]
            if stock[key] == 0:
                del stock[key]
        storage_facility.UpdateState(stock)
        self._owner.UpdateState(old_payload)


class GiveClientOrder(GenericTask):

    def __init__(self, owner: "ActiveSimulationObject", params: dict[str, any]):
        super().__init__(owner, params)
        assert len(params['target']) == 2

    def simulateTask(self, deltaTime: float) -> bool:
        pass

    def finalizeTask(self):
        pass
