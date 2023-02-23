
class NotDefinedError(Exception):
    pass


class FPTMapping:
    LIST_OF_MAPPING_TYPES = ["all", "constant", "reindexing", "arithmetic", "testing", "miscellaneous"]
    dictOfFPTMappings = {}
    dictOfMappings = {}

    listOfInvalidFPTMappings = []

    def __init__(self, name, list_of_tuples=None, mapping_type=None, input_set_name=None, output_set_name=None, input_mv=None, input_mv_k=None, output_mv=None, output_mv_k=None):
        self.name = name
        self.inputSetName = input_set_name
        self.outputSetName = output_set_name
        self.inputMV = input_mv
        self.inputMVK = input_mv_k
        self.outputMV = output_mv
        self.outputMVK = output_mv_k

        self.isNew = False
        self.listOfTuples = []
        self.listOfElements = []
        self.listOfValues = []

        self.mappingType = "all"
        self.inputType = str
        self.outputType = str

        if mapping_type is not None:
            if mapping_type in FPTMapping.LIST_OF_MAPPING_TYPES:
                self.mappingType = mapping_type
            else:
                print("WARNING: Tried to create a mapping with a non-existing mapping type!")
                self.mappingType = "all"
        else:
            self.calculateMappingType()

        if list_of_tuples is not None:
            self.isNew = True
            self.listOfTuples = list_of_tuples

            for tup in self.listOfTuples:
                self.listOfElements.append(tup[0])
                self.listOfValues.append(tup[1])

            self.calculateTypes()
        else:
            self.calculateListOfTuples()

        if self.isNew:
            self.createFunctionFromList()

    @staticmethod
    def repairInvalidFPTMappings():
        for funcObj in FPTMapping.listOfInvalidFPTMappings:
            funcObj.calculateMappingType()
            funcObj.calculateListOfTuples()
        FPTMapping.listOfInvalidFPTMappings = []

    @staticmethod
    def getNewMappingName():
        newMappingName = "new mapping"
        counter = 1
        while True:
            if newMappingName + str(counter) not in FPTMapping.dictOfFPTMappings.keys():
                return newMappingName + str(counter)
            counter += 1

    def createFunctionFromList(self):
        if self.name in FPTMapping.dictOfMappings.keys():
            newFunction = FPTMapping.dictOfMappings[self.name]
        else:
            if not self.isNew:
                print("WARNING: Tried to access a mapping that is not created yet")

            mapsFromFunction = False
            for elem in self.listOfElements:
                mapsFromFunction = type(elem) == FPTMapping
                break

            mapsFromFunctionTuple = []
            for elem in self.listOfElements:
                if type(elem) == tuple:
                    mapsFromFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem]
                    # mapsFromFunctionTuple = type(elem[0]) == FPTMapping
                    break
                break

            mapsFromFunctionSet = False
            for elem in self.listOfElements:
                if type(elem) == frozenset:
                    done = False
                    for innerElem in elem:
                        mapsFromFunctionSet = type(innerElem) == FPTMapping
                        done = True
                        break
                    if done:
                        break
                else:
                    break

            mapsToFunction = False
            for elem in self.listOfValues:
                mapsToFunction = type(elem) == FPTMapping
                break

            mapsToFunctionTuple = [False]
            for elem in self.listOfValues:
                if type(elem) == tuple:
                    mapsToFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem]
                    # mapsToFunctionTuple = type(elem[0]) == FPTMapping
                    break
                break

            mapsToFunctionSet = False
            for elem in self.listOfValues:
                if type(elem) == frozenset:
                    done = False
                    for innerElem in elem:
                        mapsToFunctionSet = type(innerElem) == FPTMapping
                        done = True
                        break
                    if done:
                        break
                else:
                    break

            if mapsFromFunction and mapsToFunction:
                newListOfElements = []
                for elem in self.listOfElements:
                    newListOfElements.append(elem.createFunctionFromList())

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                    else:
                        raise NotDefinedError
            elif mapsFromFunction and any(mapsToFunctionTuple):
                newListOfElements = []
                for elem in self.listOfElements:
                    newListOfElements.append(elem.createFunctionFromList())

                def newFunction(x):
                    if x in newListOfElements:
                        tup = self.listOfValues[newListOfElements.index(x)]
                        for i in range(len(tup)):
                            if tup[i] is not None and mapsToFunctionTuple[i]:
                                tup[i] = tup[i].createFunctionFromList()
                        return tup
                    else:
                        raise NotDefinedError()
            elif mapsFromFunction and mapsToFunctionSet:
                newListOfElements = []
                for elem in self.listOfElements:
                    newListOfElements.append(elem.createFunctionFromList())

                def newFunction(x):
                    if x in newListOfElements:
                        oldSet = self.listOfValues[newListOfElements.index(x)]
                        newSet = []
                        for elem in oldSet:
                            newSet.append(elem.createFunctionFromList())
                        return frozenset(newSet)
                    else:
                        raise NotDefinedError()
            elif any(mapsFromFunctionTuple) and mapsToFunction:
                newListOfElements = []
                for elem in self.listOfElements:
                    newTup = []
                    for i in range(len(elem)):
                        if mapsFromFunctionTuple[i]:
                            newTup.append(elem[i].createFunctionFromList())
                        else:
                            newTup.append(elem[i])

                    newListOfElements.append(tuple(newTup))

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                    else:
                        raise NotDefinedError
            elif any(mapsFromFunctionTuple) and any(mapsToFunctionTuple):
                newListOfElements = []
                for elem in self.listOfElements:
                    newTup = []
                    for i in range(len(elem)):
                        if mapsFromFunctionTuple[i]:
                            newTup.append(elem[i].createFunctionFromList())
                        else:
                            newTup.append(elem[i])

                    newListOfElements.append(tuple(newTup))

                def newFunction(x):
                    if x in newListOfElements:
                        tup = self.listOfValues[newListOfElements.index(x)]
                        for i in range(len(tup)):
                            if tup[i] is not None and mapsToFunctionTuple[i]:
                                tup[i] = tup[i].createFunctionFromList()
                        return tup
                    else:
                        raise NotDefinedError()
            elif any(mapsFromFunctionTuple) and mapsToFunctionSet:
                newListOfElements = []
                for elem in self.listOfElements:
                    newTup = []
                    for i in range(len(elem)):
                        if mapsFromFunctionTuple[i]:
                            newTup.append(elem[i].createFunctionFromList())
                        else:
                            newTup.append(elem[i])

                    newListOfElements.append(tuple(newTup))

                def newFunction(x):
                    if x in newListOfElements:
                        oldSet = self.listOfValues[newListOfElements.index(x)]
                        newSet = []
                        for elem in oldSet:
                            newSet.append(elem.createFunctionFromList())
                        return frozenset(newSet)
                    else:
                        raise NotDefinedError()
            elif mapsFromFunctionSet and mapsToFunction:
                newListOfElements = []
                for elem in self.listOfElements:
                    newSet = []
                    for innerElem in elem:
                        newSet.append(innerElem.createFunctionFromList())
                    newListOfElements.append(frozenset(newSet))

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                    else:
                        raise NotDefinedError
            elif mapsFromFunctionSet and any(mapsToFunctionTuple):
                newListOfElements = []
                for elem in self.listOfElements:
                    newSet = []
                    for innerElem in elem:
                        newSet.append(innerElem.createFunctionFromList())
                    newListOfElements.append(frozenset(newSet))

                def newFunction(x):
                    if x in newListOfElements:
                        tup = self.listOfValues[newListOfElements.index(x)]
                        for i in range(len(tup)):
                            if tup[i] is not None and mapsToFunctionTuple[i]:
                                tup[i] = tup[i].createFunctionFromList()
                        return tup
                    else:
                        raise NotDefinedError()
            elif mapsFromFunctionSet and mapsToFunctionSet:
                newListOfElements = []
                for elem in self.listOfElements:
                    newSet = []
                    for innerElem in elem:
                        newSet.append(innerElem.createFunctionFromList())
                    newListOfElements.append(frozenset(newSet))

                def newFunction(x):
                    if x in newListOfElements:
                        oldSet = self.listOfValues[newListOfElements.index(x)]
                        newSet = []
                        for elem in oldSet:
                            newSet.append(elem.createFunctionFromList())
                        return frozenset(newSet)
                    else:
                        raise NotDefinedError()
            elif mapsToFunction:
                def newFunction(x):
                    if x in self.listOfElements:
                        return self.listOfValues[self.listOfElements.index(x)].createFunctionFromList()
                    else:
                        raise NotDefinedError()
            elif any(mapsToFunctionTuple):
                def newFunction(x):
                    if x in newListOfElements:
                        tup = self.listOfValues[newListOfElements.index(x)]
                        for i in range(len(tup)):
                            if tup[i] is not None and mapsToFunctionTuple[i]:
                                tup[i] = tup[i].createFunctionFromList()
                        return tup
                    else:
                        raise NotDefinedError()
            elif mapsToFunctionSet:
                def newFunction(x):
                    if x in self.listOfElements:
                        oldSet = self.listOfValues[self.listOfElements.index(x)]
                        newSet = []
                        for elem in oldSet:
                            newSet.append(elem.createFunctionFromList())
                        return frozenset(newSet)
                    else:
                        raise NotDefinedError()
            elif mapsFromFunction:
                newListOfElements = []
                for elem in self.listOfElements:
                    newListOfElements.append(elem.createFunctionFromList())

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)]
                    else:
                        raise NotDefinedError()
            elif any(mapsFromFunctionTuple):
                newListOfElements = []
                for elem in self.listOfElements:
                    newTup = []
                    for i in range(len(elem)):
                        if mapsFromFunctionTuple[i]:
                            newTup.append(elem[i].createFunctionFromList())
                        else:
                            newTup.append(elem[i])

                    newListOfElements.append(tuple(newTup))

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)]
                    else:
                        raise NotDefinedError()
            elif mapsFromFunctionSet:
                newListOfElements = []
                for elem in self.listOfElements:
                    newSet = []
                    for innerElem in elem:
                        newSet.append(innerElem.createFunctionFromList())
                    newListOfElements.append(frozenset(newSet))

                def newFunction(x):
                    if x in newListOfElements:
                        return self.listOfValues[newListOfElements.index(x)]
                    else:
                        raise NotDefinedError()
            else:
                def newFunction(x):
                    if x in self.listOfElements:
                        return self.listOfValues[self.listOfElements.index(x)]
                    else:
                        raise NotDefinedError()

            FPTMapping.dictOfFPTMappings[self.name] = self
            FPTMapping.dictOfMappings[self.name] = newFunction
        return newFunction

    def recreateFunctionFromList(self):
        # mapsFromFunction = False
        # for elem in self.listOfElements:
        #     mapsFromFunction = type(elem) == FPTMapping
        #     break
        #
        # mapsFromFunctionTuple = False
        # for elem in self.listOfElements:
        #     if type(elem) == tuple:
        #         mapsFromFunctionTuple = type(elem[0]) == FPTMapping
        #         break
        #     break
        #
        # mapsFromFunctionSet = False
        # for elem in self.listOfElements:
        #     if type(elem) == frozenset:
        #         done = False
        #         for innerElem in elem:
        #             mapsFromFunctionSet = type(innerElem) == FPTMapping
        #             done = True
        #             break
        #         if done:
        #             break
        #     else:
        #         break
        #
        # mapsToFunction = False
        # for elem in self.listOfValues:
        #     mapsToFunction = type(elem) == FPTMapping
        #     break
        #
        # mapsToFunctionTuple = False
        # for elem in self.listOfValues:
        #     if type(elem) == tuple:
        #         mapsToFunctionTuple = type(elem[0]) == FPTMapping
        #         break
        #     break
        #
        # mapsToFunctionSet = False
        # for elem in self.listOfValues:
        #     if type(elem) == frozenset:
        #         done = False
        #         for innerElem in elem:
        #             mapsToFunctionSet = type(innerElem) == FPTMapping
        #             done = True
        #             break
        #         if done:
        #             break
        #     else:
        #         break
        #
        # if mapsFromFunction and mapsToFunction:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newListOfElements.append(elem.createFunctionFromList())
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
        #         else:
        #             raise NotDefinedError
        # elif mapsFromFunction and mapsToFunctionTuple:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newListOfElements.append(elem.createFunctionFromList())
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             tup = self.listOfValues[newListOfElements.index(x)]
        #             if tup[0] is not None:
        #                 tup[0] = tup[0].createFunctionFromList()
        #             if tup[1] is not None:
        #                 tup[1] = tup[1].createFunctionFromList()
        #             return tup
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunction and mapsToFunctionSet:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newListOfElements.append(elem.createFunctionFromList())
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             oldSet = self.listOfValues[newListOfElements.index(x)]
        #             newSet = []
        #             for elem in oldSet:
        #                 newSet.append(elem.createFunctionFromList())
        #             return frozenset(newSet)
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionTuple and mapsToFunction:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         elem0 = elem[0].createFunctionFromList()
        #         elem1 = elem[1].createFunctionFromList()
        #         newListOfElements.append(tuple([elem0, elem1]))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
        #         else:
        #             raise NotDefinedError
        # elif mapsFromFunctionTuple and mapsToFunctionTuple:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         elem0 = elem[0].createFunctionFromList()
        #         elem1 = elem[1].createFunctionFromList()
        #         newListOfElements.append(tuple([elem0, elem1]))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             tup = self.listOfValues[newListOfElements.index(x)]
        #             if tup[0] is not None:
        #                 tup[0] = tup[0].createFunctionFromList()
        #             if tup[1] is not None:
        #                 tup[1] = tup[1].createFunctionFromList()
        #             return tup
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionTuple and mapsToFunctionSet:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         elem0 = elem[0].createFunctionFromList()
        #         elem1 = elem[1].createFunctionFromList()
        #         newListOfElements.append(tuple([elem0, elem1]))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             oldSet = self.listOfValues[newListOfElements.index(x)]
        #             newSet = []
        #             for elem in oldSet:
        #                 newSet.append(elem.createFunctionFromList())
        #             return frozenset(newSet)
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionSet and mapsToFunction:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newSet = []
        #         for innerElem in elem:
        #             newSet.append(innerElem.createFunctionFromList())
        #         newListOfElements.append(frozenset(newSet))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
        #         else:
        #             raise NotDefinedError
        # elif mapsFromFunctionSet and mapsToFunctionTuple:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newSet = []
        #         for innerElem in elem:
        #             newSet.append(innerElem.createFunctionFromList())
        #         newListOfElements.append(frozenset(newSet))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             tup = self.listOfValues[newListOfElements.index(x)]
        #             if tup[0] is not None:
        #                 tup[0] = tup[0].createFunctionFromList()
        #             if tup[1] is not None:
        #                 tup[1] = tup[1].createFunctionFromList()
        #             return tup
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionSet and mapsToFunctionSet:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newSet = []
        #         for innerElem in elem:
        #             newSet.append(innerElem.createFunctionFromList())
        #         newListOfElements.append(frozenset(newSet))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             oldSet = self.listOfValues[newListOfElements.index(x)]
        #             newSet = []
        #             for elem in oldSet:
        #                 newSet.append(elem.createFunctionFromList())
        #             return frozenset(newSet)
        #         else:
        #             raise NotDefinedError()
        # elif mapsToFunction:
        #     def newFunction(x):
        #         if x in self.listOfElements:
        #             return self.listOfValues[self.listOfElements.index(x)].createFunctionFromList()
        #         else:
        #             raise NotDefinedError()
        # elif mapsToFunctionTuple:
        #     def newFunction(x):
        #         if x in self.listOfElements:
        #             tup = self.listOfValues[self.listOfElements.index(x)]
        #             if tup[0] is not None:
        #                 tup[0] = tup[0].createFunctionFromList()
        #             if tup[1] is not None:
        #                 tup[1] = tup[1].createFunctionFromList()
        #             return tup
        #         else:
        #             raise NotDefinedError()
        # elif mapsToFunctionSet:
        #     def newFunction(x):
        #         if x in self.listOfElements:
        #             oldSet = self.listOfValues[self.listOfElements.index(x)]
        #             newSet = []
        #             for elem in oldSet:
        #                 newSet.append(elem.createFunctionFromList())
        #             return frozenset(newSet)
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunction:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newListOfElements.append(elem.createFunctionFromList())
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)]
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionTuple:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         elem0 = elem[0].createFunctionFromList()
        #         elem1 = elem[1].createFunctionFromList()
        #         newListOfElements.append(tuple([elem0, elem1]))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)]
        #         else:
        #             raise NotDefinedError()
        # elif mapsFromFunctionSet:
        #     newListOfElements = []
        #     for elem in self.listOfElements:
        #         newSet = []
        #         for innerElem in elem:
        #             newSet.append(innerElem.createFunctionFromList())
        #         newListOfElements.append(frozenset(newSet))
        #
        #     def newFunction(x):
        #         if x in newListOfElements:
        #             return self.listOfValues[newListOfElements.index(x)]
        #         else:
        #             raise NotDefinedError()
        # else:
        #     def newFunction(x):
        #         if x in self.listOfElements:
        #             return self.listOfValues[self.listOfElements.index(x)]
        #         else:
        #             raise NotDefinedError()
        mapsFromFunction = False
        for elem in self.listOfElements:
            mapsFromFunction = type(elem) == FPTMapping
            break

        mapsFromFunctionTuple = []
        for elem in self.listOfElements:
            if type(elem) == tuple:
                mapsFromFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem]
                # mapsFromFunctionTuple = type(elem[0]) == FPTMapping
                break
            break

        mapsFromFunctionSet = False
        for elem in self.listOfElements:
            if type(elem) == frozenset:
                done = False
                for innerElem in elem:
                    mapsFromFunctionSet = type(innerElem) == FPTMapping
                    done = True
                    break
                if done:
                    break
            else:
                break

        mapsToFunction = False
        for elem in self.listOfValues:
            mapsToFunction = type(elem) == FPTMapping
            break

        mapsToFunctionTuple = [False]
        for elem in self.listOfValues:
            if type(elem) == tuple:
                mapsToFunctionTuple = [type(innerElem) == FPTMapping for innerElem in elem]
                # mapsToFunctionTuple = type(elem[0]) == FPTMapping
                break
            break

        mapsToFunctionSet = False
        for elem in self.listOfValues:
            if type(elem) == frozenset:
                done = False
                for innerElem in elem:
                    mapsToFunctionSet = type(innerElem) == FPTMapping
                    done = True
                    break
                if done:
                    break
            else:
                break

        if mapsFromFunction and mapsToFunction:
            newListOfElements = []
            for elem in self.listOfElements:
                newListOfElements.append(elem.createFunctionFromList())

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                else:
                    raise NotDefinedError
        elif mapsFromFunction and any(mapsToFunctionTuple):
            newListOfElements = []
            for elem in self.listOfElements:
                newListOfElements.append(elem.createFunctionFromList())

            def newFunction(x):
                if x in newListOfElements:
                    tup = self.listOfValues[newListOfElements.index(x)]
                    for i in range(len(tup)):
                        if tup[i] is not None and mapsToFunctionTuple[i]:
                            tup[i] = tup[i].createFunctionFromList()
                    return tup
                else:
                    raise NotDefinedError()
        elif mapsFromFunction and mapsToFunctionSet:
            newListOfElements = []
            for elem in self.listOfElements:
                newListOfElements.append(elem.createFunctionFromList())

            def newFunction(x):
                if x in newListOfElements:
                    oldSet = self.listOfValues[newListOfElements.index(x)]
                    newSet = []
                    for elem in oldSet:
                        newSet.append(elem.createFunctionFromList())
                    return frozenset(newSet)
                else:
                    raise NotDefinedError()
        elif any(mapsFromFunctionTuple) and mapsToFunction:
            newListOfElements = []
            for elem in self.listOfElements:
                newTup = []
                for i in range(len(elem)):
                    if mapsFromFunctionTuple[i]:
                        newTup.append(elem[i].createFunctionFromList())
                    else:
                        newTup.append(elem[i])

                newListOfElements.append(tuple(newTup))

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                else:
                    raise NotDefinedError
        elif any(mapsFromFunctionTuple) and any(mapsToFunctionTuple):
            newListOfElements = []
            for elem in self.listOfElements:
                newTup = []
                for i in range(len(elem)):
                    if mapsFromFunctionTuple[i]:
                        newTup.append(elem[i].createFunctionFromList())
                    else:
                        newTup.append(elem[i])

                newListOfElements.append(tuple(newTup))

            def newFunction(x):
                if x in newListOfElements:
                    tup = self.listOfValues[newListOfElements.index(x)]
                    for i in range(len(tup)):
                        if tup[i] is not None and mapsToFunctionTuple[i]:
                            tup[i] = tup[i].createFunctionFromList()
                    return tup
                else:
                    raise NotDefinedError()
        elif any(mapsFromFunctionTuple) and mapsToFunctionSet:
            newListOfElements = []
            for elem in self.listOfElements:
                newTup = []
                for i in range(len(elem)):
                    if mapsFromFunctionTuple[i]:
                        newTup.append(elem[i].createFunctionFromList())
                    else:
                        newTup.append(elem[i])

                newListOfElements.append(tuple(newTup))

            def newFunction(x):
                if x in newListOfElements:
                    oldSet = self.listOfValues[newListOfElements.index(x)]
                    newSet = []
                    for elem in oldSet:
                        newSet.append(elem.createFunctionFromList())
                    return frozenset(newSet)
                else:
                    raise NotDefinedError()
        elif mapsFromFunctionSet and mapsToFunction:
            newListOfElements = []
            for elem in self.listOfElements:
                newSet = []
                for innerElem in elem:
                    newSet.append(innerElem.createFunctionFromList())
                newListOfElements.append(frozenset(newSet))

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)].createFunctionFromList()
                else:
                    raise NotDefinedError
        elif mapsFromFunctionSet and any(mapsToFunctionTuple):
            newListOfElements = []
            for elem in self.listOfElements:
                newSet = []
                for innerElem in elem:
                    newSet.append(innerElem.createFunctionFromList())
                newListOfElements.append(frozenset(newSet))

            def newFunction(x):
                if x in newListOfElements:
                    tup = self.listOfValues[newListOfElements.index(x)]
                    for i in range(len(tup)):
                        if tup[i] is not None and mapsToFunctionTuple[i]:
                            tup[i] = tup[i].createFunctionFromList()
                    return tup
                else:
                    raise NotDefinedError()
        elif mapsFromFunctionSet and mapsToFunctionSet:
            newListOfElements = []
            for elem in self.listOfElements:
                newSet = []
                for innerElem in elem:
                    newSet.append(innerElem.createFunctionFromList())
                newListOfElements.append(frozenset(newSet))

            def newFunction(x):
                if x in newListOfElements:
                    oldSet = self.listOfValues[newListOfElements.index(x)]
                    newSet = []
                    for elem in oldSet:
                        newSet.append(elem.createFunctionFromList())
                    return frozenset(newSet)
                else:
                    raise NotDefinedError()
        elif mapsToFunction:
            def newFunction(x):
                if x in self.listOfElements:
                    return self.listOfValues[self.listOfElements.index(x)].createFunctionFromList()
                else:
                    raise NotDefinedError()
        elif any(mapsToFunctionTuple):
            def newFunction(x):
                if x in newListOfElements:
                    tup = self.listOfValues[newListOfElements.index(x)]
                    for i in range(len(tup)):
                        if tup[i] is not None and mapsToFunctionTuple[i]:
                            tup[i] = tup[i].createFunctionFromList()
                    return tup
                else:
                    raise NotDefinedError()
        elif mapsToFunctionSet:
            def newFunction(x):
                if x in self.listOfElements:
                    oldSet = self.listOfValues[self.listOfElements.index(x)]
                    newSet = []
                    for elem in oldSet:
                        newSet.append(elem.createFunctionFromList())
                    return frozenset(newSet)
                else:
                    raise NotDefinedError()
        elif mapsFromFunction:
            newListOfElements = []
            for elem in self.listOfElements:
                newListOfElements.append(elem.createFunctionFromList())

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)]
                else:
                    raise NotDefinedError()
        elif any(mapsFromFunctionTuple):
            newListOfElements = []
            for elem in self.listOfElements:
                newTup = []
                for i in range(len(elem)):
                    if mapsFromFunctionTuple[i]:
                        newTup.append(elem[i].createFunctionFromList())
                    else:
                        newTup.append(elem[i])

                newListOfElements.append(tuple(newTup))

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)]
                else:
                    raise NotDefinedError()
        elif mapsFromFunctionSet:
            newListOfElements = []
            for elem in self.listOfElements:
                newSet = []
                for innerElem in elem:
                    newSet.append(innerElem.createFunctionFromList())
                newListOfElements.append(frozenset(newSet))

            def newFunction(x):
                if x in newListOfElements:
                    return self.listOfValues[newListOfElements.index(x)]
                else:
                    raise NotDefinedError()
        else:
            def newFunction(x):
                if x in self.listOfElements:
                    return self.listOfValues[self.listOfElements.index(x)]
                else:
                    raise NotDefinedError()

        FPTMapping.dictOfFPTMappings[self.name] = self
        FPTMapping.dictOfMappings[self.name] = newFunction
        return newFunction

    def calculateListOfTuples(self):
        if self.name in FPTMapping.dictOfFPTMappings.keys():
            self.inputSetName = FPTMapping.dictOfFPTMappings[self.name].inputSetName
            self.outputSetName = FPTMapping.dictOfFPTMappings[self.name].outputSetName
            self.inputMV = FPTMapping.dictOfFPTMappings[self.name].inputMV
            self.inputMVK = FPTMapping.dictOfFPTMappings[self.name].inputMVK
            self.outputMV = FPTMapping.dictOfFPTMappings[self.name].outputMV
            self.outputMVK = FPTMapping.dictOfFPTMappings[self.name].outputMVK

            self.listOfTuples = FPTMapping.dictOfFPTMappings[self.name].listOfTuples
            self.listOfElements = []
            self.listOfValues = []
            for tup in self.listOfTuples:
                self.listOfElements.append(tup[0])
                self.listOfValues.append(tup[1])

            self.calculateTypes()
        else:
            if self not in FPTMapping.listOfInvalidFPTMappings:
                FPTMapping.listOfInvalidFPTMappings.append(self)
            print("WARNING: Tried to access non-existing FPTMapping:  ", self.name)
            return None

    def calculateMappingType(self):
        if self.name in FPTMapping.dictOfFPTMappings.keys():
            self.mappingType = FPTMapping.dictOfFPTMappings[self.name].mappingType
        else:
            if self not in FPTMapping.listOfInvalidFPTMappings:
                FPTMapping.listOfInvalidFPTMappings.append(self)
            print("WARNING: Tried to access non-existing FPTMapping:  ", self.name)
            return None

    def calculateTypes(self):
        for elem in self.listOfElements:
            self.inputType = type(elem)
            if self.inputType == int: self.inputType = float
            break
        for elem in self.listOfValues:
            self.outputType = type(elem)
            if self.outputType == int: self.outputType = float
            break

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __members(self):
        return self.name

    def __eq__(self, other):
        if type(other) is type(self):
            return self.__members() == other.__members()
        else:
            return False

    def __lt__(self, other):
        if type(other) is type(self):
            return self.__members() < other.__members()
        else:
            return False

    def __hash__(self):
        return hash(self.__members())
