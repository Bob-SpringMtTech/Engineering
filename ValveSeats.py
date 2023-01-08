import numpy as np
import matplotlib.pyplot as plt

from Library import unit_of_measure as um
from Library import NIST330 as un
from Library import Water as h2o

def uFormat(q, u, f):
    if(len(u.Symbol) > 0):
        str = f'{q.Value(u):{f}} {u.Symbol}'
    else:
        str = f'{q.Value(u):{f}}'

    return str

def poly(x, coeff):
    y = 0.0
    for i in range(len(coeff)-1):
        y = (coeff[i] + y) * x
    y += coeff[len(coeff)-1]

    return y

# Calculate the flow area between a spherical radius plug and beveled seat.
# All angles are taken from the axis of the part (half angles)
def FlowArea_SphPlug_BevSeat(diaSeat, angSeat, htSeat, srPlug, htPlug, diaStem, stroke):
    angSeatRad = angSeat.SIValue

    # x1, y1 correspond to the lower corner of the seat
    x1 = diaSeat.SIValue / 2.0             
    y1 = 0                                

    # x2, y2 correspond to the upper corner of the seat
    x2 = x1 + htSeat.SIValue * np.tan(angSeatRad)
    y2 = y1 + htSeat.SIValue

    # xc, yc correspond to the contact point between the seat and plug (ideal)
    xc = srPlug.SIValue * np.sin(np.pi / 2.0 - angSeatRad)
    yc = y1 + (xc - x1) / np.tan(angSeatRad)

    # x0, y0 correspond to the center of the spherical radius
    x0 = 0
    y0closed = srPlug.SIValue * np.sin(angSeatRad) + yc

    # x3, y3 correspond to the lower corner of the plug where the spherical radius ends
    x3 = np.sqrt(srPlug.SIValue ** 2 - htPlug.SIValue ** 2)
    y3closed = y0closed - htPlug.SIValue

    y0 = y0closed + stroke.SIValue
    y3 = y3closed + stroke.SIValue

    angCS = np.arctan((y0 - y2) / x2)
    angCP = np.arctan((y3 - y2) / (x2 - x3))
    if (y3 < y2):
        angCP = 0
    
    angFlow = max(angSeatRad, angCS, angCP)

    if (angFlow == angSeatRad):
        gap = stroke.SIValue * np.sin(angSeatRad)
        xp = xc
        xs = xp + gap * np.cos(angSeatRad)
        lCone = srPlug.SIValue
    elif (angFlow == angCS):
        gap = np.sqrt(((x2 - x0) ** 2) + ((y2 - y0) ** 2)) - srPlug.SIValue
        xs = x2
        xp = xs - gap * np.cos(angFlow)
        lCone = srPlug.SIValue
    elif (angFlow == angCP):
        gap = np.sqrt(((x2 - x3) ** 2) + ((y2 - y3) ** 2))
        xs = x2
        xp = x3
        lCone = xp / np.cos(angFlow)
    else:
        gap = 0.0

    areaTruncCone = np.pi * (lCone * (xs - xp) + xs * gap)

    areaAnnular = np.pi / 4.0 * (diaSeat.SIValue ** 2 - diaStem.SIValue ** 2)

    area = min(areaTruncCone, areaAnnular) * un.Area.meterSq

    return area


# Calculate the flow area between a ball plug and beveled seat.
# All angles are taken from the axis of the part (half angles)
def FlowArea_BallPlug_BevSeat(diaSeat, angSeat, htSeat, diaPlug, stroke):
    srPlug = diaPlug / 2.0
    htPlug = srPlug
    diaStem = 0.0 * uin  
    return FlowArea_SphPlug_BevSeat(diaSeat, angSeat, htSeat, srPlug, htPlug, diaStem, stroke)


# Calculate the flow area between a ball plug and square seat.
# All angles are taken from the axis of the part (half angles)
def FlowArea_BallPlug_SqSeat(diaSeat, angSeat, diaPlug, stroke):
    xs = diaSeat.SIValue / 2.0
    sr = diaPlug.SIValue / 2.0
    y0closed = np.sqrt(sr ** 2 - xs ** 2)
    y0open = y0closed + stroke.SIValue

    hypot = np.sqrt(y0open ** 2 + xs ** 2)
    gap = hypot - sr

    xp = xs * sr / hypot

    areaTruncCone = np.pi * (sr * (xs - xp) + xs * gap)

    areaAnnular = np.pi * xs ** 2

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
    y3 = - (x1 - x3) / np.tan(angPlugRad) + stroke.SIValue

    xs = x1
    gap = stroke.SIValue * np.sin(angPlugRad)
    xp = xs - gap * np.cos(angPlugRad)
    if (xp > x3): # cone is limiting the flow area
        lCone = xp / np.cos(angPlugRad)
    else: # cone is fully retracted from the seat
        xp = x3
        gap = np.sqrt(((x1 - x3) ** 2) + ((y1 - y3) ** 2))
        lCone = x3 * gap / (x1 - x3)

    areaTruncCone = np.pi * (lCone * (xs - xp) + xs * gap)

    areaAnnular = np.pi / 4.0 * diaSeat.SIValue

    area = min(areaTruncCone, areaAnnular) * un.Area.meterSq
   
    return area


utf = un.Temperature.degF
upsig = un.Pressure.psig
upsia = un.Pressure.psia
upsi = un.Pressure.psi
ulbf = un.Force.lbf
uin = un.Length.inch
usqin = un.Area.inSq
udeg = un.Angle.deg

area = FlowArea_BallPlug_BevSeat(1.000 * uin, 30.0 * udeg, 0.040 * uin, 1.18136721 * uin, 0.125 * uin )
print(f'BB flow area= {uFormat(area, usqin, "0.5f")}')

area = FlowArea_BallPlug_SqSeat(1.000 * uin, 30.0 * udeg, 1.18136721 * uin, 0.25084678 * uin )
print(f'BS flow area= {uFormat(area, usqin, "0.5f")}')

area = FlowArea_SphPlug_BevSeat(1.500 * uin, 30.0 * udeg, 0.040 * uin, 0.875 * uin, 0.5625 * uin, 0.3125 * uin, 0.525 * uin)
print(f'SB flow area= {uFormat(area, usqin, "0.5f")}')

area = FlowArea_ConePlug_SqSeat(0.375 * uin, 0.250 * uin, 30.0 * udeg, 0.200 * uin)
print(f'CS flow area = {uFormat(area, usqin, "0.5f")}')

