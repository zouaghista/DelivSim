from Tasks.Task import GenericTask


class TaskRegistry:

    def __init__(self):
        self._active_tasks: list[GenericTask] = []

    def RegisterTask(self, task: GenericTask):
        self._active_tasks.append(task)

    def CancelRegisterTask(self, task: GenericTask):
        if task not in self._active_tasks:
            raise Exception("Task non existent")
        self._active_tasks.remove(task)
        task.CancelTask()

    def SimulateAllTasks(self, deltaTime: float):
        for task in self._active_tasks:
            if task.simulateTask(deltaTime):
                task.finalizeTask()
        for task in self._active_tasks.copy():
            if task.is_task_done():
                self._active_tasks.remove(task)
