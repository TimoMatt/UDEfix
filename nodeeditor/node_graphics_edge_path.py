import math
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainterPath

EDGE_CP_ROUNDNESS = 100


class GraphicsEdgePathBase:
    def __init__(self, owner):
        self.owner = owner

    def calcPath(self):
        return None


class GraphicsEdgePathDirect(GraphicsEdgePathBase):
    def calcPath(self):
        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.lineTo(self.owner.posDestination[0], self.owner.posDestination[1])
        return path


class GraphicsEdgePathBezier(GraphicsEdgePathBase):
    def calcPath(self):
        s = self.owner.posSource
        d = self.owner.posDestination
        dist = (d[0] - s[0]) * 0.5

        cpx_s = +dist
        cpx_d = -dist
        cpy_s = 0
        cpy_d = 0

        if self.owner.edge.start_socket is not None:
            ssin = self.owner.edge.start_socket.is_input
            ssout = self.owner.edge.start_socket.is_output

            if (s[0] > d[0] and ssout) or (s[0] < d[0] and ssin):
                cpx_d *= -1
                cpx_s *= -1

                cpy_d = (
                    (s[1] - d[1]) / math.fabs(
                        (s[1] - d[1]) if (s[1] - d[1]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS
                cpy_s = (
                    (d[1] - s[1]) / math.fabs(
                        (d[1] - s[1]) if (d[1] - s[1]) != 0 else 0.00001
                    )
                ) * EDGE_CP_ROUNDNESS

        path = QPainterPath(QPointF(self.owner.posSource[0], self.owner.posSource[1]))
        path.cubicTo(s[0] + cpx_s, s[1] + cpy_s, d[0] + cpx_d, d[1] + cpy_d, self.owner.posDestination[0], self.owner.posDestination[1])

        return path