import math
import sys
eng_path = './Engineering'
if not eng_path in sys.path:
    sys.path.insert(0, eng_path)
import NIST330 as un

def uFormat(q, u, f): # this function will be removed eventually.
    return q.Format(u, f)

# conv_fac = 39.37 # convert meters to inches
conv_fac = (1.0 * un.Length.m).Value(un.Length.inch)

class Point2d:
    def __init__(self, x, y, name = None):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self) -> str:
        return f'({self.name}: {self.x * conv_fac}, {self.y * conv_fac})'

    @property
    def Name(self):
        return self.name

    @classmethod
    def Distance(cls, p1, p2):
        dx = p2.x - p1.x
        dy = p2.y - p1.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def Shift(self, dx = math.nan, dy = math.nan):
        new_x = self.x
        new_y = self.y
        goodData = (0 if math.isnan(dx) else 2) + (0 if math.isnan(dy) else 1)
        if (goodData == 0):
            raise Exception("must specify either 'dx' or 'dy'")
        elif (goodData == 1): # dy was specified, dx was not
            new_y += dy
        elif (goodData == 2): # dx was specified, dy was not
            new_x += dx
        else: # both x1 and y1 were specified
            raise Exception("must not specify both 'dx' and 'dy'")
        
        return Point2d(new_x, new_y, self.name)

class Line2d:
    def __init__(self, m, b, name = None):
        self.m = m
        self.b = b
        self.name = name

    def __str__(self) -> str:
        if (self.b >= 0.0):
            _b = self.b
            _sgn = '+'
        else:
            _b = -self.b
            _sgn = '-'

        return f'{self.name}: y = {self.m}x {_sgn} {_b * conv_fac}'


    def X(self, y):
        return (y - self.b) / self.m

    def Y(self, x):
        return self.m * x + self.b

    @property
    def Slope(self):
        return self.m

    @property
    def Y_Int(self):
        return self.b

    @property
    def Name(self):
        return self.name

    @classmethod
    def SlopeYInt(cls, m, b, name = None):
        return Line2d(m, b, name)
        
    @classmethod
    def ThruPointWithSlope(cls, pt, m, name = None):
        return Line2d(m, pt.y - m * pt.x, name)
        
    @classmethod
    def Thru2Points(cls, p1, p2, name = None):
        m = (p2.y - p1.y) / (p2.x - p1.x)
        b = p1.y - m * p1.x
        return Line2d(m, b, name)

    def Perpendicular(self, thruPoint2d, name = None):
        m_new = -1.0/self.m
        b_new = thruPoint2d.y - m_new * thruPoint2d.x
        return Line2d(m_new, b_new, name)

    def Intersection(self, otherLine, name = None):
        x_int = (otherLine.b - self.b) / (self.m - otherLine.m)
        y_int = self.Y(x_int)
        return Point2d(x_int, y_int, name)

    def Shift(self, dx = math.nan, dy = math.nan):
        goodData = (0 if math.isnan(dx) else 2) + (0 if math.isnan(dy) else 1)
        if (goodData == 0):
            raise Exception("must specify either 'dx' or 'dy'")
        elif (goodData == 1): # dy was specified, dx was not
            new_b = self.b + dy
        elif (goodData == 2): # dx was specified, dy was not
            new_b = self.b + self.Y(dx)
        else: # both x1 and y1 were specified
            raise Exception("must not specify both 'dx' and 'dy'")
        
        return Line2d(self.Slope, new_b, self.Name)

class LineSegment2d:
    def __init__(self, p1, p2, name = None):
        self.line = Line2d.Thru2Points(p1, p2, name)
        self.p1 = p1
        self.p2 = p2

    def __str__(self) -> str:
        return f'{self.line} from {self.p1} to {self.p2}'

    @classmethod
    def WithCoordinates(cls, line, x1 = math.nan, y1 = math.nan, x2 = math.nan, y2 = math.nan, name = None):
        goodData = (0 if math.isnan(x1) else 2) + (0 if math.isnan(y1) else 1)
        if (goodData == 0):
            raise Exception("must specify either 'x' or 'y' of point 1")
        elif (goodData == 1): # y1 was specified, x1 was not
            x1 = line.X(y1)
        elif (goodData == 2): # x1 was specified, y1 was not
            y1 = line.Y(x1)
        else: # both x1 and y1 were specified
            raise Exception("must not specify both 'x' and 'y' of point 1")
    
        goodData = (0 if math.isnan(x2) else 2) + (0 if math.isnan(y2) else 1)
        if (goodData == 0):
            raise Exception("must specify either 'x' or 'y' of point 2")
        elif (goodData == 1): # y2 was specified, x2 was not
            x2 = line.X(y2)
        elif (goodData == 2): # x2 was specified, y2 was not
            y2 = line.Y(x2)
        else: # both x2 and y2 were specified
            raise Exception("must not specify both 'x' and 'y' of point 2")

        return LineSegment2d(Point2d(x1, y1), Point2d(x2, y2), name)
        
    @property
    def Line(self):
        return self.line
    
    @property
    def Point1(self):
        return self.p1
    
    @property
    def Point2(self):
        return self.p2
    
    @property
    def MidPoint(self):
        midX = (self.p1.x + self.p2.x) / 2.0
        midY = (self.p1.y + self.p2.y) / 2.0
        return Point2d(midX, midY)

    @property
    def Length(self):
        return Point2d.Distance(self.p1, self.p2)

    def ContainsPoint(self, pt): # assumes that pt lies on the line defined by the line segment
        mid = self.MidPoint
        dist = Point2d.Distance(pt, mid)
        if (dist < self.Length / 2.0):
            return True
        else:
            return False

    def Shift(self, *, dx = math.nan, dy = math.nan):
        return LineSegment2d(self.Point1.Shift(dx, dy), self.Point2.Shift(dx, dy))

    @property
    def Name(self):
        return self.Line.Name

    # calculate the surface area of a truncated cone assuming the axis of rotation is along the y axis
    def ConicalArea(self):
        area = math.pi * self.Length * (self.p1.x + self.p2.x)
        return area


class TwoCones:
    def __init__(self, segmentA, segmentB):
        self.A = segmentA
        self.B = segmentB
        area = math.nan
        zone = None

    def _CalcArea(self, segment):
        newArea = segment.ConicalArea()
        if (newArea < self.area):
            self.area = newArea
            self.zone = segment.Name

    def MinArea(self):
        # start by trying all of the conical sections defined by the end points of both line segments
        A1_B1 = LineSegment2d(self.A.p1, self.B.p1, f'{self.A.p1.Name} - {self.B.p1.Name}')
        self.area = A1_B1.ConicalArea()
        self.zone = A1_B1.Name
        A1_B2 = LineSegment2d(self.A.p1, self.B.p2, f'{self.A.p1.Name} - {self.B.p2.Name}')
        self._CalcArea(A1_B2)
        A2_B1 = LineSegment2d(self.A.p2, self.B.p1, f'{self.A.p2.Name} - {self.B.p1.Name}')
        self._CalcArea(A2_B1)
        A2_B2 = LineSegment2d(self.A.p2, self.B.p2, f'{self.A.p2.Name} - {self.B.p2.Name}')
        self._CalcArea(A2_B2)

        # next, look at the line segments going thru one of the endpoints and perpendicular to the other line segment
        # point defined by the interesction of a line perpendicular to A passing thru B at pt1 and line A
        ptA_B1 = self.A.Line.Perpendicular(self.B.p1).Intersection(self.A.Line)
        perpA_thruB1 = LineSegment2d(self.B.p1, ptA_B1, f'{self.A.Name} - {self.B.p1.Name}')
        if (self.A.ContainsPoint(ptA_B1)):
            self._CalcArea(perpA_thruB1)

        # point defined by the interesction of a line perpendicular to A passing thru B at pt2 and line A
        ptA_B2 = self.A.Line.Perpendicular(self.B.p2).Intersection(self.A.Line)
        perpA_thruB2 = LineSegment2d(self.B.p2, ptA_B2, f'{self.A.Name} - {self.B.p2.Name}')
        if (self.A.ContainsPoint(ptA_B2)):
            self._CalcArea(perpA_thruB2)

        # point defined by the interesction of a line perpendicular to B passing thru A at pt1 and line B
        ptB_A1 = self.B.Line.Perpendicular(self.A.p1).Intersection(self.B.Line) 
        perpB_thruA1 = LineSegment2d(self.A.p1, ptB_A1, f'{self.B.Name} - {self.A.p1.Name}')
        if (self.B.ContainsPoint(ptB_A1)):
            self._CalcArea(perpB_thruA1)

        # point defined by the interesction of a line perpendicular to B passing thru A at pt2 and line B
        ptB_A2 = self.B.Line.Perpendicular(self.A.p2).Intersection(self.B.Line) 
        perpB_thruA2 = LineSegment2d(self.A.p2, ptB_A2, f'{self.B.Name} - {self.A.p2.Name}')
        if (self.B.ContainsPoint(ptB_A2)):
            self._CalcArea(perpB_thruA2)

        return self.area, self.zone
   

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
#  diaFlatPlug - the diameter at the termination of the spherical radius on the lower corner
#  diaStem     - the diameter of the stem below the lower corner of the seat
#
# Plugs can contact the seat on the lower corner, upper corner, or on the bevel.
class SphericalPlug_BeveledSeat:
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
class BallPlug_BeveledSeat:
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
        self._vlv = SphericalPlug_BeveledSeat(diaSeat, angSeat, htSeat, srPlug, diaFlatPlug, diaStem)

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
class BallPlug_SquareSeat:
    def __init__(self, diaSeat, diaBall = 0.0 * un.Length.m, contactAngle = 0.0 * un.Angle.deg):
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
class ConicalPlug_SquareSeat:
    def __init__(self, diaSeat, diaPlugTip, angPlug):
        self._diaSeat = diaSeat.SIValue
        self._diaPlugTip = diaPlugTip.SIValue
        self._angPlug = angPlug.SIValue

        self._seat = Point2d(self._diaSeat / 2.0, 0, 'seat corner')

        self._xc = self._diaSeat / 2.0
        self._yc = 0.0

        plugContact = Point2d(self._xc, self._yc, 'plug contact')
        plug_line = Line2d.ThruPointWithSlope(plugContact, math.tan(math.pi / 2 - self._angPlug))
        cone_body_rad = self._xc * 100.0 # set the cone body diameter so large that it will never govern the flow area
        self._plug_segment = LineSegment2d.WithCoordinates(plug_line, x1 = self._diaPlugTip / 2.0, x2 = cone_body_rad, name='plug face')
        self._plug_segment.p1.name = 'plug tip'

        self._area_annular = math.pi / 4.0 * self._diaSeat ** 2
        self._area_zone = 'invalid'
        
    def FlowArea(self, stroke):
        _stroke = stroke.SIValue
        stroke_segment = self._plug_segment.Shift(dy = _stroke)

        # start by calculating the tip to corner conical area
        cornerSegment = LineSegment2d(stroke_segment.p1, self._seat, f'{stroke_segment.p1.Name} - {self._seat.Name}')
        area = cornerSegment.ConicalArea()
        self._area_zone = cornerSegment.Name

        # next, look at the line segments going thru the seat corner perpendicular to the cone segment
        normalPt = stroke_segment.Line.Perpendicular(self._seat).Intersection(stroke_segment.Line)
        normalSegment = LineSegment2d(normalPt, self._seat, f'{stroke_segment.Name} - {self._seat.Name}')
        if (stroke_segment.ContainsPoint(normalPt)):
            normalArea = normalSegment.ConicalArea()
            if (normalArea < area):
                area = normalArea
                self._area_zone = normalSegment.Name

        if (self._area_annular < area):
            area = self._area_annular
            self._area_zone = 'seat diameter'
    
        return area * un.Area.meterSq

    @property
    def ContactDia(self):
        return self._diaSeat * un.Length.m

    @property
    def ContactLocation(self):
        return 'seat corner'

    @property
    def AreaZone(self):
        return self._area_zone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq


# Calculate the flow area between a conical plug and square seat.
# All angles are taken from the axis of the part (half angles)
class ___OLD___ConicalPlug_SquareSeat:
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

        areaTruncCone = math.pi * gap * (xs + xp)

        area = min(areaTruncCone, self._area_annular)

        if (area == self._area_annular):
            self._area_zone = 'seat diameter'
    
        return area * un.Area.meterSq

    @property
    def ContactDia(self):
        return self._diaSeat * un.Length.m

    @property
    def ContactLocation(self):
        return 'seat corner'

    @property
    def AreaZone(self):
        return self._area_zone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq


# Calculate the flow area between a conical plug and beveled seat.
# All angles are taken from the axis of the part (half angles)
class ConicalPlug_BeveledSeat:
    def __init__(self, diaSeat, angSeat, htSeat, diaPlugTip, angPlug):
        self._diaSeat = diaSeat.SIValue
        self._angSeat = angSeat.SIValue
        self._htSeat = htSeat.SIValue
        self._diaPlugTip = diaPlugTip.SIValue
        self._angPlug = angPlug.SIValue

        # x1, y1 correspond to the lower corner of the seat
        self._x1 = self._diaSeat / 2.0             
        self._y1 = 0                                

        # x2, y2 correspond to the upper corner of the seat
        self._x2 = self._x1 + self._htSeat * math.tan(self._angSeat)
        self._y2 = self._y1 + self._htSeat

        seatLowerCorner = Point2d(self._x1, self._y1, 'seat lower corner')
        seatUpperCorner = Point2d(self._x2, self._y2, 'seat upper corner')
        self._seat_segment = LineSegment2d(seatLowerCorner, seatUpperCorner, name='seat face')

        if (self._angPlug > self._angSeat): # contact is at the upper corner of the seat.
            self._xc = self._x2
            self._yc = self._y2
            self._contact_location = 'upper corner'
        elif (self._angPlug < self._angSeat): # contact is at the lower corner of the seat
            self._xc = self._x1
            self._yc = self._y1
            self._contact_location = 'lower corner'
        else:
            self._xc = (self._x1 + self._x2) / 2.0
            self._yc = (self._y1 + self._y2) / 2.0
            self._contact_location = 'midway'

        plugContact = Point2d(self._xc, self._yc, 'plug contact')
        plug_line = Line2d.ThruPointWithSlope(plugContact, math.tan(math.pi / 2 - self._angPlug))
        cone_body_rad = self._x2 * 100.0 # set the cone body diameter so large that it will never govern the flow area
        self._plug_segment = LineSegment2d.WithCoordinates(plug_line, x1 = self._diaPlugTip / 2.0, x2 = cone_body_rad, name='plug face')
        self._plug_segment.p1.name = 'plug tip'

        self._area_annular = math.pi / 4.0 * self._diaSeat ** 2
        self._area_zone = 'invalid'
        
    def FlowArea(self, stroke):
        _stroke = stroke.SIValue
        vlv = TwoCones(self._seat_segment, self._plug_segment.Shift(dy = _stroke))
        area, self._area_zone = vlv.MinArea()

        if (self._area_annular < area):
            area = self._area_annular
            self._area_zone = 'seat bore'
        return area * un.Area.meterSq

    @property
    def ContactDia(self):
        return (self._xc * 2.0) * un.Length.m

    @property
    def ContactLocation(self):
        return self._contact_location

    @property
    def AreaZone(self):
        return self._area_zone

    @property
    def MaxArea(self):
        return self._area_annular * un.Area.meterSq

