import numpy as np
import sys
eng_path = './Engineering'
if not eng_path in sys.path:
    sys.path.insert(0, eng_path)
from unit_of_measure import *

class Acceleration:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    1,  -2,   0,   0,   0,     0,    0])
    g = Unit.Create('g', _dim, 9.80665)
    Gal = Unit.Create('Gal', _dim, 1.0)

class AbsorbedDose:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Gray = Unit.Create('Gy', _dim, 1.0)

class Activity:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Becquerel = Unit.Create('Bq', _dim, 1.0)

class Amount:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   0,   0,   0,   1,     0,    0])
    Mol = Unit.Create('Mol', _dim, 1.0)
    kMol = Unit('kMol', 1000.0 * Mol)

class Angle:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    Radian = Unit.Create('rad', _dim, 1.0)
    rev = Unit('r', Radian * 2.0 * np.pi)
    deg = Unit('°', rev / 360.0)
    grad = Unit('grad', rev / 400.0)
    gon = Unit('gon', 1.0 * grad)
    mil = Unit('mil', rev / 6400.0)
    min = Unit("'", deg / 60.0)
    sec = Unit('"', min / 60.0)
    Steradian = Unit('sr', 1.0 * Radian)
    

class Area:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,   0,   0,   0,   0,     0,    0])
    meterSq = Unit.Create('m^2', _dim, 1.0)
    mmSq = Unit('mm^2', 0.001 ** 2 * meterSq)
    acre = Unit('acre', 4046.87260987 * meterSq)
    are = Unit('a', 100.0 * meterSq)
    barn = Unit('b', 1.0E-28 * meterSq)
    cmil = Unit('cmil', 5.06707479097498e-10 * meterSq)
    hectare = Unit('ha', 10000.0 * meterSq)
    ftSq = Unit('ft^2', 0.3048 ** 2 * meterSq)
    inSq = Unit('in^2', 0.0254 ** 2 * meterSq)
    mileSq = Unit('mi^2', 1609.344 ** 2 * meterSq)
    mileUSSq = Unit('miUS^2', 1609.34721869 ** 2 * meterSq)
    yardSq = Unit('yd^2', 0.9144 ** 2 * meterSq)

class Capacitance:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([-1,   -2,   4,   2,   0,   0,     0,    0])
    Farad = Unit.Create('F', _dim, 1.0)
    milliFarad = Unit('mF', 0.001 * Farad)
    microFarad = Unit('µF', 0.000001 * Farad)
    pico = Unit('pF', 0.000000001 * Farad)

class Charge:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   1,   1,   0,   0,     0,    0])
    Coulomb = Unit.Create('C', _dim, 1.0)
    
class Conductance:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,   3,   2,   0,   0,     0,    0])
    Siemens = Unit.Create('S', _dim, 1.0)

class Density:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,   -3,   0,   0,   0,   0,     0,    0])
    kg_m3 = Unit.Create('kg/m^3', _dim, 1.0)
    g_cm3 = Unit('g/cm^3', 1000.0 * kg_m3)
    lbm_ft3 = Unit('lbm/ft^3', 16.018463373960138 * kg_m3)
    lbm_in3 = Unit('lbm/in^3', 27679.904710203125 * kg_m3)

class Dimensionless:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    none = Unit.Create('', _dim, 1.0)
    pct = Unit('%', none / 100.0)
    ppm = Unit('ppm', none / 1.0e6)

class Energy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -2,   0,   0,   0,     0,    0])
    J = Unit.Create('J', _dim, 1.0)
    kJ = Unit('kJ', 1000.0 * J)   
    Btu = Unit('Btu', 1055.05585262 * J)
    cal = Unit('cal', 4.184 * J)  # based on the thermochemical calorie, not the International Table calorie

class EquivalentDose:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Sievert = Unit.Create('Sv', _dim, 1.0)

class Force:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    1,  -2,   0,   0,   0,     0,    0])
    N = Unit.Create('N', _dim, 1.0)
    kN = Unit('kN', 1000.0 * N)
    gf =  Unit('gf', 0.00980665 * N) 
    kip = Unit('kip', 4448.22161526 * N)
    pdl = Unit('pdl', 0.138254954376 * N)
    lbf = Unit('lbf', 4.4482216152605 * N)
    ozf = Unit('ozf', 0.278013850953781 * N)

class Frequency:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Hz = Unit.Create('Hz', _dim, 1.0)
    kHz = Unit('kHz', 1000.0 * Hz)
    MHz = Unit('MHz', 1.0e6 * Hz)
    GHz = Unit('GHz', 1.0e9 * Hz)

class Illuminance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,   0,   0,   0,   0,     1,    0])
    Lux = Unit.Create('lx', _dim, 1.0)             

class Inductance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -2,   -2,   0,   0,     0,    0])
    Henry = Unit.Create('H', _dim, 1.0)            
    milliHenry = Unit('mH', Henry / 1000.0)            
    microHenry = Unit('mH', Henry / 1.0e6)            
    picoHenry = Unit('pH', Henry / 1.0e9)            

class Length:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    1,   0,   0,   0,   0,     0,    0])
    m = Unit.Create('m', _dim, 1.0)
    cm = Unit('cm', 0.01 * m)
    mm = Unit('mm', 0.001 * m)
    micron = Unit('um', m / 1.0e6)
    Km = Unit('Km', 1000.0 * m)

    ft = Unit('ft', 0.3048 * m)
    ftUS = Unit('ftUS', 0.304800609601 * m)
    inch = Unit('in', ft / 12.0)
    mil = Unit('mil', 0.001 * inch)
    mile = Unit('mi', 5280.0 * ft)
    miUS = Unit('miUS', 1609.34721869 * m)
    nmi = Unit('nmi', 1852.0 * m)
    yd = Unit('yd', 3.0 * ft)

class LuminousFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   0,   0,   0,   0,     1,    0])
    Lumen = Unit.Create('lm', _dim, 1.0)             

class MagneticFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -2,  -1,   0,   0,     0,    0])
    Weber = Unit.Create('Wb', _dim, 1.0)             

class MagneticFluxDensity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    0,  -2,  -1,   0,   0,     0,    0])
    Tesla = Unit.Create('T', _dim, 1.0)

class Mass:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    0,   0,   0,   0,   0,     0,    0])
    Kg = Unit.Create('Kg', _dim, 1.0)
    g = Unit('g', 0.001 * Kg)
    mg = Unit('mg', Kg / 1.0e6)
    oz = Unit('oz', 0.028349523125 * Kg)
    lbm = Unit('lbm', 0.45359237 * Kg)
    slug = Unit('slug', 14.5939029372 * Kg)
    ton = Unit('ton', 907.18474 * Kg)
    tonUK = Unit('tonUK', 1016.0469088 * Kg)

class Power:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -3,   0,   0,   0,     0,    0])
    Watt = Unit.Create('W', _dim, 1.0)
    hp = Unit('hp', 745.699871582 * Watt)
    mW = Unit('mW', 0.001 * Watt)
    kW = Unit('kW', 1000.0 * Watt)
    MW = Unit('kW', 1.0e6 * Watt)
    GW = Unit('kW', 1.0e9 * Watt)

class Pressure:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,   -1,  -2,   0,   0,   0,     0,    0])
    Pa = Unit.Create('Pa', _dim, 1.0)
    atm = Unit('atm', 101325.0 * Pa)
    bar = Unit('bar', 100000.0 * Pa)
    mbar = Unit('mbar', 0.001 * bar)
    kPa = Unit('kPa', 1000.0 * Pa)
    MPa = Unit('MPa', 1000.0 * kPa)
    inHg = Unit('inHg', 3386.38815789 * Pa)
    inH2O = Unit('inH2O', 248.84 * Pa)
    mmHg = Unit('mmHg', 133.322368421 * Pa)
    mmH2O = Unit('mmH2O', 9.796850394 * Pa)
    psi = Unit('psi', 6894.75729317 * Pa)
    psia = Unit('psia', 1.0 * psi)
    psig = Unit('psig', 6894.75729317 * Pa, 1.0 * atm)
    Torr = Unit('torr', 1.0 * mmHg)
 
class Resistance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -3,   -2,   0,   0,     0,    0])
    Ohm = Unit.Create('Ω', _dim, 1.0)
    kOhm = Unit('kΩ', 1000.0 * Ohm)
    MOhm = Unit('MΩ', 1.0e6 * Ohm)
    mOhm = Unit('mΩ', 0.001 * Ohm)
    µOhm = Unit('µΩ', Ohm / 1.0e6)

class SpEnergy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    J_g = Unit.Create('J/g', _dim, 1000.0)
    kJ_kg = Unit('kJ/Kg', 1.0 * J_g)   
    Btu_lbm = Unit('Btu/lbm', 2.324444 * J_g)  # based on the thermochemical calorie, not the International Table calorie
    cal_g = Unit('cal/g', 4.184 * J_g)         # based on the thermochemical calorie, not the International Table calorie

class SpHeatCap:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    2,  -2,   0,  -1,   0,     0,    0])
    J_gK = Unit.Create('J/g·°K', _dim, 1000.0)
    kJ_kgK = Unit('kJ/kg·°K', 1.0 * J_gK)   
    Btu_lbmF = Unit('Btu/lbm·°F', 4.184 * J_gK)  # based on the thermochemical calorie, not the International Table calorie
    cal_gC = Unit('cal/g·°C', 4.184 * J_gK)      # based on the thermochemical calorie, not the International Table calorie

class SpVolume:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([-1,    3,   0,   0,   0,   0,     0,    0])
    m3_kg = Unit.Create('m^3/kg', _dim, 1.0)
    cm3_g = Unit('cm^3/g', 0.001 * m3_kg)
    ft3_lbm = Unit('ft^3/lbm', m3_kg / 16.0184633739601)
    in3_lbm = Unit('in^3/lbm', m3_kg / 27679.9047102031)

class Stress:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,   -1,  -2,   0,   0,   0,     0,    0])
    Pa = Unit.Create('Pa', _dim, 1.0)
    kPa = Unit('kPa', 1000.0 * Pa)
    MPa = Unit('MPa', 1.0e6 * Pa)
    psi = Unit('psi', 6894.75729317 * Pa)
    ksi = Unit('ksi', 1000.0 * psi)
    msi = Unit('msi', 1.0e6 * psi)

class Temperature:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   0,   0,   1,   0,     0,    0])
    degK = Unit.Create('K', _dim, 1.0)
    degR = Unit('°R', 5.0 / 9.0 * degK)
    degC = Unit('°C', 1.0 * degK, 273.15 * degK)
    deltaC = Unit('▲°C', 1.0 * degK)
    degF = Unit('°F', 1.0 * degR, 459.67 * degR)
    deltaF = Unit('▲°F', 1.0 * degR)

class Time:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    0,   1,   0,   0,   0,     0,    0])
    s = Unit.Create('s', _dim, 1.0)
    min = Unit('min', 60.0 * s)
    hr = Unit('h', 60.0 * min)
    d = Unit('d', 24.0 * hr)
    yr = Unit('yr', 365.0 * d)

class Velocity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    1,  -1,   0,   0,   0,     0,    0])
    mps = Unit.Create('mps', _dim, 1.0)
    mph = Unit('mph', mps / 3600.0)
    kph = Unit('kph', 1000.0 * mph)

    fps = Unit('fps', 0.3048 * mps)
    fpm = Unit('fpm', fps / 60.0)
    knot = Unit('knot', 0.514444444444 * mps)

class Viscosity:
   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimAbs = Dimension([1,   -1,  -1,   0,   0,   0,     0,    0])
    Pa_s = Unit.Create('Pa·s', _dimAbs, 1.0)
    Poise = Unit('P', 0.01 * Pa_s)
    cP = Unit('cP', 0.01 * Poise)

   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimKin = Dimension([0,    2,  -1,   0,   0,   0,     0,    0])
    m2ps = Unit.Create('m^2/s', _dimKin, 1.0)
    Stoke = Unit('St', m2ps / 1.0e4)
    cSt = Unit('cSt', 0.01 * Stoke)

class Voltage:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([1,    2,  -3,  -1,   0,   0,     0,    0])
    Volt = Unit.Create('V', _dim, 1.0)
    kV = Unit('kV', 1000.0 * Volt)
    MV = Unit('MV', 1.0e6 * Volt)
    mV = Unit('mV', 0.001 * Volt)
    µV = Unit('µV', Volt / 1.0e6)

class Volume:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    3,   0,   0,   0,   0,     0,    0])
    meterCu = Unit.Create('m^3', _dim, 1.0)
    liter = Unit('l', 0.001 * meterCu)
    ml = Unit('ml', liter / 1000.0)
    cc = Unit('cc', 1.0 * ml)

    inCu = Unit('in^3', meterCu * 0.0254 ** 3)
    ftCu = Unit('ft^3', inCu / 12.0 ** 3)
    ydCu = Unit('ft^3', ftCu / 3.0 ** 3)
    bbl = Unit('bbl', 0.158987294928 * meterCu)
    cup = Unit('cu', 2.365882365E-04 * meterCu)
    gal = Unit('gal', 0.003785411784 * meterCu)
    galCdn = Unit('galC', 0.00454609 * meterCu)
    galUK = Unit('galUK', 0.004546092 * meterCu)
    ozfl = Unit('m^3', 2.95735295625E-05 * meterCu)
    ozUK = Unit('ozUK', 0.000028413075 * meterCu)
    pt = Unit('pt', 0.000473176473 * meterCu)
    qt = Unit('qt', 0.000946352946 * meterCu)
    tbsp = Unit('tbsp', 1.47867647813E-05 * meterCu)
    tsp = Unit('tsp', 4.92892159375E-06 * meterCu)

class VolFlowRate:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = Dimension([0,    3,  -1,   0,   0,   0,     0,    0])
    m3_s = Unit.Create('m^3/s', _dim, 1.0)
    lpm = Unit('ccm', 1.0 * Volume.liter / Time.min)

    gpm = Unit('gpm', 1.0 * Volume.gal / Time.min)
    gph = Unit('gph', 1.0 * Volume.gal / Time.hr)
    ccm = Unit('ccm', 1.0 * Volume.cc / Time.min)
    ml_m = Unit('ml/min', 1.0 * Volume.ml / Time.min)
    cfm = Unit('cfm', 1.0 * Volume.ftCu / Time.min)
    cfh = Unit('cfh', Volume.ftCu / Time.hr)

class Work:
    Btu = Energy.Btu
    cal = Energy.cal
    J = Energy.J
    kJ = Energy.kJ


if __name__ == '__main__':
    # Dimension handles exponents
    # Quantity contains float and Dimension
    # Unit is (derived from) Quantity with symbol string and offset (pressure and temperature)
    # Quantity q1 = float * Unit
    # sq1 = q1.Format(Unit, fmt) returns string of Value formatted 
    # Unit u1 = value, offset, dimension, symbol
    # su1 = u1.Format(Unit, fmt) returns string of Value formatted

    def main():
        #ang1 = 360.0 * Angle.deg
        #print(ang1.Format(Angle.grad, '0.2f'))
        #print(ang1.Format(Angle.rev, '0.2f'))

        #rho = 1000.0 * Density.kg_m3
        #print(rho.Format(Density.kg_m3, '0.2f'))
        #print(rho.Format(Density.g_cm3, '0.2f'))
        #print(rho.Format(Density.lbm_in3, '0.4f'))
        #print(rho.Format(Density.lbm_ft3, '0.4f'))

        cp = 1000.0 * SpHeatCap.kJ_kgK
        print(cp.Format(SpHeatCap.kJ_kgK, '0.6f'))
        print(cp.Format(SpHeatCap.J_gK, '0.6f'))
        print(cp.Format(SpHeatCap.Btu_lbmF, '0.6f'))
        print(cp.Format(SpHeatCap.cal_gC, '0.6f'))

        um    = Length.m
        ucm   = Length.cm
        umm   = Length.mm
        uKm   = Length.Km
        uft   = Length.ft
        uinch = Length.inch
        uyd   = Length.yd

        d1 = 2.0 * uyd
        d9 = 3.0 * d1
        d2 = 36.0 * uinch
        d3 = d1 + d2
        a1 = d1.squared()
        v1 = d1 * d2 * d3
        
        print(f'd3 = {d3.Format(uinch, "0.2f")}')
        print(f'd3 = {d3.Format(uft, "0.3f")}')
        print(f'd3 = {d3.Format(uyd, "0.4f")}')

        q1 = 3.0 / squared()
        print(q1)

    main()