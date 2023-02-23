from PyQt5.QtWidgets import *

from fixpointtool.content.fpt_mapping import FPTMapping


class QDMListWidgetItem(QListWidgetItem):
    def __init__(self, item, itemType, parent=None):
        super().__init__(parent)
        self.item = item
        self.type = itemType

        self.overwriteText()

    def overwriteText(self):
        if self.type == "string" or self.type == "number" or self.type == "mapping":
            self.setText(str(self.item))
        elif self.type == "n-tuple":
            newStr = "("
            for elem in self.item:
                if type(elem) == set or type(elem) == frozenset:
                    newStr1 = "{"
                    for innerElem in sorted(elem):
                        newStr1 += str(innerElem) + ", "
                    if len(newStr1) > 1:
                        newStr1 = newStr1[:-2] + "}"
                    else:
                        newStr1 = "{}"
                else:
                    newStr1 = str(elem)
                newStr += newStr1 + ", "
            newStr = newStr[:-2] + ")"

            self.setText(newStr)
        elif self.type == "set" or self.type == "power set":
            newStr = "{"
            for elem in sorted(self.item):
                newStr += str(elem) + ", "
            if len(newStr) > 1:
                newStr = newStr[:-2] + "}"
            else:
                newStr = "{}"

            self.setText(newStr)
        else:
            self.setText("ERROR")