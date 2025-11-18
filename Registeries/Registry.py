

class GenericRegistry:
    def __init__(self):
        self._reg: [str, any] = {}

    def Add(self, obj: any, obj_id: str):
        self._reg[obj_id] = obj

    def Remove(self, obj_id):
        del self._reg[obj_id]

    def Get(self, obj_id):
        return self._reg[obj_id]
