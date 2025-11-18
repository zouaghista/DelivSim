import json
from abc import ABC, abstractmethod
import hashlib
from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from Engine.SimulationObject import ActiveSimulationObject


class GenericTask(ABC):

    def __init__(self, owner: "ActiveSimulationObject", params: dict[str, any]):
        self._owner = owner
        self._task_done = False
        self._params = params

    def is_task_done(self) -> bool:
        """

        :return: True if the task is done, False otherwise
        """
        return self._task_done

    def _simulateTask(self, deltaTime: float):
        return self.simulateTask(deltaTime)

    def _finalizeTask(self):
        self._task_done = True
        return self.finalizeTask()

    def CancelTask(self):
        pass

    @abstractmethod
    def simulateTask(self, deltaTime: float) -> bool:
        """
        Executes one simulation step of the task.

        Args:
            deltaTime (float): Time elapsed since the previous simulation step.

        Returns:
            bool: True if the task has completed, False otherwise.
        """
        return False

    @abstractmethod
    def finalizeTask(self):
        """
        Executes once the task finishes
        """
        pass


class GenericSharedTask(GenericTask):
    peer_dict: Dict[bytes, list[GenericTask]] = {}
    score_dict: Dict[bytes, int] = {}

    def __init__(self, owner: "ActiveSimulationObject", params: dict[str, any], peers: list["ActiveSimulationObject"]):
        super().__init__(owner, params)
        self.peers = peers
        self._finalized = False
        peer_list = peers.copy()
        peer_list.append(owner)
        peer_list = sorted(peer_list, key=lambda item: item.vehicle_id)
        concat = self.__class__.__name__
        concat += json.dumps(params, sort_keys=True, separators=(',', ':'))
        concat += "".join(vehicle.GetId() for vehicle in peer_list)
        task_hash = hashlib.sha256(concat.encode("utf-8")).digest()
        if task_hash not in GenericSharedTask.peer_dict.keys():
            GenericSharedTask.peer_dict[task_hash] = [self]
            GenericSharedTask.score_dict[task_hash] = 0
            return
        self._event_hash = task_hash
        GenericSharedTask.peer_dict[task_hash].append(self)

    def _simulateTask(self, deltaTime: float) -> bool:
        if self._finalized:
            return False
        task_state = self.simulateTask(deltaTime)
        if task_state and self._evaluate_peers():
            self._task_done = True
        return True

    def _finalizeTask(self):
        if self._task_done:
            del GenericSharedTask.score_dict[self._event_hash]
            for peer in GenericSharedTask.peer_dict[self._event_hash]:
                peer.finalizeTask()
                peer._task_done = True
            del GenericSharedTask.peer_dict[self._event_hash]
            return
        GenericSharedTask.score_dict[self._event_hash] += 1
        self._finalized = True
        return

    def _evaluate_peers(self):
        if self._event_hash in GenericSharedTask.peer_dict.keys():
            return self.EvaluatePeers()
        return False

    def CancelTask(self):
        if self._event_hash not in GenericSharedTask.peer_dict.keys():
            return
        GenericSharedTask.peer_dict[self._event_hash].remove(self)

    @abstractmethod
    def EvaluatePeers(self) -> bool:
        """
        Evaluates if all peers are done with executing a task.
        Returns:
            bool: True if the conditions for the joint task are met, False otherwise.
        """
        return False

    @abstractmethod
    def finalizeTask(self):
        """
        Executes once the task finishes
        """
        pass

    @abstractmethod
    def simulateTask(self, deltaTime: float) -> bool:
        """
        Executes one simulation step of the task.

        Args:
            deltaTime (float): Time elapsed since the previous simulation step.

        Returns:
            bool: True if the task has completed, False otherwise.
        """
        return False
