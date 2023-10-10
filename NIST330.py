import numpy as np
import unit_of_measure as um

class Acceleration:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,  -2,   0,   0,   0,     0,    0])
    g = um.Unit.Create('g', _dim, 9.80665)
    Gal = um.Unit.Create('Gal', _dim, 1.0)

class AbsorbedDose:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Gray = um.Unit.Create('Gy', _dim, 1.0)

class Activity:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Becquerel = um.Unit.Create('Bq', _dim, 1.0)

class Amount:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   1,     0,    0])
    Mol = um.Unit.Create('Mol', _dim, 1.0)
    kMol = um.Unit('kMol', 1000.0 * Mol)

class Angle:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    Radian = um.Unit.Create('rad', _dim, 1.0)
    rev = um.Unit('r', Radian * 2.0 * np.pi)
    deg = um.Unit('°', rev / 360.0)
    grad = um.Unit('grad', rev / 400.0)
    gon = um.Unit('gon', 1.0 * grad)
    mil = um.Unit('mil', rev / 6400.0)
    min = um.Unit("'", deg / 60.0)
    sec = um.Unit('"', min / 60.0)
    Steradian = um.Unit('sr', 1.0 * Radian)
    

class Area:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,   0,   0,   0,   0,     0,    0])
    meterSq = um.Unit.Create('m^2', _dim, 1.0)
    mmSq = um.Unit('mm^2', 0.001 ** 2 * meterSq)
    acre = um.Unit('acre', 4046.87260987 * meterSq)
    are = um.Unit('a', 100.0 * meterSq)
    barn = um.Unit('b', 1.0E-28 * meterSq)
    cmil = um.Unit('cmil', 5.06707479097498e-10 * meterSq)
    hectare = um.Unit('ha', 10000.0 * meterSq)
    ftSq = um.Unit('ft^2', 0.3048 ** 2 * meterSq)
    inSq = um.Unit('in^2', 0.0254 ** 2 * meterSq)
    mileSq = um.Unit('mi^2', 1609.344 ** 2 * meterSq)
    mileUSSq = um.Unit('miUS^2', 1609.34721869 ** 2 * meterSq)
    yardSq = um.Unit('yd^2', 0.9144 ** 2 * meterSq)

class Capacitance:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([-1,   -2,   4,   2,   0,   0,     0,    0])
    Farad = um.Unit.Create('F', _dim, 1.0)
    milliFarad = um.Unit('mF', 0.001 * Farad)
    microFarad = um.Unit('µF', 0.000001 * Farad)
    pico = um.Unit('pF', 0.000000001 * Farad)

class Charge:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   1,   1,   0,   0,     0,    0])
    Coulomb = um.Unit.Create('C', _dim, 1.0)
    
class Conductance:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,   3,   2,   0,   0,     0,    0])
    Siemens = um.Unit.Create('S', _dim, 1.0)

class Density:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,   -3,   0,   0,   0,   0,     0,    0])
    kg_m3 = um.Unit.Create('kg/m^3', _dim, 1.0)
    g_cm3 = um.Unit('g/cm^3', 1000.0 * kg_m3)
    lbm_ft3 = um.Unit('lbm/ft^3', 16.018463373960138 * kg_m3)
    lbm_in3 = um.Unit('lbm/in^3', 27679.904710203125 * kg_m3)

class Dimensionless:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     0,    0])
    none = um.Unit.Create('', _dim, 1.0)
    pct = um.Unit('%', none / 100.0)
    ppm = um.Unit('ppm', none / 1.0e6)

class Energy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,   0,   0,   0,     0,    0])
    J = um.Unit.Create('J', _dim, 1.0)
    kJ = um.Unit('kJ', 1000.0 * J)   
    Btu = um.Unit('Btu', 1055.05585262 * J)
    cal = um.Unit('cal', 4.184 * J)  # based on the thermochemical calorie, not the International Table calorie

class EquivalentDose:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    Sievert = um.Unit.Create('Sv', _dim, 1.0)

class Force:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    1,  -2,   0,   0,   0,     0,    0])
    N = um.Unit.Create('N', _dim, 1.0)
    kN = um.Unit('kN', 1000.0 * N)
    gf =  um.Unit('gf', 0.00980665 * N) 
    kip = um.Unit('kip', 4448.22161526 * N)
    pdl = um.Unit('pdl', 0.138254954376 * N)
    lbf = um.Unit('lbf', 4.4482216152605 * N)
    ozf = um.Unit('ozf', 0.278013850953781 * N)

class Frequency:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,  -1,   0,   0,   0,     0,    0])
    Hz = um.Unit.Create('Hz', _dim, 1.0)
    kHz = um.Unit('kHz', 1000.0 * Hz)
    MHz = um.Unit('MHz', 1.0e6 * Hz)
    GHz = um.Unit('GHz', 1.0e9 * Hz)

class Illuminance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,   0,   0,   0,   0,     1,    0])
    Lux = um.Unit.Create('lx', _dim, 1.0)             

class Inductance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,   -2,   0,   0,     0,    0])
    Henry = um.Unit.Create('H', _dim, 1.0)            
    milliHenry = um.Unit('mH', Henry / 1000.0)            
    microHenry = um.Unit('mH', Henry / 1.0e6)            
    picoHenry = um.Unit('pH', Henry / 1.0e9)            

class Length:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,   0,   0,   0,   0,     0,    0])
    m = um.Unit.Create('m', _dim, 1.0)
    cm = um.Unit('cm', 0.01 * m)
    mm = um.Unit('mm', 0.001 * m)
    micron = um.Unit('um', m / 1.0e6)
    Km = um.Unit('Km', 1000.0 * m)

    ft = um.Unit('ft', 0.3048 * m)
    ftUS = um.Unit('ftUS', 0.304800609601 * m)
    inch = um.Unit('in', ft / 12.0)
    mil = um.Unit('mil', 0.001 * inch)
    mile = um.Unit('mi', 5280.0 * ft)
    miUS = um.Unit('miUS', 1609.34721869 * m)
    nmi = um.Unit('nmi', 1852.0 * m)
    yd = um.Unit('yd', 3.0 * ft)

class LuminousFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   0,   0,     1,    0])
    Lumen = um.Unit.Create('lm', _dim, 1.0)             

class MagneticFlux:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -2,  -1,   0,   0,     0,    0])
    Weber = um.Unit.Create('Wb', _dim, 1.0)             

class MagneticFluxDensity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    0,  -2,  -1,   0,   0,     0,    0])
    Tesla = um.Unit.Create('T', _dim, 1.0)

class Mass:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    0,   0,   0,   0,   0,     0,    0])
    Kg = um.Unit.Create('Kg', _dim, 1.0)
    g = um.Unit('g', 0.001 * Kg)
    mg = um.Unit('mg', Kg / 1.0e6)
    oz = um.Unit('oz', 0.028349523125 * Kg)
    lbm = um.Unit('lbm', 0.45359237 * Kg)
    slug = um.Unit('slug', 14.5939029372 * Kg)
    ton = um.Unit('ton', 907.18474 * Kg)
    tonUK = um.Unit('tonUK', 1016.0469088 * Kg)

class Power:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,   0,   0,   0,     0,    0])
    Watt = um.Unit.Create('W', _dim, 1.0)
    hp = um.Unit('hp', 745.699871582 * Watt)
    mW = um.Unit('mW', 0.001 * Watt)
    kW = um.Unit('kW', 1000.0 * Watt)
    MW = um.Unit('kW', 1.0e6 * Watt)
    GW = um.Unit('kW', 1.0e9 * Watt)

class Pressure:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,   -1,  -2,   0,   0,   0,     0,    0])
    Pa = um.Unit.Create('Pa', _dim, 1.0)
    atm = um.Unit('atm', 101325.0 * Pa)
    bar = um.Unit('bar', 100000.0 * Pa)
    mbar = um.Unit('mbar', 0.001 * bar)
    kPa = um.Unit('kPa', 1000.0 * Pa)
    MPa = um.Unit('MPa', 1.0e6 * kPa)
    inHg = um.Unit('inHg', 3386.38815789 * Pa)
    inH2O = um.Unit('inH2O', 248.84 * Pa)
    mmHg = um.Unit('mmHg', 133.322368421 * Pa)
    mmH2O = um.Unit('mmH2O', 9.796850394 * Pa)
    psi = um.Unit('psi', 6894.75729317 * Pa)
    psia = um.Unit('psia', 1.0 * psi)
    psig = um.Unit('psig', 6894.75729317 * Pa, 1.0 * atm)
    Torr = um.Unit('torr', 1.0 * mmHg)
 
class Resistance:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,   -2,   0,   0,     0,    0])
    Ohm = um.Unit.Create('Ω', _dim, 1.0)
    kOhm = um.Unit('kΩ', 1000.0 * Ohm)
    MOhm = um.Unit('MΩ', 1.0e6 * Ohm)
    mOhm = um.Unit('mΩ', 0.001 * Ohm)
    µOhm = um.Unit('µΩ', Ohm / 1.0e6)

class SpEnergy:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,   0,   0,     0,    0])
    J_g = um.Unit.Create('J/g', _dim, 1000.0)
    kJ_kg = um.Unit('kJ/Kg', 1.0 * J_g)   
    Btu_lbm = um.Unit('Btu/lbm', 2.324444 * J_g)  # based on the thermochemical calorie, not the International Table calorie
    cal_g = um.Unit('cal/g', 4.184 * J_g)         # based on the thermochemical calorie, not the International Table calorie

class SpHeatCap:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    2,  -2,   0,  -1,   0,     0,    0])
    J_gK = um.Unit.Create('J/g·°K', _dim, 1000.0)
    kJ_kgK = um.Unit('kJ/kg·°K', 1.0 * J_gK)   
    Btu_lbmF = um.Unit('Btu/lbm·°F', 4.184 * J_gK)  # based on the thermochemical calorie, not the International Table calorie
    cal_gC = um.Unit('cal/g·°C', 4.184 * J_gK)      # based on the thermochemical calorie, not the International Table calorie

class SpVolume:
    #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([-1,    3,   0,   0,   0,   0,     0,    0])
    m3_kg = um.Unit.Create('m^3/kg', _dim, 1.0)
    cm3_g = um.Unit('cm^3/g', 0.001 * m3_kg)
    ft3_lbm = um.Unit('ft^3/lbm', m3_kg / 16.0184633739601)
    in3_lbm = um.Unit('in^3/lbm', m3_kg / 27679.9047102031)

class Stress:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,   -1,  -2,   0,   0,   0,     0,    0])
    Pa = um.Unit.Create('Pa', _dim, 1.0)
    kPa = um.Unit('kPa', 1000.0 * Pa)
    MPa = um.Unit('MPa', 1.0e6 * Pa)
    psi = um.Unit('psi', 6894.75729317 * Pa)
    ksi = um.Unit('ksi', 1000.0 * psi)
    msi = um.Unit('msi', 1.0e6 * psi)

class Temperature:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   0,   0,   1,   0,     0,    0])
    degK = um.Unit.Create('K', _dim, 1.0)
    degR = um.Unit('°R', 5.0 / 9.0 * degK)
    degC = um.Unit('°C', 1.0 * degK, 273.15 * degK)
    deltaC = um.Unit('▲°C', 1.0 * degK)
    degF = um.Unit('°F', 1.0 * degR, 459.67 * degR)
    deltaF = um.Unit('▲°F', 1.0 * degR)

class Time:
    #                   'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    0,   1,   0,   0,   0,     0,    0])
    s = um.Unit.Create('s', _dim, 1.0)
    min = um.Unit('min', 60.0 * s)
    hr = um.Unit('h', 60.0 * min)
    d = um.Unit('d', 24.0 * hr)
    yr = um.Unit('yr', 365.0 * d)

class Velocity:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    1,  -1,   0,   0,   0,     0,    0])
    mps = um.Unit.Create('mps', _dim, 1.0)
    mph = um.Unit('mph', mps / 3600.0)
    kph = um.Unit('kph', 1000.0 * mph)

    fps = um.Unit('fps', 0.3048 * mps)
    fpm = um.Unit('fpm', fps / 60.0)
    knot = um.Unit('knot', 0.514444444444 * mps)

class Viscosity:
   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimAbs = um.Dimension([1,   -1,  -1,   0,   0,   0,     0,    0])
    Pa_s = um.Unit.Create('Pa·s', _dimAbs, 1.0)
    Poise = um.Unit('P', 0.01 * Pa_s)
    cP = um.Unit('cP', 0.01 * Poise)

   #                       'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dimKin = um.Dimension([0,    2,  -1,   0,   0,   0,     0,    0])
    m2ps = um.Unit.Create('m^2/s', _dimKin, 1.0)
    Stoke = um.Unit('St', m2ps / 1.0e4)
    cSt = um.Unit('cSt', 0.01 * Stoke)

class Voltage:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([1,    2,  -3,  -1,   0,   0,     0,    0])
    Volt = um.Unit.Create('V', _dim, 1.0)
    kV = um.Unit('kV', 1000.0 * Volt)
    MV = um.Unit('MV', 1.0e6 * Volt)
    mV = um.Unit('mV', 0.001 * Volt)
    µV = um.Unit('µV', Volt / 1.0e6)

class Volume:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    3,   0,   0,   0,   0,     0,    0])
    meterCu = um.Unit.Create('m^3', _dim, 1.0)
    liter = um.Unit('l', 0.001 * meterCu)
    ml = um.Unit('ml', liter / 1000.0)
    cc = um.Unit('cc', 1.0 * ml)

    inCu = um.Unit('in^3', meterCu * 0.0254 ** 3)
    ftCu = um.Unit('ft^3', inCu / 12.0 ** 3)
    ydCu = um.Unit('ft^3', ftCu / 3.0 ** 3)
    bbl = um.Unit('bbl', 0.158987294928 * meterCu)
    cup = um.Unit('cu', 2.365882365E-04 * meterCu)
    gal = um.Unit('gal', 0.003785411784 * meterCu)
    galCdn = um.Unit('galC', 0.00454609 * meterCu)
    galUK = um.Unit('galUK', 0.004546092 * meterCu)
    ozfl = um.Unit('m^3', 2.95735295625E-05 * meterCu)
    ozUK = um.Unit('ozUK', 0.000028413075 * meterCu)
    pt = um.Unit('pt', 0.000473176473 * meterCu)
    qt = um.Unit('qt', 0.000946352946 * meterCu)
    tbsp = um.Unit('tbsp', 1.47867647813E-05 * meterCu)
    tsp = um.Unit('tsp', 4.92892159375E-06 * meterCu)

class VolFlowRate:
   #                    'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    _dim = um.Dimension([0,    3,  -1,   0,   0,   0,     0,    0])
    m3_s = um.Unit.Create('m^3/s', _dim, 1.0)
    lpm = um.Unit('ccm', 1.0 * Volume.liter / Time.min)

    gpm = um.Unit('gpm', 1.0 * Volume.gal / Time.min)
    gph = um.Unit('gph', 1.0 * Volume.gal / Time.hr)
    ccm = um.Unit('ccm', 1.0 * Volume.cc / Time.min)
    ml_m = um.Unit('ml/min', 1.0 * Volume.ml / Time.min)
    cfm = um.Unit('cfm', 1.0 * Volume.ftCu / Time.min)
    cfh = um.Unit('cfh', Volume.ftCu / Time.hr)

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

        q1 = 3.0 / um.squared()
        print(q1)

    main()