# B31_3_Para304_1_2(P, D, d, c, S, E, W, t_act = (0.0 * uin))
#   P: design pressure
#   D: outside diameter
#   d: inside diameter
#   c: sum of allowances - mechanical, corrosion
#   S: stress value from B31.3 table A-1
#   E: quality factor from B31.3 table A-1A or A-1B
#   W: weld joint strength reduction factor per B31.3 para 302.3.5(e)
#   t_act: actual thickness to be compared with calculated required thickness
#   returns: required pipe wall thickness
#
# UG34_C_2_Eq1(d, P, S, C, E, t_act = (0.0 * uin))
#   d: diameter, or short span, measured as indicated in VIII, Div 1 Fig. UG-34
#   P: internal design pressure
#   S: maximum allowable stress value in tension from applicable table of stress values referenced by VIII, Div 1 UG-23
#   C: a factor depending upon the method of attachment of head, shell dimensions, and other items as listed in UG-34(d), 
#      dimensionless. The factors for welded covers also include a factor of 0.667 that effectively increases the allowable
#      stress for such constructions to 1.5S.
#   E: joint efficiency, from VIII, Div 1 Table UW-12, of any Category A weld as defined in VIII, Div 1 UW-3(a)(1)
#   t_act: actual thickness to be compared with calculated required thickness
#   returns: required head thickness
#
# AppII_Dims(bo, od_contact_face, bolt_cir_dia)
#   bo: basic gasket seating width (from Table 2-5.2)
#   od_contact_face: outer diameter of the contact face between the gasket and the flange
#   bolt_cir_dia: bolt circle diameter of the flange
#   returns: G (diameter at location of gasket load reaction), hg (gasket moment arm), and b (effective gasket or 
#            joint-contact-surface seating width [see VIII, Div 1, App 2, Note 1, 2-5(c)(1)])
#
# AppII_Wm1(P, G, b, m)
#   P: internal design pressure
#   G: diameter at location of gasket load reaction
#   b: effective gasket or joint-contact-surface seating width [see VIII, Div 1, App 2, Note 1, 2-5(c)(1)]
#   m: gasket factor, obtain from Table 2-5.1 [see VIII, Div 1, App 2, Note 1, 2-5(c)(1)]
#   returns: Wm1 (minimum required bolt load for the operating conditions [see 2-5(c)])
#
# AppII_Wm2(G, b, y)
#   G: diameter at location of gasket load reaction
#   b: effective gasket or joint-contact-surface seating width [see VIII, Div 1, App 2, Note 1, 2-5(c)(1)]
#   y: gasket or joint-contact-surface unit seating load, [see VIII, Div 1, App 2, Note 1, 2-5(c)]
#   returns: Wm2 (minimum required bolt load for gasket seating [see VIII, Div 1, App 2, 2-5(c)])
#
# UG34_C_2_Eq2_Operating(d, P, S1, Wm1, hg, C, E)
#   d: diameter, or short span, measured as indicated in VIII, Div 1 Fig. UG-34
#   P: internal design pressure
#   S1: maximum allowable stress value in tension at the operating temperature from applicable table of stress values 
#       referenced by VIII, Div 1 UG-23
#   Wm1: minimum required bolt load for the operating conditions from VIII, Div 1, App 2 Formula (3) of 2-5(e)
#   hg: gasket moment arm, equal to the radial distance from the centerline of the bolts to the line of the gasket reaction,
#       as shown in VIII, Div 1, App 2 Table 2-5.2
#   C: a factor depending upon the method of attachment of head, shell dimensions, and other items as listed in UG-34(d), 
#      dimensionless. The factors for welded covers also include a factor of 0.667 that effectively increases the allowable
#      stress for such constructions to 1.5S.
#   E: joint efficiency, from VIII, Div 1 Table UW-12, of any Category A weld as defined in VIII, Div 1 UW-3(a)(1)
#   returns: required head thickness to satisfy the operating load
#
# UG34_C_2_Eq2_Gasket(d, S2, W2, hg, E)
#   d: diameter, or short span, measured as indicated in VIII, Div 1 Fig. UG-34
#   S2: maximum allowable stress value in tension at atmospheric temperature from applicable table of stress values 
#       referenced by VIII, Div 1 UG-23
#   Wm2: minimum required bolt load for the gasket seating conditions from VIII, Div 1, App 2 Formula (4) of 2-5(e)
#   hg: gasket moment arm, equal to the radial distance from the centerline of the bolts to the line of the gasket reaction,
#       as shown in VIII, Div 1, App 2 Table 2-5.2
#   E: joint efficiency, from VIII, Div 1 Table UW-12, of any Category A weld as defined in VIII, Div 1 UW-3(a)(1)
#   returns: required head thickness to satisfy the gasket seating load
#
# UG34_C_2_Eq2(d, P, S1, S2, W1, W2, hg, C, E, t_act = (0.0 * uin))
#   d: diameter, or short span, measured as indicated in VIII, Div 1 Fig. UG-34
#   P: internal design pressure
#   S1: maximum allowable stress value in tension at the operating temperature from applicable table of stress values 
#       referenced by VIII, Div 1 UG-23
#   S2: maximum allowable stress value in tension at atmospheric temperature from applicable table of stress values 
#       referenced by VIII, Div 1 UG-23
#   Wm1: minimum required bolt load for the operating conditions from VIII, Div 1, App 2 Formula (3) of 2-5(e)
#   Wm2: minimum required bolt load for the gasket seating conditions from VIII, Div 1, App 2 Formula (4) of 2-5(e)
#   hg: gasket moment arm, equal to the radial distance from the centerline of the bolts to the line of the gasket reaction,
#       as shown in VIII, Div 1, App 2 Table 2-5.2
#   C: a factor depending upon the method of attachment of head, shell dimensions, and other items as listed in UG-34(d), 
#      dimensionless. The factors for welded covers also include a factor of 0.667 that effectively increases the allowable
#      stress for such constructions to 1.5S.
#   E: joint efficiency, from VIII, Div 1 Table UW-12, of any Category A weld as defined in VIII, Div 1 UW-3(a)(1)
#   returns: required head thickness to satisfy both the operating and gasket seating loads
#
# AppII_Bolting(S, Wm, bolt_thd, N)
#   S: maximum allowable stress value in tension at the appropriate temperature from applicable table of stress values 
#      referenced by VIII, Div 1 UG-23
#   Wm: minimum required bolt load for the appropriate conditions from VIII, Div 1, App 2 Formula (3) or (4) of 2-5(e)
#   bolt_thd: an instance of class ThreadUN specifying size, tpi, series, and cls
#   N: number of bolts
#   returns: the actual bolting stress for the given conditions
#
# B16_34_Min_Wall_Thickness(Pc, dia, t_act = (0.0 * uin))
#   Pc: pressure class
#   dia: inside diameter.  See B16.34 para 6.1.2 for specifics
#   t_act: actual thickness to be compared with calculated required thickness
#   returns: required wall thickness
#
# B16_34_Bolted_Cover_Joint(Pc, Dg, bolt_thd, N, Sa)
#   Pc: pressure class
#   Dg: diameter bounded by the effective outside periphery of a gasket or O-ring or other seal-effective periphery
#   bolt_thd: an instance of class ThreadUN specifying size, tpi, series, and cls
#   N: number of bolts
#   Sa: allowable bolt stress at 38°C (100°F)
#   returns: the actual bolting stress for the given conditions
#
# B16_34_Threaded_Cover_Joint(Pc, Dg, cover_thd, LE)
#   Pc: pressure class
#   Dg: diameter bounded by the effective outside periphery of a gasket or O-ring or other seal-effective periphery
#   cover_thd: an instance of class ThreadUN specifying size, tpi, series, and cls
#   LE: length of thread engagement
#   returns: the actual bolting stress for the given conditions
#
# B16_34_Bolted_Body_Joint(Pc, Dg, bolt_thd, N, Sa)
#   Pc: pressure class
#   Dg: diameter bounded by the effective outside periphery of a gasket or O-ring or other seal-effective periphery
#   bolt_thd: an instance of class ThreadUN specifying size, tpi, series, and cls
#   N: number of bolts
#   Sa: allowable bolt stress at 38°C (100°F)
#   returns: the actual bolting stress for the given conditions

import numpy as np
import math

from Engineering import unit_of_measure as um
from Engineering import NIST330 as un
from Engineering import Threads as Threads

utf = un.Temperature.degF
upsig = un.Pressure.psig
upsia = un.Pressure.psia
upsi = un.Pressure.psi
ulbf = un.Force.lbf
uin = un.Length.inch
uksi = um.Unit('ksi', upsi.Dimension, upsi.Factor * 1000.0)
usqin = un.Area.inSq
uul = un.Dimensionless.none

# units of measure and formats for printed values
ulen = uin
flen = '0.3f'

upr = upsi
fpr = '0.0f'

ust = uksi
fst = '0.3f'

ufr = ulbf
ffr = '0.0f'

uar = usqin
far = '0.6f'

ful = '0.3f' # format string for unitless values

Test_Fail_Str = '\n  ***** Test Failed *****\n'
Test_Pass_Str = 'Test Passed'

def uFormat(q, u, f):
    if(len(u.Symbol) > 0):
        str = f'{q.Value(u):{f}} {u.Symbol}'
    else:
        str = f'{q.Value(u):{f}}'

    return str

verbose = True


# B31.3 304.1 - Pressure Design of Straight Pipe

def B31_3_Table304_1_1(D, d, c):
    t = (D - d) / 2.0
    if (t < (D / 6.0)):
        Y = 0.40 * uul
        f_str =  '  Y = from Table 304.1.1 (valid for temperatures up to 900F, other than cast iron)'
        v_str = f'  Y = {uFormat(Y, uul, "0.3f")}'
    else:
        Y = (d + c * 2.0) / (D + d + c * 2.0)
        f_str = '  Y = (d + 2*c) / (D + d + 2*c)'
        v_str = f'  Y = {uFormat(Y, uul, "0.3f")} = ({uFormat(d, ulen, flen)} + 2 * {uFormat(c, ulen, flen)}) / ({uFormat(D, ulen, flen)} + {uFormat(d, ulen, flen)} + 2 * {uFormat(c, ulen, flen)})'

    if (verbose):
        print(f_str)
        print(v_str)

    return Y
 
def B31_3_Para304_1_2(P, D, d, c, S, E, W, t_act = (0.0 * uin)):
    if (verbose):
        print(f'Calculate required wall thickness per ASME B31.3 Para 304.1.2 eq(3a)')
    if ((P / S / E).Value(uul) > 0.385):
        t = np.nan * uin
        if (verbose):
            print('***error: P/SE > 0.385 - See B31.3 304.1.2(b)')
    elif (d * 1.5 < D):
        t = np.nan * uin
        if (verbose):
            print('***error: t >= D / 6 - See B31.3 304.1.2(b)')
    else:
        Y = B31_3_Table304_1_1(D, d, c)
        t = (P * D) / ((S * E * W) + (P * Y)) / 2.0

        f_str = '  t = (P*D) / (2 * (S*E*W + P*Y))'
    
        if (verbose):
            st = uFormat(t, ulen, flen)
            sP = uFormat(P, upr, fpr)
            sD = uFormat(D, ulen, flen)
            sS = uFormat(S, ust, fst)
            sE = uFormat(E, uul, ful)
            sW = uFormat(W, uul, ful)
            sY = uFormat(Y, uul, ful)
            print(f_str)
            print(f'  t = {st} = ({sP} * {sD}) / (2 * ({sS} * {sE} * {sW} + {sP} * {sY})')

            if (t_act.Value(uin) > 0.0):
                st_act = uFormat(t_act, ulen, flen)
                if (t > t_act):
                    print(f'  t > t act {st_act}')
                    print(f'  {st} > {st_act}')
                    status = Test_Fail_Str
                else:
                    status = Test_Pass_Str
                    print(f'  t <= t act {st_act}')
                    print(f'  {st} <= {st_act}')
                print(f'  {status}')

    return t



def UG34_C_2_Eq1(d, P, S, C, E, t_act = (0.0 * uin)):

    if (verbose):
        print(f'Calculate required flat head thickness per Sec VII, Div 1, UG-34(c)(2) eqn (1) - no edge moments')

    t = d * (C * P / S / E).sqrt()
    f_str = '  t = d * sqrt((C*P) / (S*E))'

    if (verbose):
        print(f_str)

        sd = uFormat(d, ulen, flen)
        st = uFormat(t, ulen, flen)
        sd = uFormat(d, ulen, flen)
        sP = uFormat(P, upr, fpr)
        sS = uFormat(S, ust, fst)
        sC = uFormat(C, uul, ful)
        sE = uFormat(E, uul, ful)

        print(f'  t = {st} = {sd} * sqrt(({sC} * {sP}) / ({sS} * {sE}))')

        if (t_act.Value(uin) > 0.0):
            st_act = uFormat(t_act, ulen, flen)
            if (t > t_act):
                print(f'  t > t act {st_act}')
                print(f'  {st} > {st_act}')
                status = Test_Fail_Str
            else:
                status = Test_Pass_Str
                print(f'  t <= t act {st_act}')
                print(f'  {st} <= {st_act}')
            print(f'  {status}')


    return t

def AppII_Dims(bo, od_contact_face, bolt_cir_dia):
    if (verbose):
        print(f'Calculate flange gasket dimensions G (diameter of gasket load reaction), hg (bolt load moment arm), and b (effective sealing width) per Appendix II')
    
    b = bo
    f1_str = '  b = bo'
    if (bo.Value(uin) > 0.250):
        b = (math.sqrt(bo.Value(uin)) / 2.0) * uin
        f1_str = '  b = sqrt(bo) / 2'

    G = od_contact_face - b * 2.0
    hg = (bolt_cir_dia - G) / 2.0

    f2_str = '  G = OD_face - 2 * b'
    f3_str = '  hg = (bc - G) / 2'

    if (verbose):
        bs   = uFormat(b, ulen, flen)
        bos  = uFormat(bo, ulen, flen)
        cfs  = uFormat(od_contact_face, ulen, flen)
        bcs  = uFormat(bolt_cir_dia, ulen, flen)
        Gs   = uFormat(G, ulen, flen)
        hgs  = uFormat(hg, ulen, flen)

        if (bo.Value(uin) > 0.250):
            v1_str = f'  b = {bs} = sqrt({bos}) / 2'
        else:
            v1_str = f'  b = {bs}'

        print(f1_str)
        print(v1_str)
        print(f2_str)
        print(f'  G = {Gs} = {cfs} - 2 * {bs}')
        print(f3_str)
        print(f'  hg = {hgs} = ({bcs} - {Gs}) / 2')

    return G, hg, b
    
def AppII_Wm1(P, G, b, m):

    Wm1 = (G.squared() * P / 4.0 + b * G * P * m * 2.0) * math.pi
    f_str = '  Wm1 = pi * (G^2 * P / 4.0 + 2 * b * G * m * P)'

    Wm1s = uFormat(Wm1, ufr, ffr)

    if (verbose):
        print(f_str)
        sWm1 = uFormat(Wm1, ufr, ffr)
        sP   = uFormat(P, upr, fpr)
        sG   = uFormat(G, ulen, flen)
        sb   = uFormat(b, ulen, flen)
        sm   = uFormat(m, uul, ful)

        print(f'  Wm1 = {sWm1} = pi * (({sG})^2 * {sP} / 4.0 + 2 * {sb} * {sG} * {sm} * {sP})')

    return Wm1

def AppII_Wm2(G, b, y):

    Wm2 = b * G * y * math.pi
    f_str = '  Wm2 = pi * b * G * y'

    sWm2 = uFormat(Wm2, ufr, ffr)
    sb   = uFormat(b, ulen, flen)
    sG   = uFormat(G, ulen, flen)
    sy   = uFormat(y, upr, fpr)

    if (verbose):
        print(f_str)
        print(f'  Wm2 = {sWm2} = pi * {sb} * {sG} * {sy}')

    return Wm2

def UG34_C_2_Eq2_Operating(d, P, S1, W1, hg, C, E):
    # S1 and W1 correspond to the operating load case

    t = d * (C * P / S1 / E + W1 * hg / S1 / E / d.cubed()).sqrt()
    f_str = '  t1 = d * sqrt( (C*P)/(S*E) + (1.9*W*hg) / (S*E*d^3) )   UG34(c)(2)(2) operating loads'

    if (verbose):
        print(f_str)

        st = uFormat(t, ulen, flen)
        sd = uFormat(d, ulen, flen)
        sP = uFormat(P, upr, fpr)
        sS = uFormat(S1, ust, fst)
        sC = uFormat(C, uul, ful)
        sE = uFormat(E, uul, ful)
        sW = uFormat(W1, ufr, ffr)
        shg = uFormat(hg, ulen, flen)
        print(f'  t1 = {st} = {sd} * sqrt( ({sC}* {sP}) / ({sS} * {sE}) + (1.9 * {sW} * {shg}) / ({sS} * {sE} * ({sd})^3) )')

    return t

def UG34_C_2_Eq2_Gasket(d, S2, W2, hg, E):
    # S2 and W2 correspond to the gasket seating case
    t = d * (W2 * hg / S2 / E / d.cubed()).sqrt()
    f_str = '  t2 = d * sqrt( (1.9*W*hg) / (S*E*d^3) )   UG34(c)(2)(2) gasket seating loads'
    ts = uFormat(t, ulen, flen)
    ds = uFormat(d, ulen, flen)
    Ss = uFormat(S2, ust, fst)
    Es = uFormat(E, uul, ful)
    Ws = uFormat(W2, ufr, ffr)
    hgs = uFormat(hg, ulen, flen)

    if (verbose):
        print(f_str)
        print(f'  t2 = {ts} = {ds} * sqrt( (1.9 * {Ws} * {hgs}) / ({Ss} * {Es} * ({ds})^3) )')

    return t

def UG34_C_2_Eq2(d, P, S1, S2, W1, W2, hg, C, E, t_act = (0.0 * uin)):
    # S1 and W1 dorrespond to the operating load case
    # S2 and W2 correspond to the gasket seating case

    if (verbose):
        print(f'Calculate required flat head thickness per Sec VII, Div 1, UG-34(c)(2) eqn (2) - with edge moments')

    t1 = UG34_C_2_Eq2_Operating(d, P, S1, W1, hg, C, E)
    t2 = UG34_C_2_Eq2_Gasket(d, S2, W2, hg, E)

    if (t1 > t2):
        t = t1
        s3 = '  Operating loads govern'
    else:
        t = t2
        s3 = '  Gasket seating loads govern'

    if (verbose):
        st  = uFormat(t, ulen, flen)
        st1 = uFormat(t1, ulen, flen)
        st2 = uFormat(t2, ulen, flen)
        
        print('  t = max(t1, t2)')
        print(f'  t = {st} = max({st1}, {st2})')
        print(s3)

        if (t_act.Value(uin) > 0.0):
            st_act = uFormat(t_act, ulen, flen)
            if (t > t_act):
                print(f'  t > t act {st_act}')
                print(f'  {st} > {st_act}')
                status = Test_Fail_Str
            else:
                status = Test_Pass_Str
                print(f'  t <= t act {st_act}')
                print(f'  {st} <= {st_act}')
            print(f'  {status}')

    return t

def AppII_Bolting(S, Wm, bolt_thd, N):
    if (verbose):
        print(f'Calculate required bolting area and compare to actual, Sec VIII, Div 1, Appendix II para 2-3')

    f1_str = '  A reqd = Wm / S'
    a_reqd = Wm / S

    tsa = bolt_thd.TensileArea() * usqin
    a_act = tsa * N
    f2_str = '  A act = Thread Tensile Area * N'

    if (a_reqd > a_act):
        status = Test_Fail_Str
    else:
        status = Test_Pass_Str

    S_act = Wm / a_act
    f3_str = '  S act = Wm / a act'

    if (verbose):
        stsa = uFormat(tsa, uar, far)
        sa_act = uFormat(a_act, uar, far)
        sS = uFormat(S, upr, fpr)
        sWm = uFormat(Wm, ufr, ffr)
        sbolt = f'{bolt_thd}'
        sN = f'{N}'
        sa_reqd = uFormat(a_reqd, uar, far)
        sS_act = uFormat(S_act, upr, fpr)
        
        print(f1_str)
        print(f'  A reqd = {sa_reqd} = {sWm} / {sS}')               
        print(f2_str)
        print(f'  A act = {sa_act} = {stsa} * {sN}')
        print(f3_str)
        print(f'  S act = {sS_act} = {sWm} / {sa_act}')
        print(f'  {status}\n')


    return S_act


def B16_34_Min_Wall_Thickness(Pc, dia, t_act = (0.0 * uin)):
    global verbose
    if (verbose):
        print(f'Calculate minimum wall thickness, B16.34 para 6.1.1 and 6.1.2')

    cClass = 0
    cDmax = 1
    cM = 2
    cB = 3

    pressure_classes = [150, 300, 600, 900, 1500, 2500, 4500]

    Table_VI_2 = []
    Table_VI_2.append([150, 2.00, 0.064, 0.092])
    Table_VI_2.append([150, 4.00, 0.020, 0.180])
    Table_VI_2.append([150, 60.0, 0.163, 0.185])
    
    Table_VI_2.append([300, 1.00, 0.080, 0.090])
    Table_VI_2.append([300, 2.00, 0.070, 0.100])
    Table_VI_2.append([300, 60.0, 0.033, 0.180])
    
    Table_VI_2.append([600, 1.00, 0.0860, 0.100])
    Table_VI_2.append([600, 2.00, 0.0580, 0.130])
    Table_VI_2.append([600, 60.0, 0.0675, 0.110])
    
    Table_VI_2.append([900, 1.00, 0.15000, 0.090])
    Table_VI_2.append([900, 2.00, 0.05900, 0.190])
    Table_VI_2.append([900, 50.0, 0.10449, 0.100])
 
    Table_VI_2.append([1500, 50.0, 0.18443, 0.100])
    Table_VI_2.append([2500, 50.0, 0.34091, 0.100])
    Table_VI_2.append([4500, 50.0, 0.78488, 0.100])
    
    d_in = dia.Value(uin)
    if (d_in < 0.120):
        print("Diameters less than 0.12 inches are not valid")
        return np.nan * uin

    Pc_psi = np.round(Pc.Value(upsi), 0)
    if (Pc_psi < 150):
        print("Pressure classes less than 150 are not valid")
        return np.nan * uin

    if (Pc_psi > 4500):
        print("Pressure classes greater than 4500 are not valid")
        return np.nan * uin

    t_in = -1.0
    
    for row in range(len(Table_VI_2)):
        if (Pc_psi == Table_VI_2[row][cClass]): # Scan the table to find the correct diameter row
            if (d_in < Table_VI_2[row][cDmax]): # Scan the table for an exact pressure class match
                m = Table_VI_2[row][cM]
                b = Table_VI_2[row][cB]
                t_in = (d_in * m + b)
                break

    low_row = 0
    if (t_in < 0.0): # Scan thru table failed to locate the correct row, try interpolating
        for row in range(len(pressure_classes)):
            if (Pc_psi > pressure_classes[row]):
                low_row = row

        low_pc   = pressure_classes[low_row]
        high_pc  = pressure_classes[low_row+1]
        save_verbose = verbose
        verbose = False
        low_thk  = B16_34_Min_Wall_Thickness((low_pc * upsi), dia).Value(uin)
        high_thk = B16_34_Min_Wall_Thickness((high_pc * upsi), dia).Value(uin)
        verbose = save_verbose
        
        if (not np.isnan(low_thk)):
            if (not np.isnan(high_thk)):
                m = (high_thk - low_thk) / (high_pc - low_pc)
                t_in = low_pc * m + low_thk
    
    if (t_in < 0.0):
        t = np.nan * uin
        print("***** Input out of range.  Calculation failed *****")
    else:
        t = np.round(t_in, 2) * uin
        if (verbose):
            st = uFormat(t, ulen, flen)
            sPc = uFormat(Pc, upr, fpr)
            sdia = uFormat(dia, ulen, flen)
            print(f'  Pc  = {sPc}')
            print(f'  Dia = {sdia}')
 
            if (t_act.Value(uin) > 0.0):
                st_act = uFormat(t_act, ulen, flen)
                if (t > t_act):
                    status = Test_Fail_Str
                    print(f'  t act < t')
                    print(f'  {st_act} < {st}')
                else:
                    status = Test_Pass_Str
                    print(f'  t act >= t')
                    print(f'  {st_act} >= {st}')
                print(f'  {status}')

    return t


def B16_34_Bolted_Cover_Joint(Pc, Dg, bolt_thd, N, Sa):
    if (verbose):
        print(f'Calculate required tensile stress area of the cover bolting and compare to actual, B16.34 para 6.4.1.1')

    f1_str = '  Ag = pi / 4 * Dg^2'
    f2_str = '  As = Thread tensile area * N'
    f3_str = '  Pc * Ag / Ab <= K1 * Sa <= 9000'
    
    Ag = Dg.squared() * math.pi / 4.0
    Ab = bolt_thd.TensileArea() * usqin * N
    
    S_act = Pc * Ag / Ab
    S_lim = 9000.0 * upsi
    S_max = Sa * 0.45
    if (S_max > S_lim):
        S_max = S_lim

    if (S_act > S_lim):
        status = Test_Fail_Str
    else:
        status = Test_Pass_Str

    if (verbose):
        sPc = uFormat(Pc, upr, fpr)
        sDg = uFormat(Dg, ulen, flen)
        sAg = uFormat(Ag, uar, far)
        sthd = f'{bolt_thd}'
        sAb = uFormat(Ab, uar, far)
        sSa = uFormat(Sa, upr, fpr)
        sS_act = uFormat(S_act, upr, fpr)

        print(f1_str)
        print(f'  Ag = {sAg} = pi / 4 * ({sDg})^2')
        print(f2_str)
        print(f'  {sthd} x {N} bolts')
        print(f'  Ab = {sAb}')
        print(f3_str)
        print(f'  {sPc} * {sAg} / {sAb}  = {sS_act} <= 0.45 * {sSa} <= 9000')
        print(f'  {status}\n')

    return S_act   


def B16_34_Threaded_Cover_Joint(Pc, Dg, cover_thd, LE):
    if (verbose):
        print(f'Calculate required shear area of the cover and compare to actual, B16.34 para 6.4.1.2')

    f1_str = '  Ag = pi / 4 * Dg^2'
    f2_str = '  As = Thread shear area'
    f3_str = '  Pc * Ag / As <= 4200'
    
    Ag = Dg.squared() * math.pi / 4.0
    cover_thd.LE = LE.Value(uin)
    Asi = cover_thd.ShearAreaInternal()
    Asx = cover_thd.ShearAreaExternal()
    if (Asi < Asx):
        As = Asi * usqin
    else:
        As = Asx * usqin

    S_act = Pc * Ag / As
    S_lim = 4200.0 * upsi

    if (S_act > S_lim):
        status = Test_Fail_Str
    else:
        status = Test_Pass_Str

    if (verbose):
        sPc = uFormat(Pc, upr, fpr)
        sDg = uFormat(Dg, ulen, flen)
        sAg = uFormat(Ag, uar, far)
        sthd = f'{cover_thd}'
        sLE = uFormat(LE, ulen, flen)
        sAs = uFormat(As, uar, far)
        sS_act = uFormat(S_act, upr, fpr)

        print(f1_str)
        print(f'  Ag = {sAg} = pi / 4 * ({sDg})^2')
        print(f2_str)
        print(f'  {sthd}  length of engagement = {sLE}')
        print(f'  As = {sAs}')
        print(f3_str)
        print(f'  {sPc} * {sAg} / {sAs} = {sS_act} <= 4200')
        print(f'  {status}\n')


    return S_act   


def B16_34_Bolted_Body_Joint(Pc, Dg, bolt_thd, N, Sa):
    if (verbose):
        print(f'Calculate required tensile stress area of the body joint bolting and compare to actual, B16.34 para 6.4.2.1')

    f1_str = '  Ag = pi / 4 * Dg^2'
    f2_str = '  As = Thread tensile area * N'
    f3_str = '  Pc * Ag / Ab <= K2 * Sa <= 7000'
    
    Ag = Dg.squared() * math.pi / 4.0
    Ab = bolt_thd.TensileArea() * usqin * N
    
    S_act = Pc * Ag / Ab
    S_lim = 7000.0 * upsi
    S_max = Sa * 0.35
    if (S_max > S_lim):
        S_max = S_lim

    if (S_act > S_lim):
        status = Test_Fail_Str
    else:
        status = Test_Pass_Str

    if (verbose):
        sPc = uFormat(Pc, upr, fpr)
        sDg = uFormat(Dg, ulen, flen)
        sAg = uFormat(Ag, uar, far)
        sthd = f'{bolt_thd}'
        sAb = uFormat(Ab, uar, far)
        sSa = uFormat(Sa, upr, fpr)
        sS_act = uFormat(S_act, upr, fpr)

        print(f1_str)
        print(f'  Ag = {sAg} = pi / 4 * ({sDg})^2')
        print(f2_str)
        print(f'  {sthd} x {N} bolts')
        print(f'  Ab = {sAb}')
        print(f3_str)
        print(f'  {sPc} * {sAg} / {sAb}  = {sS_act} <= 0.35 * {sSa} <= 7000')
        print(f'  {status}\n')

    return S_act   


def B16_34_Threaded_Body_Joint(Pc, Dg, cover_thd, LE):
    if (verbose):
        print(f'Calculate required shear area of the cover and compare to actual, B16.34 para 6.4.2.2')

    f1_str = '  Ag = pi / 4 * Dg^2'
    f2_str = '  As = Thread shear area'
    f3_str = '  Pc * Ag / As <= 3300'
    
    Ag = Dg.squared() * math.pi / 4.0
    cover_thd.LE = LE.Value(uin)
    Asi = cover_thd.ShearAreaInternal()
    Asx = cover_thd.ShearAreaExternal()
    if (Asi < Asx):
        As = Asi * usqin
    else:
        As = Asx * usqin

    S_act = Pc * Ag / As
    S_lim = 3300.0 * upsi

    if (S_act > S_lim):
        status = Test_Fail_Str
    else:
        status = Test_Pass_Str

    if (verbose):
        sPc = uFormat(Pc, upr, fpr)
        sDg = uFormat(Dg, ulen, flen)
        sAg = uFormat(Ag, uar, far)
        sthd = f'{cover_thd}'
        sLE = uFormat(LE, ulen, flen)
        sAs = uFormat(As, uar, far)
        sS_act = uFormat(S_act, upr, fpr)

        print(f1_str)
        print(f'  Ag = {sAg} = pi / 4 * ({sDg})^2')
        print(f2_str)
        print(f'  {sthd}  length of engagement = {sLE}')
        print(f'  As = {sAs}')
        print(f3_str)
        print(f'  {sPc} * {sAg} / {sAs} = {sS_act} <= 3300')
        print(f'  {status}\n')


    return S_act   

def Wm2_Flat_Face(od, id, hd, N, y):
    if (verbose):
        print(f'Calculate the gasket seating load for a flat face gasket using the Garlock Design Spreadsheet Formulas')

    f1_str = '  Ag = pi / 4 * (od^2 - id^2 * N * hd)'
    f2_str = '  Wm2 = Ag * y'

    ag = (od.squared() - id.squared() - hd.squared() * N) * np.pi / 4.0
    Wm2 = ag * y

    if (verbose):
        sAg  = uFormat(ag, uar, far)
        sod  = uFormat(od, ulen, flen)
        sid  = uFormat(id, ulen, flen)
        shd  = uFormat(hd, ulen, flen)
        sy   = uFormat(y, upr, fpr)
        sWm2 = uFormat(Wm2, ufr, ffr)
        
        print(f1_str)
        print(f'  Ag = {sAg} = pi / 4 * (({sod})^2 - ({sid})^2 * N * ({shd}))')
        print(f2_str)
        print(f'  Wm2 = {Wm2} = {sAg} * {sy}')

    return Wm2

