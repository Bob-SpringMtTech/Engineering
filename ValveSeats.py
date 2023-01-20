import math

from Engineering import unit_of_measure as um
from Engineering import NIST330 as un

def uFormat(q, u, f):
    if(len(u.Symbol) > 0):
        str = f'{q.Value(u):{f}} {u.Symbol}'
    else:
        str = f'{q.Value(u):{f}}'

    return str

# Calculate the surface area of a truncated cone excluding the circular areas.  Height is the perpendicular
# distance between the big and small circles (not slant height).  
# Works for non-truncated cones by setting smallRadius to zero.
def TruncConeArea(bigRadius, smallRadius, height):
    slant = math.sqrt((bigRadius - smallRadius) ** 2 + height ** 2)
    area = math.pi * slant * (bigRadius + smallRadius)

    return area

# Spherical radius plug against a beveled seat.  All angles are taken from the axis of the parts (half angles)
#  diaSeat     - thru bore of the seat
#  angSeat     - the angle of the seat wrt the seat axis (half angle)
#  htSeat      - the vertical distance between the upper corner and lower corner of the seat
#  srPlug      - spherical radius of the plug.  Set equal to zero to calculate the sph rad that will put the 
#                contact circle at the mid point of the seat.
#  diaFlatPlug - the diameter at the termination of the spherical radius
#  diaStem     - the diameter of the stem below the lower corner of the seat
#
# Plugs can contact the seat on the lower corner, upper corner, or on the bevel.
class SphPlug_BevelSeat:
    def __init__(self, diaSeat, angSeat, htSeat, srPlug, diaFlatPlug, diaStem):
        self._diaSeat = diaSeat.SIValue
        self._angSeat = angSeat.SIValue
        self._htSeat  = htSeat.SIValue
        self._srPlug  = srPlug.SIValue
        self._diaFlatPlug  = diaFlatPlug.SIValue
        self._diaStem = diaStem.SIValue

        # x1, y1 correspond to the lower corner of the seat
        self._x1 = self._diaSeat / 2.0             
        self._y1 = 0                                

        # x2, y2 correspond to the upper corner of the seat
        self._x2 = self._x1 + self._htSeat * math.tan(self._angSeat)
        self._y2 = self._y1 + self._htSeat

        if (self._srPlug  == 0): # a zero value for srPlug will calculate srPlug so that it the contact circle is at the midpoint in the seat.
            self._xc = (self._x1 + self._x2) / 2.0
            self._yc = (self._y1 + self._y2) / 2.0
            self._srPlug = self._xc / math.cos(self._angSeat)
        else: # srPlug was specified
            # xc, yc correspond to the contact point between the seat and plug (ideal)
            self._xc = self._srPlug * math.sin(math.pi / 2.0 - self._angSeat)
            self._yc = self._y1 + (self._xc - self._x1) / math.tan(self._angSeat)

        contactPct = (self._xc - self._x1) / (self._x2 - self._x1) * 100.0
        self._contact_location = f'On Bevel @ {contactPct:0.1f}'

        # test for the large plug condition.  set the contact circle at x2,y2 corner
        if (self._xc > self._x2): 
            self._xc = self._x2
            self._yc = self._y2
            self._contact_location = 'Upper Corner - Large Plug'
        # test for the small plug condition.  set the contact circle at x1,y1 corner
        if (self._xc < self._x1):
            self._xc = self._x1
            self._yc = self._y1
            self._contact_location = 'Lower Corner - Small Plug'

        # x0, y0 corresponds to the center of the spherical radius
        self._x0 = 0
        self._y0closed = math.sqrt(self._srPlug ** 2 - self._xc ** 2) + self._yc

        # x3, y3 correspond to the lower corner of the plug where the spherical radius ends
        self._x3 = self._diaFlatPlug / 2.0
        if (self._x3 > self._x1):
            self._contact_location = 'NO contact - inavalid configuration'
            raise ValueError(self._contact_location)
        self._y3closed = self._y0closed - math.sqrt(self._srPlug ** 2 - self._x3 ** 2)
    
        # Calculate the stroke where the minimum gap is on the corner of x2,y2  
        # Strokes greater than this will be limited by the gap between the sph rad and x2,y2
        # Strokes less than this will be limited by the gap defined by the sph rad and perpendicular to the bevel.
        y0 = self._x2 * math.tan(self._angSeat) + self._y2
        self._stroke_break = y0 - self._y0closed

        self._area_zone = 'undefined - calculate the FlowArea()'
        self._area_annular = math.pi / 4.0 * (self._diaSeat ** 2 - self._diaStem ** 2)
    
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

        area_3_1 = TruncConeArea(self._x1, self._x3, self._y3 - self._y1)
        area_3_2 = TruncConeArea(self._x2, self._x3, self._y3 - self._y2)

        area = min(area_3_1, area_3_2)

        # the area between sph rad plug and the lower corner of the seat
        slant0_1 = math.sqrt(self._x1 ** 2 + (self._y0 - self._y1) ** 2)
        xp = self._x1 * self._srPlug / slant0_1
        area_p_1 = 1e200
        if (xp > self._x3):
            slantp_1 = slant0_1 - self._srPlug
            area_p_1 = math.pi * slantp_1 * (self._x1 + xp)
            area = min(area, area_p_1)

        # the area between sph rad plug and the upper corner of the seat
        slant0_2 = math.sqrt(self._x2 ** 2 + (self._y0 - self._y2) ** 2)
        xp = self._x2 * self._srPlug / slant0_2
        area_p_2 = 1e200
        if (xp > self._x3):
            slantp_2 = slant0_2 - self._srPlug
            area_p_2 = math.pi * slantp_2 * (self._x2 + xp)
            area = min(area, area_p_2)

        area_p_s = 1e200
        if (strokeSI < self._stroke_break):
            # the area between sph rad plug and the line perpendicular to the seat
            gapp_s = strokeSI * math.sin(self._angSeat)
            slant0_s = self._srPlug + gapp_s
            xs = self._xc * slant0_s / self._srPlug
            area_p_s = math.pi * gapp_s * (xs + self._xc)
            area = min(area, area_p_s)

        area = min(area, self._area_annular)

        if (area == area_3_1):
            self._area_zone = 'plug corner to lower seat corner'
        if (area == area_3_2):
            self._area_zone = 'plug corner to upper seat corner'
        if (area == area_p_1):
            self._area_zone = 'plug surface to lower seat corner'
        if (area == area_p_2):
            self._area_zone = 'plug surface to upper seat corner'
        if (area == area_p_s):
            self._area_zone = 'plug surface to seat bevel surface'
        if (area == self._area_annular):
            self._area_zone = 'plug stem diameter to seat diameter'

        return area * un.Area.meterSq

    @property
    def ContactLocation(self):
        return self._contact_location

    @property
    def AreaZone(self):
        return self._area_zone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq


# Ball plug against a beveled seat.  All angles are taken from the axis of the parts (half angles)
class BallPlug_BevSeat:
    def __init__(self, diaSeat, angSeat, htSeat, diaBall):
        srPlug = diaBall / 2.0
        if (srPlug.SIValue == 0.0):
            angSeatSI = angSeat.SIValue
            xc = (diaSeat + htSeat * math.tan(angSeatSI)) / 2.0
            srPlug = xc / math.cos(angSeatSI)
            htPlug = srPlug
        else:
            htPlug = srPlug
        diaFlatPlug = 0.0 * un.Length.m
        diaStem = 0.0 * un.Length.m
        self._vlv = SphPlug_BevelSeat(diaSeat, angSeat, htSeat, srPlug, diaFlatPlug, diaStem)

    @property
    def SphRadPlug(self):
        return self._vlv.SphRadPlug

    @property
    def ContactDia(self):
        return self._vlv.ContactDiameter 

    # Calculate the flow area for a given stroke.
    def FlowArea(self, stroke):
        return self._vlv.FlowArea(stroke)

    @property
    def ContactLocation(self):
        return self._vlv.ContactLocation

    @property
    def AreaZone(self):
        return self._vlv.AreaZone

    @property
    def MaxArea(self):
        return self._vlv.MaxArea



# Ball plug against a square seat.  All angles are taken from the axis of the parts (half angles)
class BallPlug_SqSeat:
    def __init__(self, diaSeat, diaBall = 0.0 * un.Length.inch, contactAngle = 0.0 * un.Angle.deg):
        self._diaSeat = diaSeat.SIValue
        self._srPlug  = diaBall.SIValue / 2.0
        self._contactAngle = contactAngle.SIValue

        if (self._srPlug == 0.0 and self._contactAngle == 0.0):
            raise ValueError('either diaBall or contactAngle must be specified')

        # x1, y1 correspond to the corner of the seat
        self._x1 = self._diaSeat / 2.0             
        self._y1 = 0                                

        # x0, y0 corresponds to the center of the spherical radius
        self._x0 = 0
        if (self._srPlug == 0.0):
            self._srPlug = self._x1 / math.cos(self._contactAngle)
        if (self._contactAngle == 0.0):
            self._contactAngle = math.acos(self._x1 / self._srPlug)
        
        self._y0closed = math.sqrt(self._srPlug ** 2 - self._x1 ** 2) + self._y1
        self._area_annular = math.pi / 4.0 * self._diaSeat ** 2
    
    # Calculate the flow area for a given stroke.
    def FlowArea(self, stroke):
        strokeSI = stroke.SIValue
        self._y0 = self._y0closed + strokeSI

        # the area between sph rad plug and the lower corner of the seat
        slant0_1 = math.sqrt(self._x1 ** 2 + (self._y0 - self._y1) ** 2)
        xp = self._x1 * self._srPlug / slant0_1
        slantp_1 = slant0_1 - self._srPlug
        area_p_1 = math.pi * slantp_1 * (self._x1 + xp)

        area = min(area_p_1, self._area_annular)

        if (area == area_p_1):
            self._area_zone = 'plug surface to seat corner'
        if (area == self._area_annular):
            self._area_zone = 'seat diameter'

        return area * un.Area.meterSq


    @property
    def SphRadPlug(self):
        return self._srPlug * un.Length.m

    @property
    def ContactDia(self):
        return self._x1 * 2.0 * un.Length.m

    @property
    def ContactLocation(self):
        return 'seat corner'

    @property
    def AreaZone(self):
        return self._vlv.AreaZone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq


# Calculate the flow area between a conical plug and square seat.
# All angles are taken from the axis of the part (half angles)
class ConePlug_SqSeat:
    def __init__(self, diaSeat, diaPlugTip, angPlug):
        self._diaSeat = diaSeat.SIValue
        self._diaPlugTip = diaPlugTip.SIValue
        self._angPlug = angPlug.SIValue

        # x1, y1 correspond to the corner of the seat
        self._x1 = self._diaSeat / 2.0             
        self._y1 = 0                                

        self._area_annular = math.pi / 4.0 * self._diaSeat ** 2
    
        
    def FlowArea(self, stroke):
        _stroke = stroke.SIValue
        # x3, y3 correspond to the tip of the plug
        x3 = self._diaPlugTip / 2.0
        y3 = self._y1 + _stroke - (self._x1 - x3) / math.tan(self._angPlug)

        xs = self._x1
        gap = _stroke * math.sin(self._angPlug)
        xp = xs - gap * math.cos(self._angPlug)
        self._area_zone = 'plug surface to seat corner'
        if (xp < x3): # cone is fully retracted from the seat
            xp = x3
            gap = math.sqrt(((self._x1 - x3) ** 2) + ((self._y1 - y3) ** 2))
            self._area_zone = 'plug tip to seat corner'
            stroke_inch = stroke.Value(un.Length.inch)
            # print (stroke_inch)

        areaTruncCone = math.pi * gap * (xs + xp)

        area = min(areaTruncCone, self._area_annular)

        if (area == self._area_annular):
            self._area_zone = 'seat diameter'
    
        return area * un.Area.meterSq

    @property
    def ContactDia(self):
        return self._diaSeat * un.Length.inch 

    @property
    def ContactLocation(self):
        return 'seat corner'

    @property
    def AreaZone(self):
        return self._area_zone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq

