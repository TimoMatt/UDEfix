from fixpointtool.content.fpt_mapping import FPTMapping


class FPTRelation:
    LIST_OF_RELATION_TYPES = ["custom", "is-element-of", "projection"]
    # DICT_OF_IS_ELEMENT_OF_TYPES = {
    #     0: "X -> Y",
    #     1: "X -> P(X)",
    # }
    DICT_OF_PROJECTION_TYPES = {
        0: "(x, y) -> x",
        1: "(x, y) -> y",
        2: "{(x\u2081, y\u2081),...} -> ({x\u2081,...}, {y\u2081,...})",
        3: "{(x\u2081, y\u2081),...} -> {x\u2081,...}",
        4: "{(x\u2081, y\u2081),...} -> {y\u2081,...}"
    }

    def __init__(self, name, relation, input_set_name, output_set_name, type=None, projection_type=None):

        self.name = name
        self.relation = relation
        self.input_set_name = input_set_name
        self.output_set_name = output_set_name

        if type is None:
            self.type = "custom"
        else:
            if type in FPTRelation.LIST_OF_RELATION_TYPES:
                self.type = type
            else:
                self.type = "custom"
                print("WARNING: Unsupported relation type")

        # if is_element_of_type in FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES.keys():
        #     self.is_element_of_type = is_element_of_type
        # elif is_element_of_type in FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES.values():
        #     self.projection_type = list(FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES.keys())[list(FPTRelation.DICT_OF_IS_ELEMENT_OF_TYPES.values()).index(is_element_of_type)]
        # else:
        #     self.is_element_of_type = 0

        if projection_type in FPTRelation.DICT_OF_PROJECTION_TYPES.keys():
            self.projection_type = projection_type
        elif projection_type in FPTRelation.DICT_OF_PROJECTION_TYPES.values():
            self.projection_type = list(FPTRelation.DICT_OF_PROJECTION_TYPES.keys())[list(FPTRelation.DICT_OF_PROJECTION_TYPES.values()).index(projection_type)]
        else:
            self.projection_type = 0

    def getRelation(self):
        # mapsFromFunction = False
        # for elem in self.relation:
        #     mapsFromFunction = type(elem[0]) == FPTMapping
        #     break
        #
        # mapsFromFunctionTuple = False
        # for elem in self.relation:
        #     if type(elem[0]) == tuple:
        #         mapsFromFunctionTuple = type(elem[0][0]) == FPTMapping
        #         break
        #     break
        #
        # mapsFromFunctionSet = False
        # for elem in self.relation:
        #     if type(elem[0]) == frozenset:
        #         done = False
        #         for innerElem in elem[0]:
        #             mapsFromFunctionSet = type(innerElem) == FPTMapping
        #             done = True
        #             break
        #         if done:
        #             break
        #     else:
        #         break
        #
        # mapsToFunction = False
        # for elem in self.relation:
        #     mapsToFunction = type(elem[1]) == FPTMapping
        #     break
        #
        # mapsToFunctionTuple = False
        # for elem in self.relation:
        #     if type(elem[1]) == tuple:
        #         mapsToFunctionTuple = type(elem[1][0]) == FPTMapping
        #         break
        #     break
        #
        # mapsToFunctionSet = False
        # for elem in self.relation:
        #     if type(elem[1]) == frozenset:
        #         done = False
        #         for innerElem in elem[1]:
        #             mapsToFunctionSet = type(innerElem) == FPTMapping
        #             done = True
        #             break
        #         if done:
        #             break
        #     else:
        #         break

        mapsFromFunction = False
        for elem in self.relation:
            mapsFromFunction = type(elem[0]) == FPTMapping
            break

        mapsFromFunctionTuple = []
        for elem in self.relation:
            if type(elem[0]) == tuple:
                mapsFromFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem[0]]
                # mapsFromFunctionTuple = type(elem[0]) == FPTMapping
                break
            break

        mapsFromFunctionSet = False
        for elem in self.relation:
            if type(elem[0]) == frozenset:
                done = False
                for innerElem in elem[0]:
                    mapsFromFunctionSet = type(innerElem) == FPTMapping
                    done = True
                    break
                if done:
                    break
            else:
                break

        mapsToFunction = False
        for elem in self.relation:
            mapsToFunction = type(elem[1]) == FPTMapping
            break

        mapsToFunctionTuple = [False]
        for elem in self.relation:
            if type(elem[1]) == tuple:
                mapsToFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem[1]]
                # mapsToFunctionTuple = type(elem[0]) == FPTMapping
                break
            break

        mapsToFunctionSet = False
        for elem in self.relation:
            if type(elem[1]) == frozenset:
                done = False
                for innerElem in elem[1]:
                    mapsToFunctionSet = type(innerElem) == FPTMapping
                    done = True
                    break
                if done:
                    break
            else:
                break

        newRelation = []
        for tup in self.relation:
            if mapsFromFunction and mapsToFunction:
                newRelation.append(tuple([tup[0].createFunctionFromList(), tup[1].createFunctionFromList()]))
            elif mapsFromFunction and any(mapsToFunctionTuple):
                newToTup = []
                for i in range(len(tup[1])):
                    if mapsToFunctionTuple[i]:
                        newToTup.append(tup[1][i].createFunctionFromList())
                    else:
                        newToTup.append(tup[1][i])
                newRelation.append(tuple([tup[0].createFunctionFromList(), tuple(newToTup)]))
            elif mapsFromFunction and mapsToFunctionSet:
                newSet = []
                for elem in tup[1]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([tup[0].createFunctionFromList(), frozenset(newSet)]))
            elif any(mapsFromFunctionTuple) and mapsToFunction:
                newFromTup = []
                for i in range(len(tup[0])):
                    if mapsFromFunctionTuple[i]:
                        newFromTup.append(tup[0][i].createFunctionFromList())
                    else:
                        newFromTup.append(tup[0][i])
                newRelation.append(tuple([tuple(newFromTup), tup[1].createFunctionFromList()]))
            elif any(mapsFromFunctionTuple) and any(mapsToFunctionTuple):
                newFromTup = []
                for i in range(len(tup[0])):
                    if mapsFromFunctionTuple[i]:
                        newFromTup.append(tup[0][i].createFunctionFromList())
                    else:
                        newFromTup.append(tup[0][i])
                newToTup = []
                for i in range(len(tup[1])):
                    if mapsToFunctionTuple[i]:
                        newToTup.append(tup[1][i].createFunctionFromList())
                    else:
                        newToTup.append(tup[1][i])
                newRelation.append(tuple([tuple(newFromTup), tuple(newToTup)]))
            elif any(mapsFromFunctionTuple) and mapsToFunctionSet:
                newFromTup = []
                for i in range(len(tup[0])):
                    if mapsFromFunctionTuple[i]:
                        newFromTup.append(tup[0][i].createFunctionFromList())
                    else:
                        newFromTup.append(tup[0][i])
                newSet = []
                for elem in tup[1]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([tuple(newFromTup), frozenset(newSet)]))
            elif mapsFromFunctionSet and mapsToFunction:
                newSet = []
                for elem in tup[0]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([frozenset(newSet), tup[1].createFunctionFromList()]))
            elif mapsFromFunctionSet and any(mapsToFunctionTuple):
                newToTup = []
                for i in range(len(tup[1])):
                    if mapsToFunctionTuple[i]:
                        newToTup.append(tup[1][i].createFunctionFromList())
                    else:
                        newToTup.append(tup[1][i])
                newSet = []
                for elem in tup[0]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([frozenset(newSet), tuple(newToTup)]))
            elif mapsFromFunctionSet and mapsToFunctionSet:
                newSet0 = []
                for elem in tup[0]:
                    newSet0.append(elem.createFunctionFromList())
                newSet1 = []
                for elem in tup[1]:
                    newSet1.append(elem.createFunctionFromList())
                newRelation.append(tuple([frozenset(newSet0), frozenset(newSet1)]))
            elif mapsFromFunction:
                newRelation.append(tuple([tup[0].createFunctionFromList(), tup[1]]))
            elif any(mapsFromFunctionTuple):
                newFromTup = []
                for i in range(len(tup[0])):
                    if mapsFromFunctionTuple[i]:
                        newFromTup.append(tup[0][i].createFunctionFromList())
                    else:
                        newFromTup.append(tup[0][i])
                newRelation.append(tuple([tuple(newFromTup), tup[1]]))
            elif mapsFromFunctionSet:
                newSet = []
                for elem in tup[0]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([frozenset(newSet), tup[1]]))
            elif mapsToFunction:
                newRelation.append(tuple([tup[0], tup[1].createFunctionFromList()]))
            elif any(mapsToFunctionTuple):
                newToTup = []
                for i in range(len(tup[1])):
                    if mapsToFunctionTuple[i]:
                        newToTup.append(tup[1][i].createFunctionFromList())
                    else:
                        newToTup.append(tup[1][i])
                newRelation.append(tuple([tup[0], tuple(newToTup)]))
            elif mapsToFunctionSet:
                newSet = []
                for elem in tup[1]:
                    newSet.append(elem.createFunctionFromList())
                newRelation.append(tuple([tup[0], frozenset(newSet)]))
            else:
                return self.relation

        return frozenset(newRelation)

    def __str__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ", " + str(self.input_set_name) + ", " + str(self.output_set_name) + ", " + str([(x, y) for [x, y] in self.relation]) + ")"

    def __repr__(self):
        return "(" + str(self.name) + ", " + str(self.type) + ", " + str(self.input_set_name) + ", " + str(self.output_set_name) + ", " + str([(x, y) for [x, y] in self.relation]) + ")"
