import json


class ScenarioInterpreter:

    def __init__(self, scenario_input, scenario_output):
        with open(scenario_input, "r") as f:
            self.data = json.load(f)
        self._scenario_output = scenario_output

    def GetVehicles(self) -> list[dict]:
        return self.data["vehicles"]

    def GetStructures(self) -> list[dict]:
        return self.data["structures"]

    def GetOrders(self) -> list[dict]:
        return self.data["orders"]

    def GetClients(self) -> list[dict]:
        return self.data["clients"]
