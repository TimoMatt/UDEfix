from json import dumps, loads, JSONEncoder, JSONDecoder
from collections import OrderedDict
from itertools import chain, combinations
from PyQt5.QtCore import *

from fixpointtool.content.fpt_mapping import FPTMapping, NotDefinedError
from fixpointtool.content.fpt_relation import FPTRelation
from fixpointtool.content.fpt_set import FPTSet
from nodeeditor.utils import dumpException

DEBUG = False

dict_of_mappings = {

}

dict_of_relations = {

}

dict_of_sets = {

}

DICT_OF_DICTS = {
    "mappings": dict_of_mappings,
    "relations": dict_of_relations,
    "sets": dict_of_sets
}


class PythonObjectEncoder(JSONEncoder):
    def encode(self, obj):
        def hint_datatypes(item):
            if isinstance(item, tuple):
                return {'__tuple__': True, 'items': [hint_datatypes(it) for it in item]}
            if isinstance(item, (frozenset, set)):
                return {'__set__': True, 'items': [hint_datatypes(e) for e in item]}
            if isinstance(item, list):
                return [hint_datatypes(e) for e in item]
            if isinstance(item, FPTMapping):
                if item.isNew:
                    if item.inputSetName is not None and item.outputSetName is not None:
                        return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                'input_set_name': item.inputSetName, 'output_set_name': item.outputSetName,
                                'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                    elif item.inputSetName is not None:
                        if item.outputMV is not None:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'input_set_name': item.inputSetName,
                                    'output_mv': item.outputMV, 'output_mv_k': item.outputMVK,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                        else:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'input_set_name': item.inputSetName,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                    elif item.outputSetName is not None:
                        if item.inputMV is not None:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'output_set_name': item.outputSetName,
                                    'input_mv': item.inputMV, 'input_mv_k': item.inputMVK,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                        else:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'output_set_name': item.outputSetName,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                    else:
                        if item.inputMV is not None and item.outputMV is not None:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'input_mv': item.inputMV, 'input_mv_k': item.inputMVK,
                                    'output_mv': item.outputMV, 'output_mv_k': item.outputMVK,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                        elif item.inputMV is not None:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'input_mv': item.inputMV, 'input_mv_k': item.inputMVK,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                        elif item.outputMV is not None:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'output_mv': item.outputMV, 'output_mv_k': item.outputMVK,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                        else:
                            return {'__func__': True, 'name': item.name, 'type': item.mappingType,
                                    'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.listOfTuples]}
                else:
                    return {'__func__': True, 'name': item.name}
            if isinstance(item, FPTRelation):
                if item.type == "custom" or item.type == "is-element-of":
                    return {'__relation__': True,
                            'name': item.name,
                            'type': item.type,
                            'input_set_name': item.input_set_name,
                            'output_set_name': item.output_set_name,
                            'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.relation]}
                elif item.type == "projection":
                    return {'__relation__': True,
                            'name': item.name,
                            'type': item.type,
                            'projection_type': item.projection_type,
                            'input_set_name': item.input_set_name,
                            'output_set_name': item.output_set_name,
                            'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.relation]}
                else:
                    return {'__relation__': True,
                            'name': item.name,
                            'type': item.type,
                            'input_set_name': item.input_set_name,
                            'items': [hint_datatypes(tuple([x, y])) for [x, y] in item.relation]}

            if isinstance(item, dict):
                return {key: hint_datatypes(value) for key, value in item.items()}
            else:
                return item

        return super(PythonObjectEncoder, self).encode(hint_datatypes(obj))


def hinted_datatype_hook(obj):
    if '__tuple__' in obj:
        return tuple(obj['items'])
    elif '__set__' in obj:
        return frozenset(obj['items'])
    elif '__func__' in obj:
        if 'items' in obj:
            if 'input_set_name' in obj and 'output_set_name' in obj:
                return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], input_set_name=obj['input_set_name'], output_set_name=obj['output_set_name'])
            elif 'input_set_name' in obj:
                if 'output_mv' in obj:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], input_set_name=obj['input_set_name'], output_mv=obj['output_mv'], output_mv_k=obj['output_mv_k'])
                else:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], input_set_name=obj['input_set_name'])
            elif 'output_set_name' in obj:
                if 'input_mv' in obj:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], output_set_name=obj['output_set_name'], input_mv=obj['input_mv'], input_mv_k=obj['input_mv_k'])
                else:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], output_set_name=obj['output_set_name'])
            else:
                if 'input_mv' in obj and 'output_mv' in obj:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], input_mv=obj['input_mv'], input_mv_k=obj['input_mv_k'], output_mv=obj['output_mv'], output_mv_k=obj['output_mv_k'])
                elif 'input_mv' in obj:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], input_mv=obj['input_mv'], input_mv_k=obj['input_mv_k'])
                elif 'output_mv' in obj:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'], output_mv=obj['output_mv'], output_mv_k=obj['output_mv_k'])
                else:
                    return FPTMapping(obj['name'], [[x, y] for (x, y) in obj['items']], obj['type'])
        else:
            return FPTMapping(obj['name'])
    elif '__relation__' in obj:
        if 'projection_type' in obj:
            return FPTRelation(obj['name'], frozenset([(x, y) for (x, y) in obj['items']]), obj['input_set_name'],
                               obj['output_set_name'], type=obj['type'], projection_type=obj['projection_type'])
        else:
            return FPTRelation(obj['name'], frozenset([(x, y) for (x, y) in obj['items']]), obj['input_set_name'],
                               obj['output_set_name'], obj['type'])
    else:
        return obj


class AccessDictionaries(QObject):

    def getDictionary(self, dict):
        if dict in DICT_OF_DICTS.keys():
            newDict = OrderedDict(sorted(DICT_OF_DICTS[dict].items()))
            for key in newDict.keys():
                if type(newDict[key]) == FPTMapping:
                    newDict[key] = newDict[key].createFunctionFromList()
                elif type(newDict[key]) == FPTRelation:
                    newDict[key] = newDict[key].getRelation()
                elif type(newDict[key]) == set or type(newDict[key]) == frozenset:
                    hasFunctions = False
                    for elem in newDict[key]:
                        hasFunctions = type(elem) == FPTMapping
                        break

                    hasTupleOfFunctions = []
                    for elem in newDict[key]:
                        if type(elem) == tuple:
                            hasTupleOfFunctions = [type(innerElem) == FPTMapping for innerElem in elem]
                            # hasTupleOfFunctions = type(elem[0]) == FPTMapping
                        else:
                            break

                    hasSetOfFunctions = False
                    for elem in newDict[key]:
                        if type(elem) == frozenset or type(elem) == set:
                            done = False
                            for innerElem in elem:
                                hasSetOfFunctions = type(innerElem) == FPTMapping
                                done = True
                                break
                            if done:
                                break
                        else:
                            break

                    if hasFunctions:
                        newSet = frozenset([elem.createFunctionFromList() for elem in newDict[key]])
                        newDict[key] = newSet
                    elif hasTupleOfFunctions:
                        newSet = []
                        for elem in newDict[key]:
                            tup = []
                            for i in range(len(hasTupleOfFunctions)):
                                if hasTupleOfFunctions[i]:
                                    tup.append(elem[i].createFunctionFromList())
                                else:
                                    tup.append(elem[i])
                            # newSet.append(tuple([elem[0].createFunctionFromList(), elem[1].createFunctionFromList()]))
                            newSet.append(tuple(tup))
                        newDict[key] = frozenset(newSet)
                    elif hasSetOfFunctions:
                        newSet = []
                        for elem in newDict[key]:
                            newSet.append(frozenset([innerElem.createFunctionFromList() for innerElem in elem]))
                        newDict[key] = frozenset(newSet)

            return newDict
        else:
            print("WARNING: Tried to access a non-existing dictionary")
            return None

    def getDictionaryWithoutTransformation(self, dict):
        if dict in DICT_OF_DICTS.keys():
            newDict = OrderedDict(sorted(DICT_OF_DICTS[dict].items()))
            return newDict
        else:
            print("WARNING: Tried to access a non-existing dictionary")
            return None

    def addElementToDictionary(self, dict, key, value):
        if dict in DICT_OF_DICTS.keys():
            if DEBUG: print(DICT_OF_DICTS[dict])
            DICT_OF_DICTS[dict][key] = value
            if DEBUG: print(DICT_OF_DICTS[dict])
        else:
            print("WARNING: Tried to access a non-existing dictionary")

    def deleteElementFromDictionary(self, dict, key):
        if dict in DICT_OF_DICTS.keys():
            if DEBUG: print(DICT_OF_DICTS[dict])
            DICT_OF_DICTS[dict].pop(key)
            if DEBUG: print(DICT_OF_DICTS[dict])
        else:
            print("WARNING: Tried to access a non-existing dictionary")

    def saveDictionariesInJSONFile(self, filename):
        with open(filename, "w") as file:
            try:
                file.write(dumps(DICT_OF_DICTS, cls=PythonObjectEncoder, indent=4))
            except Exception as e:
                dumpException(e)

    def power_set(self, Y):
        s = list(Y)
        temp = chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))
        return set(frozenset(i) for i in temp)

    def u(self, C):
        return frozenset(x for (x, y) in C), frozenset(y for (x, y) in C)

    def updateRelationsAndMappingsFromSetChange(self, old_name, new_name=None, deleted=False):
        if new_name is None and deleted:
            toBeDeleted = []
            for function in DICT_OF_DICTS["mappings"]:
                funcObject = DICT_OF_DICTS["mappings"][function]
                if funcObject.inputSetName == old_name or funcObject.outputSetName == old_name:
                    toBeDeleted.append(function)
            for function in toBeDeleted:
                DICT_OF_DICTS["mappings"].pop(function)

            toBeDeleted = []
            for relation in DICT_OF_DICTS["relations"]:
                relObject = DICT_OF_DICTS["relations"][relation]
                if relObject.input_set_name == old_name or relObject.output_set_name == old_name:
                    toBeDeleted.append(relation)
            for relation in toBeDeleted:
                DICT_OF_DICTS["relations"].pop(relation)
        else:
            for function in DICT_OF_DICTS["mappings"]:
                funcObject = DICT_OF_DICTS["mappings"][function]
                if funcObject.inputSetName == old_name and funcObject.outputSetName == old_name:
                    if new_name is not None:
                        funcObject.inputSetName = new_name
                        funcObject.outputSetName = new_name

                    inp_out_set = list(DICT_OF_DICTS["sets"][funcObject.inputSetName])
                    if len(inp_out_set) == 0:
                        newListOfTuples = []
                    elif len(funcObject.listOfTuples) == 0:
                        continue
                    else:
                        sameType = True
                        if isinstance(inp_out_set[0], type(funcObject.listOfElements[0])) and isinstance(inp_out_set[0], type(funcObject.listOfValues[0])):
                            if type(inp_out_set[0]) == tuple or type(inp_out_set[0]) == set or type(inp_out_set[0]) == frozenset:
                                if isinstance(list(inp_out_set[0])[0], type(list(funcObject.listOfElements[0])[0])) and isinstance(list(inp_out_set[0])[0], type(list(funcObject.listOfValues[0])[0])):
                                    pass
                                else:
                                    sameType = False
                        else:
                            sameType = False

                        if sameType:
                            hasFunctions = False
                            for elem in inp_out_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in inp_out_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in inp_out_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_inp_out_set = [x.createFunctionFromList() for x in inp_out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if x.createFunctionFromList() in transformed_inp_out_set and y.createFunctionFromList() in transformed_inp_out_set]
                            elif hasTupleOfFunctions:
                                transformed_inp_out_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in inp_out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if (x[0].createFunctionFromList(), x[1].createFunctionFromList()) in transformed_inp_out_set and (y[0].createFunctionFromList(), y[1].createFunctionFromList()) in transformed_inp_out_set]
                            elif hasSetOfFunctions:
                                transformed_inp_out_set = [frozenset([x.createFunctionFromList() for x in s]) for s in inp_out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if frozenset([elem.createFunctionFromList() for elem in x]) in transformed_inp_out_set and frozenset([elem.createFunctionFromList() for elem in y]) in transformed_inp_out_set]
                            else:
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if x in inp_out_set and y in inp_out_set]
                        else:
                            newListOfTuples = []

                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType,
                                         funcObject.inputSetName, funcObject.outputSetName)
                    newFunc.recreateFunctionFromList()
                    self.addElementToDictionary("mappings", funcObject.name, newFunc)

                elif funcObject.inputSetName == old_name:
                    if new_name is not None:
                        funcObject.inputSetName = new_name

                    inp_set = list(DICT_OF_DICTS["sets"][funcObject.inputSetName])
                    if len(inp_set) == 0:
                        newListOfTuples = []
                    elif len(funcObject.listOfTuples) == 0:
                        continue
                    else:
                        sameType = True
                        if isinstance(inp_set[0], type(funcObject.listOfElements[0])):
                            if type(inp_set[0]) == tuple or type(inp_set[0]) == set or type(inp_set[0]) == frozenset:
                                if isinstance(list(inp_set[0])[0], type(list(funcObject.listOfElements[0])[0])):
                                    pass
                                else:
                                    sameType = False
                        else:
                            sameType = False

                        if sameType:
                            hasFunctions = False
                            for elem in inp_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in inp_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in inp_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_inp_set = [x.createFunctionFromList() for x in inp_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if x.createFunctionFromList() in transformed_inp_set]
                            elif hasTupleOfFunctions:
                                transformed_inp_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in inp_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if (x[0].createFunctionFromList(), x[1].createFunctionFromList()) in transformed_inp_set]
                            elif hasSetOfFunctions:
                                transformed_inp_set = [frozenset([x.createFunctionFromList() for x in s]) for s in inp_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if frozenset([elem.createFunctionFromList() for elem in x]) in transformed_inp_set]
                            else:
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if x in inp_set]
                        else:
                            newListOfTuples = []

                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType,
                                         funcObject.inputSetName, funcObject.outputSetName)
                    newFunc.recreateFunctionFromList()
                    self.addElementToDictionary("mappings", funcObject.name, newFunc)

                elif funcObject.outputSetName == old_name:
                    if new_name is not None:
                        funcObject.outputSetName = new_name

                    out_set = list(DICT_OF_DICTS["sets"][funcObject.outputSetName])
                    if len(out_set) == 0:
                        newListOfTuples = []
                    elif len(funcObject.listOfTuples) == 0:
                        continue
                    else:
                        sameType = True
                        if isinstance(out_set[0], type(funcObject.listOfValues[0])):
                            if type(out_set[0]) == tuple or type(out_set[0]) == set or type(out_set[0]) == frozenset:
                                if isinstance(list(out_set[0])[0], type(list(funcObject.listOfValues[0])[0])):
                                    pass
                                else:
                                    sameType = False
                        else:
                            sameType = False

                        if sameType:
                            hasFunctions = False
                            for elem in out_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in out_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in out_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_out_set = [x.createFunctionFromList() for x in out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if y.createFunctionFromList() in transformed_out_set]
                            elif hasTupleOfFunctions:
                                transformed_out_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if (y[0].createFunctionFromList(), y[1].createFunctionFromList()) in transformed_out_set]
                            elif hasSetOfFunctions:
                                transformed_out_set = [frozenset([x.createFunctionFromList() for x in s]) for s in out_set]
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if frozenset([elem.createFunctionFromList() for elem in y]) in transformed_out_set]
                            else:
                                newListOfTuples = [[x, y] for [x, y] in funcObject.listOfTuples if y in out_set]
                        else:
                            newListOfTuples = []

                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType,
                                         funcObject.inputSetName, funcObject.outputSetName)
                    newFunc.recreateFunctionFromList()
                    self.addElementToDictionary("mappings", funcObject.name, newFunc)

            for relation in DICT_OF_DICTS["relations"]:
                relObject = DICT_OF_DICTS["relations"][relation]
                if relObject.type == "custom":
                    if relObject.input_set_name == old_name and relObject.output_set_name == old_name:
                        if new_name is not None:
                            relObject.input_set_name = new_name
                            relObject.output_set_name = new_name
                        inp_out_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                        rel = list(relObject.relation)
                        if len(inp_out_set) == 0:
                            relObject.relation = frozenset()
                            continue
                        elif len(rel) == 0:
                            continue
                        elif (not isinstance(inp_out_set[0], type(rel[0][0]))) or (not isinstance(inp_out_set[0], type(rel[0][1]))):
                            relObject.relation = frozenset()
                            continue
                        else:
                            hasFunctions = False
                            for elem in inp_out_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in inp_out_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in inp_out_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_inp_out_set = [x.createFunctionFromList() for x in inp_out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if x.createFunctionFromList() in transformed_inp_out_set and y.createFunctionFromList() in transformed_inp_out_set])
                            elif hasTupleOfFunctions:
                                transformed_inp_out_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in inp_out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if (x[0].createFunctionFromList(), x[1].createFunctionFromList()) in transformed_inp_out_set and (y[0].createFunctionFromList(), y[1].createFunctionFromList()) in transformed_inp_out_set])
                            elif hasSetOfFunctions:
                                transformed_inp_out_set = [frozenset([x.createFunctionFromList() for x in s]) for s in inp_out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if frozenset([elem.createFunctionFromList() for elem in x]) in transformed_inp_out_set and frozenset([elem.createFunctionFromList() for elem in y]) in transformed_inp_out_set])
                            else:
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if x in inp_out_set and y in inp_out_set])

                    elif relObject.input_set_name == old_name:
                        if new_name is not None:
                            relObject.input_set_name = new_name
                        inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                        rel = list(relObject.relation)
                        if len(inp_set) == 0:
                            relObject.relation = frozenset()
                            continue
                        elif len(rel) == 0:
                            continue
                        elif not isinstance(inp_set[0], type(rel[0][0])):
                            relObject.relation = frozenset()
                            continue
                        else:
                            hasFunctions = False
                            for elem in inp_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in inp_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in inp_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_inp_set = [x.createFunctionFromList() for x in inp_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if x.createFunctionFromList() in transformed_inp_set])
                            elif hasTupleOfFunctions:
                                transformed_inp_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in inp_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if (x[0].createFunctionFromList(), x[1].createFunctionFromList()) in transformed_inp_set])
                            elif hasSetOfFunctions:
                                transformed_inp_set = [frozenset([x.createFunctionFromList() for x in s]) for s in inp_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if frozenset([elem.createFunctionFromList() for elem in x]) in transformed_inp_set])
                            else:
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if x in inp_set])

                    elif relObject.output_set_name == old_name:
                        if new_name is not None:
                            relObject.output_set_name = new_name
                        out_set = list(DICT_OF_DICTS["sets"][relObject.output_set_name])
                        rel = list(relObject.relation)
                        if len(out_set) == 0:
                            relObject.relation = frozenset()
                            continue
                        elif len(rel) == 0:
                            continue
                        elif not isinstance(out_set[0], type(rel[0][1])):
                            relObject.relation = frozenset()
                            continue
                        else:
                            hasFunctions = False
                            for elem in out_set:
                                hasFunctions = type(elem) == FPTMapping
                                break

                            hasTupleOfFunctions = False
                            for elem in out_set:
                                if type(elem) == tuple:
                                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                                else:
                                    break

                            hasSetOfFunctions = False
                            for elem in out_set:
                                if type(elem) == frozenset or type(elem) == set:
                                    done = False
                                    for innerElem in elem:
                                        hasSetOfFunctions = type(innerElem) == FPTMapping
                                        done = True
                                        break
                                    if done:
                                        break
                                else:
                                    break

                            if hasFunctions:
                                transformed_out_set = [y.createFunctionFromList() for y in out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if y.createFunctionFromList() in transformed_out_set])
                            elif hasTupleOfFunctions:
                                transformed_out_set = [(tup[0].createFunctionFromList(), tup[1].createFunctionFromList()) for tup in out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if (y[0].createFunctionFromList(), y[1].createFunctionFromList()) in transformed_out_set])
                            elif hasSetOfFunctions:
                                transformed_out_set = [frozenset([y.createFunctionFromList() for y in s]) for s in out_set]
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if frozenset([elem.createFunctionFromList() for elem in y]) in transformed_out_set])
                            else:
                                relObject.relation = frozenset([(x, y) for (x, y) in rel if y in out_set])

                elif relObject.type == "is-element-of":
                    if relObject.input_set_name == old_name or relObject.output_set_name == old_name:
                        if new_name is not None:
                            if relObject.input_set_name == old_name:
                                relObject.input_set_name = new_name
                            if relObject.output_set_name == old_name:
                                relObject.output_set_name = new_name
                        inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                        out_set = list(DICT_OF_DICTS["sets"][relObject.output_set_name])

                        newRelation = []
                        for inputElem in inp_set:
                            for outputElem in out_set:
                                if inputElem in outputElem:
                                    newRelation += [(inputElem, outputElem)]

                        relObject.relation = frozenset(newRelation)

                # elif relObject.type == "is-element-of":
                #     if relObject.input_set_name == old_name:
                #         if new_name is not None:
                #             relObject.input_set_name = new_name
                #         inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #         temp = chain.from_iterable(combinations(inp_set, r) for r in range(len(inp_set) + 1))
                #         out_set = list(frozenset(i) for i in temp)
                #
                #         newRelation = []
                #         for elem in inp_set:
                #             for innerElem in out_set:
                #                 if elem in innerElem:
                #                     newRelation += [(elem, innerElem)]
                #
                #         relObject.relation = frozenset(newRelation)
                elif relObject.type == "projection":
                    if relObject.input_set_name == old_name or relObject.output_set_name == old_name:
                        if new_name is not None:
                            if relObject.input_set_name == old_name:
                                relObject.input_set_name = new_name
                            if relObject.output_set_name == old_name:
                                relObject.output_set_name = new_name
                        inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                        out_set = list(DICT_OF_DICTS["sets"][relObject.output_set_name])

                        if relObject.projection_type == 0:
                            newRelation = []
                            for inputElem in inp_set:
                                for outputElem in out_set:
                                    if inputElem[0] == outputElem:
                                        newRelation += [(inputElem, outputElem)]

                        elif relObject.projection_type == 1:
                            newRelation = []
                            for inputElem in inp_set:
                                for outputElem in out_set:
                                    if inputElem[1] == outputElem:
                                        newRelation += [(inputElem, outputElem)]

                        elif relObject.projection_type == 2:
                            newRelation = []
                            for inputElem in inp_set:
                                x_values = []
                                y_values = []
                                for innerInputElem in inputElem:
                                    x_values.append(innerInputElem[0])
                                    y_values.append(innerInputElem[1])
                                for outputElem in out_set:
                                    if set(x_values) == outputElem[0] and set(y_values) == outputElem[1]:
                                        newRelation += [(inputElem, outputElem)]

                        elif relObject.projection_type == 3:
                            newRelation = []
                            for inputElem in inp_set:
                                x_values = []
                                for innerInputElem in inputElem:
                                    x_values.append(innerInputElem[0])
                                for outputElem in out_set:
                                    if set(x_values) == outputElem:
                                        newRelation += [(inputElem, outputElem)]

                        elif relObject.projection_type == 4:
                            newRelation = []
                            for inputElem in inp_set:
                                y_values = []
                                for innerInputElem in inputElem:
                                    y_values.append(innerInputElem[1])
                                for outputElem in out_set:
                                    if set(y_values) == outputElem:
                                        newRelation += [(inputElem, outputElem)]

                        relObject.relation = frozenset(newRelation)

                # elif relObject.type == "projection":
                #     if relObject.input_set_name == old_name:
                #         if new_name is not None:
                #             relObject.input_set_name = new_name
                #
                #         if relObject.projection_type == 0:
                #             inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #
                #             newRelation = []
                #             for tup in inp_set:
                #                 newRelation += [(tup, tup[0])]
                #         elif relObject.projection_type == 1:
                #             inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #
                #             newRelation = []
                #             for tup in inp_set:
                #                 newRelation += [(tup, tup[1])]
                #         elif relObject.projection_type == 2:
                #             inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #             pow_set = self.power_set(inp_set)
                #
                #             newRelation = []
                #             for tup_set in pow_set:
                #                 newRelation += [(tup_set, (frozenset(x for (x, y) in tup_set), frozenset(y for (x, y) in tup_set)))]
                #
                #         elif relObject.projection_type == 3:
                #             inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #             pow_set = self.power_set(inp_set)
                #
                #             newRelation = []
                #             for tup_set in pow_set:
                #                 newRelation += [(tup_set, frozenset(x for (x, y) in tup_set))]
                #
                #         elif relObject.projection_type == 4:
                #             inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                #             pow_set = self.power_set(inp_set)
                #
                #             newRelation = []
                #             for tup_set in pow_set:
                #                 newRelation += [(tup_set, frozenset(y for (x, y) in tup_set))]
                #
                #         else:
                #             print("WARNING: Projection type does not exist")

                        # inp_set = list(DICT_OF_DICTS["sets"][relObject.input_set_name])
                        # pow_Set = self.power_set(inp_set)
                        # cross_Set = list((x, y) for x in inp_set for y in inp_set)
                        # inp_set = self.power_set(cross_Set)
                        # out_set = list((x, y) for x in pow_Set for y in pow_Set)
                        #
                        # newRelation = []
                        # for inp in inp_set:
                        #     calculatedU = self.u(inp)
                        #     for outp in out_set:
                        #         if calculatedU == outp:
                        #             newRelation += [(inp, outp)]
                        #
                        # relObject.relation = frozenset(newRelation)

    def updateMappings(self, old_name, new_name=None):
        for func in DICT_OF_DICTS["mappings"]:
            funcObject = DICT_OF_DICTS["mappings"][func]
            funcObject.calculateListOfTuples()

            mapsFromFunction = funcObject.inputType == FPTMapping
            mapsToFunction = funcObject.outputType == FPTMapping

            mapsFromFunctionTuple = False
            if funcObject.inputType == tuple:
                for elem in funcObject.listOfElements:
                    mapsFromFunctionTuple = type(elem[0]) == FPTMapping
                    break
            mapsToFunctionTuple = False
            if funcObject.outputType == tuple:
                for elem in funcObject.listOfValues:
                    mapsToFunctionTuple = type(elem[0]) == FPTMapping
                    break

            mapsFromFunctionSet = False
            if funcObject.inputType == frozenset or funcObject.inputType == set:
                for elem in funcObject.listOfElements:
                    done = False
                    for innerElem in elem:
                        mapsFromFunctionSet = type(innerElem) == FPTMapping
                        done = True
                        break
                    if done:
                        break
            mapsToFunctionSet = False
            if funcObject.outputType == frozenset or funcObject.outputType == set:
                for elem in funcObject.listOfValues:
                    done = False
                    for innerElem in elem:
                        mapsToFunctionSet = type(innerElem) == FPTMapping
                        done = True
                        break
                    if done:
                        break

            if mapsFromFunction and mapsToFunction:
                transformed_input = [elem.name for elem in funcObject.listOfElements]
                transformed_output = [elem.name for elem in funcObject.listOfValues]
                if old_name in transformed_input or old_name in transformed_output:
                    newListOfTuples = []
                    for tup in funcObject.listOfTuples:
                        if new_name is not None:
                            if tup[0].name == old_name and tup[1].name == old_name:
                                newElem1 = FPTMapping(new_name)
                                newElem2 = FPTMapping(new_name)
                            elif tup[0].name == old_name:
                                newElem1 = FPTMapping(new_name)
                                newElem2 = tup[1]
                            elif tup[1].name == old_name:
                                newElem1 = tup[0]
                                newElem2 = FPTMapping(new_name)
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        else:
                            if tup[0].name == old_name or tup[1].name == old_name:
                                continue
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        newListOfTuples.append([newElem1, newElem2])
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionTuple and mapsToFunctionTuple:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0][0].name == old_name:
                            newInnerElem11 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem11 = tup[0][0]
                        if tup[0][1].name == old_name:
                            newInnerElem12 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem12 = tup[0][1]
                        if tup[1][0].name == old_name:
                            newInnerElem21 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem21 = tup[1][0]
                        if tup[1][1].name == old_name:
                            newInnerElem22 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem22 = tup[1][1]
                    else:
                        if tup[0][0].name == old_name or tup[0][1].name == old_name or tup[1][0].name == old_name or tup[1][1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newInnerElem11 = tup[0][0]
                            newInnerElem12 = tup[0][1]
                            newInnerElem21 = tup[1][0]
                            newInnerElem22 = tup[1][1]
                    newListOfTuples.append([tuple([newInnerElem11, newInnerElem12]), tuple([newInnerElem21, newInnerElem22])])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionSet and mapsToFunctionSet:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        newSet1 = []
                        newSet2 = []
                        for elem in tup[0]:
                            if elem.name == old_name:
                                newSet1.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet1.append(elem)
                        for elem in tup[1]:
                            if elem.name == old_name:
                                newSet2.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet2.append(elem)
                        newSet1 = frozenset(newSet1)
                        newSet2 = frozenset(newSet2)
                    else:
                        if old_name in [elem.name for elem in tup[0]] or old_name in [elem.name for elem in tup[1]]:
                            somethingChanged = True
                            continue
                        else:
                            newSet1 = tup[0]
                            newSet2 = tup[1]
                    newListOfTuples.append([newSet1, newSet2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunction and mapsToFunctionTuple:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0].name == old_name:
                            newElem1 = FPTMapping(new_name)
                        else:
                            newElem1 = tup[0]
                        if tup[1][0].name == old_name:
                            newInnerElem21 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem21 = tup[1][0]
                        if tup[1][1].name == old_name:
                            newInnerElem22 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem22 = tup[1][1]
                    else:
                        if tup[0].name == old_name or tup[1][0].name == old_name or tup[1][1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newElem1 = tup[0]
                            newInnerElem21 = tup[1][0]
                            newInnerElem22 = tup[1][1]
                    newListOfTuples.append([newElem1, tuple([newInnerElem21, newInnerElem22])])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunction and mapsToFunctionSet:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0].name == old_name:
                            newElem1 = FPTMapping(new_name)
                        else:
                            newElem1 = tup[0]
                        newSet2 = []
                        for elem in tup[1]:
                            if elem.name == old_name:
                                newSet2.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet2.append(elem)
                        newSet2 = frozenset(newSet2)
                    else:
                        if tup[0].name == old_name or old_name in [elem.name for elem in tup[1]]:
                            somethingChanged = True
                            continue
                        else:
                            newElem1 = tup[0]
                            newSet2 = tup[1]
                    newListOfTuples.append([newElem1, newSet2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionTuple and mapsToFunction:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0][0].name == old_name:
                            newInnerElem11 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem11 = tup[0][0]
                        if tup[0][1].name == old_name:
                            newInnerElem12 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem12 = tup[0][1]
                        if tup[1].name == old_name:
                            newElem2 = FPTMapping(new_name)
                        else:
                            newElem2 = tup[1]
                    else:
                        if tup[0][0].name == old_name or tup[0][1].name == old_name or tup[1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newInnerElem11 = tup[0][0]
                            newInnerElem12 = tup[0][1]
                            newElem2 = tup[1]
                    newListOfTuples.append([tuple([newInnerElem11, newInnerElem12]), newElem2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionTuple and mapsToFunctionSet:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0][0].name == old_name:
                            newInnerElem11 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem11 = tup[0][0]
                        if tup[0][1].name == old_name:
                            newInnerElem12 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem12 = tup[0][1]
                        newSet2 = []
                        for elem in tup[1]:
                            if elem.name == old_name:
                                newSet2.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet2.append(elem)
                        newSet2 = frozenset(newSet2)
                    else:
                        if tup[0][0].name == old_name or tup[0][1].name == old_name or old_name in [elem.name for elem in tup[1]]:
                            somethingChanged = True
                            continue
                        else:
                            newInnerElem11 = tup[0][0]
                            newInnerElem12 = tup[0][1]
                            newSet2 = tup[1]
                    newListOfTuples.append([tuple([newInnerElem11, newInnerElem12]), newSet2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionSet and mapsToFunction:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        newSet1 = []
                        for elem in tup[0]:
                            if elem.name == old_name:
                                newSet1.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet1.append(elem)
                        newSet1 = frozenset(newSet1)
                        if tup[1].name == old_name:
                            newElem2 = FPTMapping(new_name)
                        else:
                            newElem2 = tup[1]
                    else:
                        if old_name in [elem.name for elem in tup[0]] or tup[1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newSet1 = tup[0]
                            newElem2 = tup[1]
                    newListOfTuples.append([newSet1, newElem2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionSet and mapsToFunctionTuple:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        newSet1 = []
                        for elem in tup[0]:
                            if elem.name == old_name:
                                newSet1.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet1.append(elem)
                        newSet1 = frozenset(newSet1)
                        if tup[1][0].name == old_name:
                            newInnerElem21 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem21 = tup[1][0]
                        if tup[1][1].name == old_name:
                            newInnerElem22 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem22 = tup[1][1]
                    else:
                        if old_name in [elem.name for elem in tup[0]] or tup[1][0].name == old_name or tup[1][1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newSet1 = tup[0]
                            newInnerElem21 = tup[1][0]
                            newInnerElem22 = tup[1][1]
                    newListOfTuples.append([newSet1, tuple([newInnerElem21, newInnerElem22])])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunction:
                transformed_input = [elem.name for elem in funcObject.listOfElements]
                if old_name in transformed_input:
                    newListOfTuples = []
                    for tup in funcObject.listOfTuples:
                        if new_name is not None:
                            if tup[0].name == old_name:
                                newElem1 = FPTMapping(new_name)
                                newElem2 = tup[1]
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        else:
                            if tup[0].name == old_name:
                                continue
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        newListOfTuples.append([newElem1, newElem2])
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsToFunction:
                transformed_output = [elem.name for elem in funcObject.listOfValues]
                if old_name in transformed_output:
                    newListOfTuples = []
                    for tup in funcObject.listOfTuples:
                        if new_name is not None:
                            if tup[1].name == old_name:
                                newElem1 = tup[0]
                                newElem2 = FPTMapping(new_name)
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        else:
                            if tup[1].name == old_name:
                                continue
                            else:
                                newElem1 = tup[0]
                                newElem2 = tup[1]
                        newListOfTuples.append([newElem1, newElem2])
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionTuple:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[0][0].name == old_name:
                            newInnerElem11 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem11 = tup[0][0]
                        if tup[0][1].name == old_name:
                            newInnerElem12 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem12 = tup[0][1]
                    else:
                        if tup[0][0].name == old_name or tup[0][1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newInnerElem11 = tup[0][0]
                            newInnerElem12 = tup[0][1]
                    newListOfTuples.append([tuple([newInnerElem11, newInnerElem12]), tup[1]])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsToFunctionTuple:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        if tup[1][0].name == old_name:
                            newInnerElem21 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem21 = tup[1][0]
                        if tup[1][1].name == old_name:
                            newInnerElem22 = FPTMapping(new_name)
                            somethingChanged = True
                        else:
                            newInnerElem22 = tup[1][1]
                    else:
                        if tup[1][0].name == old_name or tup[1][1].name == old_name:
                            somethingChanged = True
                            continue
                        else:
                            newInnerElem21 = tup[1][0]
                            newInnerElem22 = tup[1][1]
                    newListOfTuples.append([tup[0], tuple([newInnerElem21, newInnerElem22])])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsFromFunctionSet:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        newSet1 = []
                        for elem in tup[0]:
                            if elem.name == old_name:
                                newSet1.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet1.append(elem)
                        newSet1 = frozenset(newSet1)
                    else:
                        if old_name in [elem.name for elem in tup[0]]:
                            somethingChanged = True
                            continue
                        else:
                            newSet1 = tup[0]
                    newListOfTuples.append([newSet1, tup[1]])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

            elif mapsToFunctionSet:
                newListOfTuples = []
                somethingChanged = False
                for tup in funcObject.listOfTuples:
                    if new_name is not None:
                        newSet2 = []
                        for elem in tup[1]:
                            if elem.name == old_name:
                                newSet2.append(FPTMapping(new_name))
                                somethingChanged = True
                            else:
                                newSet2.append(elem)
                        newSet2 = frozenset(newSet2)
                    else:
                        if old_name in [elem.name for elem in tup[1]]:
                            somethingChanged = True
                            continue
                        else:
                            newSet2 = tup[1]
                    newListOfTuples.append([tup[0], newSet2])
                if somethingChanged:
                    newFunc = FPTMapping(funcObject.name, newListOfTuples, funcObject.mappingType)
                    newFunc.recreateFunctionFromList()
                    DICT_OF_DICTS["mappings"][func] = newFunc

        for oldSet in DICT_OF_DICTS["sets"]:
            old_set = DICT_OF_DICTS["sets"][oldSet]

            hasFunctions = False
            for elem in old_set:
                hasFunctions = type(elem) == FPTMapping
                break

            hasTupleOfFunctions = False
            for elem in old_set:
                if type(elem) == tuple:
                    hasTupleOfFunctions = type(elem[0]) == FPTMapping
                else:
                    break

            hasSetOfFunctions = False
            for elem in old_set:
                if type(elem) == frozenset or type(elem) == set:
                    done = False
                    for innerElem in elem:
                        hasSetOfFunctions = type(innerElem) == FPTMapping
                        done = True
                        break
                    if done:
                        break
                else:
                    break

            if hasFunctions:
                nameList = [func.name for func in old_set]
                if old_name in nameList:
                    newList = []
                    if new_name is not None:
                        for func in old_set:
                            if func.name == old_name:
                                newList.append(FPTMapping(new_name))
                            else:
                                newList.append(func)
                    else:
                        for func in old_set:
                            if func.name != old_name:
                                newList.append(func)
                    DICT_OF_DICTS["sets"][oldSet] = frozenset(newList)
                    self.updateRelationsAndMappingsFromSetChange(oldSet)

            elif hasTupleOfFunctions:
                newList = []
                if new_name is not None:
                    for tup in old_set:
                        if tup[0].name == old_name and tup[1].name == old_name:
                            newList.append(tuple([FPTMapping(new_name), FPTMapping(new_name)]))
                        elif tup[0].name == old_name:
                            newList.append(tuple([FPTMapping(new_name), tup[1]]))
                        elif tup[1].name == old_name:
                            newList.append(tuple([tup[0], FPTMapping(new_name)]))
                        else:
                            newList.append(tup)
                else:
                    for tup in old_set:
                        if tup[0].name != old_name and tup[1].name != old_name:
                            newList.append(tup)
                DICT_OF_DICTS["sets"][oldSet] = frozenset(newList)
                self.updateRelationsAndMappingsFromSetChange(oldSet)

            elif hasSetOfFunctions:
                newList = []
                if new_name is not None:
                    for s in old_set:
                        newInnerList = []
                        for elem in s:
                            if elem.name == old_name:
                                newInnerList.append(FPTMapping(new_name))
                            else:
                                newInnerList.append(elem)
                        newList.append(frozenset(newInnerList))
                else:
                    for s in old_set:
                        if old_name not in [elem.name for elem in s]:
                            newList.append(s)
                DICT_OF_DICTS["sets"][oldSet] = frozenset(newList)
                self.updateRelationsAndMappingsFromSetChange(oldSet)

        FPTMapping.dictOfMappings.pop(old_name)
        FPTMapping.dictOfFPTMappings.pop(old_name)

    def updateDictionariesFromJSONFile(self, filename):
        with open(filename, "r") as file:
            raw_data = file.read()
            try:
                dictOfDicts = loads(raw_data, object_hook=hinted_datatype_hook)
                DICT_OF_DICTS['mappings'] = dictOfDicts['mappings']
                DICT_OF_DICTS['sets'] = dictOfDicts['sets']
                DICT_OF_DICTS['relations'] = dictOfDicts['relations']

                # warning if "-" gets overwritten
                if "-" in DICT_OF_DICTS['sets'].keys() and len(DICT_OF_DICTS['sets']["-"]) > 0:
                    print("WARNING: content of the set '-' has been overwritten (reserved set name)!")

                # warning if "MV-algebra" gets deleted
                if "MV-algebra" in DICT_OF_DICTS['sets'].keys():
                    self.deleteElementFromDictionary('sets', "MV-algebra")
                    print("WARNING: content of the set 'MV-algebra' has been deleted (reserved set name)!")

                # add empty set (overwrite existing "-" set to ensure an empty set)
                self.addElementToDictionary('sets', "-", set())

                FPTMapping.repairInvalidFPTMappings()
            except Exception as e:
                dumpException(e)

    def updateDictionariesManually(self, mappings, sets, relations):
        try:
            DICT_OF_DICTS['mappings'] = mappings
            DICT_OF_DICTS['sets'] = sets
            DICT_OF_DICTS['relations'] = relations

            # warning if "-" gets overwritten
            if "-" in DICT_OF_DICTS['sets'].keys() and len(DICT_OF_DICTS['sets']["-"]) > 0:
                print("WARNING: content of the set '-' has been overwritten (reserved set name)!")

            # warning if "MV-algebra" gets deleted
            if "MV-algebra" in DICT_OF_DICTS['sets'].keys():
                self.deleteElementFromDictionary('sets', "MV-algebra")
                print("WARNING: content of the set 'MV-algebra' has been deleted (reserved set name)!")

            # add empty set (overwrite existing "-" set to ensure an empty set)
            self.addElementToDictionary('sets', "-", set())
        except Exception as e:
            dumpException(e)