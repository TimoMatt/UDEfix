class FPTTuple:
    LIST_OF_TUPLE_TYPES = ["string", "number", "mapping", "k-tuple", "set_new"]

    def __init__(self, values, tuple_types=None):
        if tuple_types is None:
            tuple_types = []

        self.values = values
        self.tuple_types = tuple_types
        self.k = len(values)

        print(self.tuple_types)

        if self.k < 2 or (len(self.tuple_types) != 0 and len(self.tuple_types) == len(self.values)):
            print("WARNING: Tuple has been constructed incorrectly")

        if not len(self.tuple_types):
            from fixpointtool.content.fpt_mapping import FPTMapping
            from fixpointtool.content.fpt_set import FPTSet
            for elem in self.values:
                if type(elem) == int or type(elem) == float:
                    self.tuple_types.append("number")
                elif type(elem) == FPTMapping:
                    self.tuple_types.append("mapping")
                elif type(elem) == FPTTuple:
                    self.tuple_types.append("tuple")
                elif type(elem) == FPTSet:
                    self.tuple_types.append("set")
                else:
                    self.tuple_types.append("string")

    def __str__(self):
        # works only for k >= 2
        return_string = "("
        for elem in self.values:
            return_string += str(elem) + ", "
        return_string = return_string[0:-2] + ")"
        return return_string

    def __repr__(self):
        # works only for k >= 2
        return_string = "("
        for elem in self.values:
            return_string += str(elem) + ", "
        return_string = return_string[0:-2] + ")"
        return return_string

    def __members(self):
        return tuple(self.values)

    def __eq__(self, other):
        if (type(self) == type(other)) and (self.k == other.k) and (self.tuple_types == other.tuple_types):
            return self.__members() == other.__members()
        else:
            return False

    def __hash__(self):
        return hash(self.__members())
