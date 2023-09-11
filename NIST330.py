import numpy as np
import unit_of_measure as um

class Acceleration:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,  -2,   0,   0,   0,     0,    0])
    g = um.Unit('g', _dim, 9.80665)
    Gal = um.Unit('Gal', _dim, 1.0)

class AbsorbedDose:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Gray = um.Unit('Gy', _dim, 1.0)

class Activity:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Becquerel = um.Unit('Bq', _dim, 1.0)

class Amount:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   1,     0,    0])
    Mol = um.Unit('Mol', _dim, 1.0)

class Angle:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    Radian = um.Unit('rad', _dim, 1.0)
    deg = um.Unit('°', _dim, np.pi / 180.0)
    grad = um.Unit('grad', _dim, 1.57079632679E-2)
    gon = um.Unit('gon', _dim,  1.57079632679E-2)
    mil = um.Unit('mil', _dim, 9.817477E-4)
    min = um.Unit("'", _dim, 2.90888208666E-4)
    rev = um.Unit('r', _dim, 2.0 * np.pi)
    sec = um.Unit('"', _dim, 4.8481368111E-6)
    Steradian = um.Unit('sr', _dim, 1.0)
    
class Area:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,   0,   0,   0,   0,     0,    0])
    meterSq = um.Unit('m^2', _dim, 1.0)
    mmSq = um.Unit('mm^2', _dim, 0.001 ** 2)
    acre = um.Unit('acre', _dim, 4046.87260987)
    are = um.Unit('a', _dim, 100.0)
    barn = um.Unit('b', _dim, 1.0E-28)
    cmil = um.Unit('cmil', _dim, 5.06707479097498e-10)
    hectare = um.Unit('ha', _dim, 10000.0)
    ftSq = um.Unit('ft^2', _dim, 0.3048 ** 2)
    inSq = um.Unit('in^2', _dim, 0.0254 ** 2)
    mileSq = um.Unit('mi^2', _dim, 1609.344 ** 2)
    mileUSSq = um.Unit('miUS^2', _dim, 1609.34721869 ** 2)
    yardSq = um.Unit('yd^2', _dim, 0.9144 ** 2)

class Capacitance:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([-1,   -2,   4,   2,   0,   0,     0,    0])
    Farad = um.Unit('F', _dim, 1.0)
    milliFarad = um.Unit('mF', _dim, 0.001)
    microFarad = um.Unit('µF', _dim, 0.000001)
    pico = um.Unit('pF', _dim, 0.000000001)

class Charge:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   1,   1,   0,   0,     0,    0])
    Coulomb = um.Unit('C', _dim, 1.0)
    
class Conductance:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,   3,   2,   0,   0,     0,    0])
    Siemens = um.Unit('S', _dim, 1.0)

class Density:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,   -3,   0,   0,   0,   0,     0,    0])
    kg_m3 = um.Unit('kg/m^3', _dim, 1.0)
    g_cm3 = um.Unit('g/cm^3', _dim, 1000.0)
    lbm_ft3 = um.Unit('lbm/ft^3', _dim, 16.018463373960138)
    lbm_in3 = um.Unit('lbm/in^3', _dim, 27679.904710203125)

class Dimensionless:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    none = um.Unit('', _dim, 1.0)
    pct = um.Unit('%', _dim, 0.01)
    ppm = um.Unit('ppm', _dim, 0.000001)

class Energy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,   0,   0,   0,     0,    0])
    Btu = um.Unit('Btu', _dim, 1055.05585262)
    cal = um.Unit('cal', _dim, 4.1868)
    J = um.Unit('J', _dim, 1.0)
    kJ = um.Unit('kJ', _dim, 1000.0)   

class EquivalentDose:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Sievert = um.Unit('Sv', _dim, 1.0)

class Force:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    1,  -2,   0,   0,   0,     0,    0])
    N = um.Unit('N', _dim, 1.0)
    kN = um.Unit('kN', _dim, 1000.0)
    gf =  um.Unit('gf', _dim, 0.00980665) 
    kip = um.Unit('kip', _dim, 4448.22161526)
    pdl = um.Unit('pdl', _dim, 0.138254954376)
    lbf = um.Unit('lbf', _dim, 4.4482216152605)
    ozf = um.Unit('ozf', _dim, 0.278013850953781)

class Frequency:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Hz = um.Unit('Hz', _dim, 1.0)
    kHz = um.Unit('Hz', _dim, 1000.0)
    MHz = um.Unit('Hz', _dim, 1000000.0)
    GHz = um.Unit('Hz', _dim, 1000000000.0)

class Illuminance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,   0,   0,   0,   0,     1,    0])
    Lux = um.Unit('lx', _dim, 1.0)             

class Inductance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,   -2,   0,   0,     0,    0])
    Henry = um.Unit('H', _dim, 1.0)            
    milliHenry = um.Unit('mH', _dim, 0.001)            
    microHenry = um.Unit('mH', _dim, 0.000001)            
    picoHenry = um.Unit('pH', _dim, 0.000000001)            

class Length:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,   0,   0,   0,   0,     0,    0])
    m = um.Unit('m', _dim, 1.0)
    cm = um.Unit('cm', _dim, 0.01)
    mm = um.Unit('mm', _dim, 0.001)
    Km = um.Unit('Km', _dim, 1000.0)

    ft = um.Unit('ft', _dim, 0.3048)
    ftUS = um.Unit('ftUS', _dim,  0.304800609601)
    inch = um.Unit('in', _dim, 0.0254)
    mil = um.Unit('mil', _dim, 0.0000254)
    mile = um.Unit('mi', _dim, 1609.344)
    miUS = um.Unit('miUS', _dim, 1609.34721869)
    nmi = um.Unit('nmi', _dim, 1852.0)
    yd = um.Unit('yd', _dim, 0.9144)

class LuminousFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     1,    0])
    Lumen = um.Unit('lm', _dim, 1.0)             

class MagneticFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,  -1,   0,   0,     0,    0])
    Weber = um.Unit('Wb', _dim, 1.0)             

class MagneticFluxDensity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    0,  -2,  -1,   0,   0,     0,    0])
    Tesla = um.Unit('T', _dim, 1.0)

class Mass:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    0,   0,   0,   0,   0,     0,    0])
    Kg = um.Unit('Kg', _dim, 1.0)
    g = um.Unit('g', _dim, 0.001)
    mg = um.Unit('mg', _dim, 0.000001)
    oz = um.Unit('oz', _dim,0.028349523125)
    lbm = um.Unit('lbm', _dim, 0.45359237)
    slug = um.Unit('slug', _dim, 14.5939029372)
    ton = um.Unit('ton', _dim, 907.18474)
    tonUK = um.Unit('tonUK', _dim, 1016.0469088)

class Power:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,   0,   0,   0,     0,    0])
    hp = um.Unit('hp', _dim, 745.699871582)
    Watt = um.Unit('W', _dim, 1.0)
    mW = um.Unit('mW', _dim, 0.001)
    kW = um.Unit('kW', _dim, 1000.0)
    MW = um.Unit('kW', _dim, 1000000.0)
    GW = um.Unit('kW', _dim, 1000000000.0)

class Pressure:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,   -1,  -2,   0,   0,   0,     0,    0])
    atm = um.Unit('atm', _dim, 101325.0)
    bar = um.Unit('bar', _dim, 100000.0)
    Pa = um.Unit('Pa', _dim, 1.0)
    kPa = um.Unit('kPa', _dim, 1000.0)
    MPa = um.Unit('MPa', _dim, 1000000.0)
    inHg = um.Unit('inHg', _dim, 3386.38815789)
    inH2O = um.Unit('inH2O', _dim, 248.84)
    mmHg = um.Unit('mmHg', _dim, 133.322368421)
    mmH2O = um.Unit('mmH2O', _dim, 9.796850394)
    psi = um.Unit('psi', _dim, 6894.75729317)
    psia = um.Unit('psia', _dim, 6894.75729317)
    psig = um.Unit('psig', _dim, 6894.75729317, 101325.0)
 
class Resistance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,   -2,   0,   0,     0,    0])
    Ohm = um.Unit('Ω', _dim, 1.0)
    kOhm = um.Unit('kΩ', _dim, 1000.0)
    MOhm = um.Unit('MΩ', _dim, 1000000.0)
    mOhm = um.Unit('mΩ', _dim, 0.001)
    µOhm = um.Unit('µΩ', _dim, 0.000001)

class SpEnergy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Btu_lbm = um.Unit('Btu/lbm', _dim, 2326.0)
    cal_g = um.Unit('cal/g', _dim, 4186.8)
    J_g = um.Unit('J/g', _dim, 1000.0)
    kJ_kg = um.Unit('kJ/Kg', _dim, 1000.0)   

class SpHeatCap:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,  -1,   0,     0,    0])
    Btu_lbmF = um.Unit('Btu/lbm·°F', _dim, 2326.0)
    cal_gC = um.Unit('cal/g·°C', _dim, 4186.8)
    J_gK = um.Unit('J/g·°K', _dim, 1000.0)
    kJ_kgK = um.Unit('kJ/kg·°K', _dim, 1000.0)   

class SpVolume:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([-1,    3,   0,   0,   0,   0,     0,    0])
    m3_kg = um.Unit('m^3/kg', _dim, 1.0)
    cm3_g = um.Unit('cm^3/g', _dim, 0.001)
    ft3_lbm = um.Unit('ft^3/lbm', _dim, 1.0 / 16.0184633739601)
    in3_lbm = um.Unit('in^3/lbm', _dim, 1.0 / 27679.9047102031)

class Temperature:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   1,   0,     0,    0])
    degK = um.Unit('K', _dim, 1.0)
    degR = um.Unit('°R', _dim, 5.0 / 9.0)
    degC = um.Unit('°C', _dim, 1.0, 273.15)
    deltaC = um.Unit('▲°C', _dim, 1.0)
    degF = um.Unit('°F', _dim, 5.0 / 9.0, 255.37222222222223)
    deltaF = um.Unit('▲°F', _dim, 5.0 / 9.0)

class Time:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   1,   0,   0,   0,     0,    0])
    s = um.Unit('s', _dim, 1.0)
    min = um.Unit('min', _dim, 60.0)
    hr = um.Unit('h', _dim, 3600.0)
    d = um.Unit('d', _dim, 86400.0)
    yr = um.Unit('yr', _dim, 31536000.0)

class Velocity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,  -1,   0,   0,   0,     0,    0])
    knot = um.Unit('knot', _dim, 0.514444444444)
    kph = um.Unit('kph', _dim, 0.277777777778)
    mph = um.Unit('mph', _dim, 0.44704)

    fps = um.Unit('fps', _dim, 0.3048)
    fpm = um.Unit('fpm', _dim, 0.3048 / 60.0)
    mps = um.Unit('mps', _dim, 1.0)

class Viscosity:
   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimAbs = um.Dimension([1,   -1,  -1,   0,   0,   0,     0,    0])
    Poise = um.Unit('P', _dimAbs, 0.1)
    cP = um.Unit('cP', _dimAbs, 0.001)

   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimKin = um.Dimension([0,    2,  -1,   0,   0,   0,     0,    0])
    Stoke = um.Unit('St', _dimKin, 0.0001)
    cSt = um.Unit('cSt', _dimKin, 0.000001)

class Voltage:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,  -1,   0,   0,     0,    0])
    Volt = um.Unit('V', _dim, 1.0)
    kV = um.Unit('kV', _dim, 1000.0)
    mV = um.Unit('mV', _dim, 0.001)
    µV = um.Unit('µV', _dim, 0.000001)

class Volume:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    3,   0,   0,   0,   0,     0,    0])
    meterCu = um.Unit('m^3', _dim, 1.0)
    cc = um.Unit('cc', _dim, 0.000001)
    ydCu = um.Unit('ft^3', _dim, np.power(0.9144, 3))
    ftCu = um.Unit('ft^3', _dim, np.power(0.3048, 3))
    inCu = um.Unit('in^3', _dim, np.power(0.0254, 3))
    bbl = um.Unit('bbl', _dim, 0.158987294928)
    cup = um.Unit('cu', _dim, 2.365882365E-04)
    gal = um.Unit('gal', _dim, 0.003785411784)
    galCdn = um.Unit('galC', _dim, 0.00454609)
    galUK = um.Unit('galUK', _dim, 0.004546092)
    liter = um.Unit('l', _dim, 0.001)
    ml = um.Unit('ml', _dim, 0.000001)
    ozfl = um.Unit('m^3', _dim, 2.95735295625E-05)
    ozUK = um.Unit('ozUK', _dim, 0.000028413075)
    pt = um.Unit('pt', _dim, 0.000473176473)
    qt = um.Unit('qt', _dim, 0.000946352946)
    tbsp = um.Unit('tbsp', _dim, 1.47867647813E-05)
    tsp = um.Unit('tsp', _dim, 4.92892159375E-06)

class VolFlowRate:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    3,  -1,   0,   0,   0,     0,    0])
    m3_s = um.Unit('m^3/s', _dim, 1.0)
    gpm = um.Unit('gpm', _dim, 6.309019640e-5)
    gph = um.Unit('gph', _dim, 1.051503273333330e-6)
    ccm = um.Unit('ccm', _dim, 1.666666666666670e-8)
    lpm = um.Unit('ccm', _dim, 1.666666666666670e-5)
    ml_m = um.Unit('ml/min', _dim, 1.666666666666670e-8)
    cfm = um.Unit('cfm', _dim, 4.719474432000000e-4)
    cfh = um.Unit('cfh', _dim, 7.865790720000000e-6)

class Work:
    Btu = Energy.Btu
    cal = Energy.cal
    J = Energy.J
    kJ = Energy.kJ
