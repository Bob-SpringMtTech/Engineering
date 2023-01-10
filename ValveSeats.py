import math

from Engineering import unit_of_measure as um
from Engineering import NIST330 as un

def uFormat(q, u, f):
    if(len(u.Symbol) > 0):
        str = f'{q.Value(u):{f}} {u.Symbol}'
    else:
        str = f'{q.Value(u):{f}}'

    return str

# Spherical radius plug against a beveled seat.  All angles are taken from the axis of the parts (half angles)
#  diaSeat - thru bore of the seat
#  angSeat - the angle of the seat wrt the seat axis (half angle)
#  htSeat  - the vertical distance between the upper corner and lower corner of the seat
#  srPlug  - spherical radius of the plug
#  htPlug  - vertical distance from the contact circle of the seat/plug to the lower cornet of the plug spg rad
#  diaStem - the diameter of the stem below the lower corner of the seat
class SphPlug_BevelSeat:
    def __init__(self, diaSeat, angSeat, htSeat, srPlug, htPlug, diaStem):
        self._diaSeat = diaSeat.SIValue
        self._angSeat = angSeat.SIValue
        self._htSeat = htSeat.SIValue
        self._srPlug = srPlug.SIValue
        self._htPlug = htPlug.SIValue
        self._diaStem = diaStem.SIValue

        # x1, y1 correspond to the lower corner of the seat
        self._x1 = self._diaSeat / 2.0             
        self._y1 = 0                                

        # x2, y2 correspond to the upper corner of the seat
        self._x2 = self._x1 + self._htSeat * math.tan(self._angSeat)
        self._y2 = self._y1 + self._htSeat

        if (self._srPlug > 0):
            # xc, yc correspond to the contact point between the seat and plug (ideal)
            self._xc = self._srPlug * math.sin(math.pi / 2.0 - self._angSeat)
            self._yc = self._y1 + (self._xc - self._x1) / math.tan(self._angSeat)
        else: # a zero value for srPlug will calculate srPlug so that it the contact circle is at the midpoint in the seat.
            self._xc = (self._x1 + self._x2) / 2.0
            self._yc = (self._y1 + self._y2) / 2.0
            self._srPlug = self._xc / math.cos(self._angSeat)

        # x0, y0 correspond to the center of the spherical radius
        self._x0 = 0
        self._y0closed = self._srPlug * math.sin(self._angSeat) + self._yc

        # x3, y3 correspond to the lower corner of the plug where the spherical radius ends
        self._y3closed = self._yc - self._htPlug
        self._x3 = math.sqrt(self._srPlug ** 2 - (self._y0closed - self._y3closed) ** 2)
    
    @property
    def ContactDiameter(self):
        return self._xc * 2.0 * un.Length.m

    @property
    def SphRadPlug(self):
        return self._srPlug * un.Length.m

    # Calculate the flow area for a given stroke.
    def FlowArea(self, stroke):
        strokeSI = stroke.SIValue
        self._y0 = self._y0closed + strokeSI
        self._y3 = self._y3closed + strokeSI

        angCS = math.atan((self._y0 - self._y2) / self._x2)
        angCP = math.atan((self._y3 - self._y2) / (self._x2 - self._x3))
        if (self._y3 < self._y2):
            angCP = 0
        
        angFlow = max(self._angSeat, angCS, angCP)

        if (angFlow == self._angSeat):
            gap = strokeSI * math.sin(self._angSeat)
            xp = self._xc
            xs = xp + gap * math.cos(self._angSeat)
            lCone = self._srPlug
        elif (angFlow == angCS):
            gap = math.sqrt(((self._x2 - self._x0) ** 2) + ((self._y2 - self._y0) ** 2)) - self._srPlug
            xs = self._x2
            xp = xs - gap * math.cos(angFlow)
            lCone = self._srPlug
        elif (angFlow == angCP):
            gap = math.sqrt(((self._x2 - self._x3) ** 2) + ((self._y2 - self._y3) ** 2))
            xs = self._x2
            xp = self._x3
            lCone = xp / math.cos(angFlow)
        else:
            gap = 0.0

        areaTruncCone = math.pi * (lCone * (xs - xp) + xs * gap)

        areaAnnular = math.pi / 4.0 * (self._diaSeat ** 2 - self._diaStem ** 2)

        area = min(areaTruncCone, areaAnnular) * un.Area.meterSq

        return area


# Ball plug against a beveled seat.  All angles are taken from the axis of the parts (half angles)
# htSeat was redefined in SphPlug_BevelSeat above - make sure this still works.
class BallPlug_BevSeat:
    def __init__(self, diaSeat, angSeat, htSeat, diaBall):
        srPlug = diaBall / 2.0
        htPlug = srPlug
        diaStem = 0.0 * un.Length.m
        self._vlv = SphPlug_BevelSeat(diaSeat, angSeat, htSeat, srPlug, diaStem)

    @property
    def ContactDia(self):
        return self._vlv.ContactDiameter 

    # Calculate the flow area for a given stroke.
    def FlowArea(self, stroke):
        return self._vlv.FlowArea(stroke)


# Ball plug against a square seat.  All angles are taken from the axis of the parts (half angles)
class BallPlug_SqSeat:
    def __init__(self, diaSeat, diaBall):
        angSeat = 90.0 * un.Angle.deg
        htSeat = 0.0 * un.Length.m
        srPlug = diaBall / 2.0
        diaStem = 0.0 * un.Length.m
        htPlug = srPlug
        self._vlv = SphPlug_BevelSeat(diaSeat, angSeat, htSeat, srPlug, htPlug, diaStem)

    @property
    def ContactDia(self):
        return self._vlv._diaSeat

    # Calculate the flow area for a given stroke.
    def FlowArea(self, stroke):
        strokeSI = stroke.SIValue
        y0 = self._vlv._y0closed + strokeSI

        angFlow = math.atan((self._vlv._y0 - self._vlv._y1) / self._vlv._x1)

        gap = math.sqrt(((self._vlv._x1 - self._vlv._x0) ** 2) + ((self._vlv._y1 - y0) ** 2)) - self._vlv._srPlug
        xs = self._vlv._x1
        xp = xs - gap * math.cos(angFlow)
        lCone = self._vlv._srPlug

        areaTruncCone = math.pi * (lCone * (xs - xp) + xs * gap)

        areaAnnular = math.pi / 4.0 * (self._vlv._diaSeat ** 2 - self._vlv._diaStem ** 2)

        area = min(areaTruncCone, areaAnnular) * un.Area.meterSq

        return area


# Calculate the flow area between a conical plug and square seat.
# All angles are taken from the axis of the part (half angles)
def FlowArea_ConePlug_SqSeat(diaSeat, diaPlugTip, angPlug, stroke):
    angPlugRad = angPlug.SIValue

    # x1, y1 correspond to the corner of the seat
    x1 = diaSeat.SIValue / 2.0             
    y1 = 0                                

    # x3, y3 correspond to the lower corner of the plug
    x3 = diaPlugTip.SIValue / 2.0
    y3 = - (x1 - x3) / math.tan(angPlugRad) + stroke.SIValue

    xs = x1
    gap = stroke.SIValue * math.sin(angPlugRad)
    xp = xs - gap * math.cos(angPlugRad)
    if (xp > x3): # cone is limiting the flow area
        lCone = xp / math.cos(angPlugRad)
    else: # cone is fully retracted from the seat
        xp = x3
        gap = math.sqrt(((x1 - x3) ** 2) + ((y1 - y3) ** 2))
        lCone = x3 * gap / (x1 - x3)

    areaTruncCone = math.pi * (lCone * (xs - xp) + xs * gap)

    areaAnnular = math.pi / 4.0 * diaSeat.SIValue

    area = min(areaTruncCone, areaAnnular) * un.Area.meterSq
   
    return area

