from abc import ABC
from Messaging.MessageRelay import MessageRelay
from Tasks.Task import GenericTask
from Tasks.TaskRegistry import TaskRegistry


class ActiveSimulationObject(ABC):

    def __init__(self, messageRelay: MessageRelay, taskRegistry: TaskRegistry):
        self._messageRelay = messageRelay
        self._taskRegistry = taskRegistry
        self._state: dict[str, any] = {}
        self._active_Tasks: list[GenericTask] = []
        self._active = True

    def UpdateState(self, updates: dict[str, any]):
        for key, value in updates.items():
            self._state[key] = value

    def GetFullState(self):
        return self._state

    def GetState(self, state_property):
        return self._state[state_property]

    def RegisterTask(self, task: GenericTask):
        self._taskRegistry.RegisterTask(task)

    def GetAllTasks(self) -> list[GenericTask]:
        return self._active_Tasks

    def RemoveTask(self, task: GenericTask):
        task.CancelTask()
        self._active_Tasks.remove(task)

    def FlushTasks(self):
        """
        Removes tasks that are done from active task pool
        """
        for task in self._active_Tasks.copy():
            if task.is_task_done():
                self._active_Tasks.remove(task)

    def Activate(self):
        self._active = True

    def Deactivate(self):
        self._active = False

    def Is_Active(self):
        return self._active

    def _send_message(self, content: str, recipientId: str):
        self._messageRelay.SendMessage(content, recipientId)

    def _simulateTurn(self, timing: float):
        if not self._active:
            return
        messages = self._messageRelay.GetMessages(timing)
        self.Simulate(messages, timing)

    def Simulate(self, messages: list[str], time: float):
        pass
