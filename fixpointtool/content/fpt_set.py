class FPTSet:
    LIST_OF_SET_TYPES = ["string", "number", "mapping", "k-tuple", "set_new"]

    def __init__(self, values, set_type=None):

        self.values = values
        self.set_type = set_type
        self.size = len(values)

        if self.set_type is None:
            if self.size == 0:
                self.set_type = "string"
            else:
                from fixpointtool.content.fpt_mapping import FPTMapping
                from fixpointtool.content.fpt_tuple import FPTTuple
                if type(self.values[0]) == int or type(self.values[0]) == float:
                    self.set_type = "number"
                elif type(self.values[0]) == FPTMapping:
                    self.set_type = "mapping"
                elif type(self.values[0]) == FPTTuple:
                    self.set_type = "tuple"
                elif type(self.values[0]) == FPTSet:
                    self.set_type = "set_new"

    def __str__(self):
        return_string = "{"
        if self.size == 0:
            return_string += "}"
        elif self.size == 1:
            return_string += self.values[0] + "}"
        else:
            for elem in self.values:
                return_string += str(elem) + ", "
            return_string = return_string[0:-2] + "}"
        return return_string

    def __repr__(self):
        return_string = "{"
        if self.size == 0:
            return_string += "}"
        elif self.size == 1:
            return_string += self.values[0] + "}"
        else:
            for elem in self.values:
                return_string += str(elem) + ", "
            return_string = return_string[0:-2] + "}"
        return return_string

    def __members(self):
        return frozenset(self.values)

    def __eq__(self, other):
        if (type(self) == type(other)) and (self.size == other.size) and (self.set_type == other.set_type):
            return self.__members() == other.__members()
        else:
            return False

    def __lt__(self, other):
        if (type(self) == type(other)) and (self.set_type == other.set_type):
            return self.size < other.size
        else:
            raise TypeError

    def __le__(self, other):
        if (type(self) == type(other)) and (self.set_type == other.set_type):
            return self.size <= other.size
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.__members())
