import os
from configparser import ConfigParser

LISTBOX_MIMETYPE = "application/x-item"

OP_CODE_ADDITION = 1
OP_CODE_SUBTRACTION = 2
OP_CODE_SUBTRACTION_Z = 3
OP_CODE_CONSTANT = 4
OP_CODE_REINDEXING = 5
OP_CODE_MINIMUM = 6
OP_CODE_MAXIMUM = 7
OP_CODE_AVERAGE = 8
OP_CODE_SEPARATOR = 9
OP_CODE_TESTING = 10
OP_CODE_HIGHER_ORDER_FUNCTION = 11

FPT_NODES = {
}

config = ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

from fixpointtool.functions.fpt_mvalgebra import Algebra1, Algebra2
try:
    if config['all']['mv-algebra'] == "algebra 1":
        ALGEBRA = Algebra1(int(config['all']['k']))
    elif config['all']['mv-algebra'] == "algebra 2":
        ALGEBRA = Algebra2(int(config['all']['k']))
    else:
        ALGEBRA = Algebra1()
        print("default algebra 1 has been selected")
except Exception as e:
    ALGEBRA = Algebra1()
    print("default algebra 1 has been selected")

GFP = True


class ConfException(Exception): pass


class InvalidNodeRegistration(ConfException): pass


class OpCodeNotRegistered(ConfException): pass


def updateMVAlgebra():
    global ALGEBRA
    global config
    config.read(os.path.join(os.path.dirname(__file__), "config.ini"))

    try:
        if config['all']['mv-algebra'] == "algebra 1":
            ALGEBRA = Algebra1(int(config['all']['k']))
        elif config['all']['mv-algebra'] == "algebra 2":
            ALGEBRA = Algebra2(int(config['all']['k']))
        else:
            ALGEBRA = Algebra1()
            print("default algebra 1 has been selected")
    except Exception as e:
        ALGEBRA = Algebra1()
        print("default algebra 1 has been selected")


def changeGFP(str):
    global GFP
    if str == "GFP":
        GFP = True
    elif str == "LFP":
        GFP = False
    else:
        print("WARNING: changeGFP has been used incorrectly")


def register_node_now(op_code, class_reference):
    if op_code in FPT_NODES:
        raise InvalidNodeRegistration("Duplicate node registration of '%s'. There is already %s"
                                      %(op_code, FPT_NODES[op_code]))
    FPT_NODES[op_code] = class_reference


def register_node(op_code):
    def decorator(original_class):
        register_node_now(op_code, original_class)
        return original_class
    return decorator


def get_class_from_opcode(op_code):
    if op_code not in FPT_NODES: raise OpCodeNotRegistered("OpCode '%d' is not registered" % op_code)
    return FPT_NODES[op_code]


# import all nodes and register them
from fixpointtool.nodes import *