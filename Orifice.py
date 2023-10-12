import numpy as np
import math
from Engineering import unit_of_measure as um
from Engineering import NIST330 as un
from Engineering import Water as h2o

upph = um.Unit('lbm/hr', 1.0 * un.Mass.lbm / un.Time.hr)

def OrificeSteamFlow(dia, cd, p1, p2):
    water = h2o.WaterIAPWS97()
    fp = water.SetSaturation(h2o.SatType.SatPress).SetQuality(1.0).SetCond(press=p1).Eval()
    rho = fp.SpVol.power(-1).Value(un.Density.lbm_ft3)
    gamma = (fp.SpHeatCp / fp.SpHeatCv).Value(un.Dimensionless.none) / 1.4
    xT = 0.72
    c0 = 63.3
    c1 = 0.66
    c2 = 0.183

    _dia = dia.Value(un.Length.inch)
    _p1 = p1.Value(un.Pressure.psia)
    _p2 = p2.Value(un.Pressure.psia)

    if (_p1 < _p2):
        raise Exception('p1 must be greater than p2')

    _px = (_p1 - _p2) / _p1

    critical = True
    if (_px < gamma * xT):
        critical = False

    mdot = 0.0

    if (critical):
        mdot = c0 * c1 * cd * ((_dia / c2) ** 2.0) * np.sqrt(gamma * xT * _p1 * rho)
    else:
        mdot = c0 * cd * ((_dia / c2) ** 2.0) * (1.0 - _px / (3.0 * gamma * xT)) * np.sqrt((_p1 - _p2) * rho)

    return mdot * upph

def OrificeDiaSteam(mdot, cd, p1, p2):
    dOne = 1.000 * un.Length.inch

    mOne = OrificeSteamFlow(dOne, cd, p1, p2)
    dia = dOne * (mdot / mOne).sqrt()

    return dia

def OrificeWaterFlow(dia, cd, p1, p2, t1):
    water = h2o.WaterIAPWS97()
    fp = water.SetSaturation(h2o.SatType.SatTemp).SetQuality(0.0).SetCond(temp=t1).Eval()
    _pv = fp.Press.Value(un.Pressure.psia)
    fp = water.SetCond(press = p1, temp=t1).Eval()
    _rho = fp.SpVol.power(-1).Value(un.Density.lbm_ft3)
    _rho_std = 62.366 # un.Density.lbm_ft3
    _sg = _rho / _rho_std
    _pcrit = 3200 # un.Pressure.psia
    _ff = 0.96 - 0.28 * math.sqrt(_pv / _pcrit)
    _fl = 0.9

    _p1 = p1.Value(un.Pressure.psia)
    _p2 = p2.Value(un.Pressure.psia)
 
    if (_p1 < _p2):
        raise Exception('p1 must be greater than p2')

    _dp = _p1 - _p2
    _dp_lim = (_fl ** 2.0) * (_p1 - _ff * _pv)
 
    _dia = dia.Value(un.Length.inch)
    _gpm = cd.Value(un.Dimensionless.none) * (_dia / 0.183) ** 2.0 # common portion
    if (_dp < _dp_lim):
        _gpm *= math.sqrt(_dp / _sg)
    else:
        _gpm *= _fl * math.sqrt((_p1 - _ff * _pv) / _sg) 

    return _gpm * un.VolFlowRate.gpm

def EstimateCv(flowArea, cd):
    # calculate the orifice diameter that has the given flow area
    d_orif_inch = math.sqrt(4.0 / math.pi * flowArea.Value(un.Area.inSq))

    Cv = cd * 29.839 * d_orif_inch ** 2

    return Cv

def QLiquid(Cv, sg, p1, p2):
    # calculate the volumetric flow rate
    _p1 = p1.Value(un.Pressure.psia)
    _p2 = p2.Value(un.Pressure.psia)
    _dp = _p1 - _p2

    Q = Cv * math.sqrt(_dp / sg) * un.VolFlowRate.gpm

    return Q

def SteamFlowCv(cv, p1, p2):
    water = h2o.WaterIAPWS97()
    fp = water.SetSaturation(h2o.SatType.SatPress).SetQuality(1.0).SetCond(press=p1).Eval()
    rho = fp.SpVol.power(-1).Value(un.Density.lbm_ft3)
    gamma = (fp.SpHeatCp / fp.SpHeatCv).Value(un.Dimensionless.none) / 1.4
    xT = 0.72
    c0 = 63.3
    c1 = 0.66

    _p1 = p1.Value(un.Pressure.psia)
    _p2 = p2.Value(un.Pressure.psia)

    if (_p1 < _p2):
        raise Exception('p1 must be greater than p2')

    _px = (_p1 - _p2) / _p1

    critical = True
    if (_px < gamma * xT):
        critical = False

    mdot = 0.0

    if (critical):
        mdot = c0 * c1 * cv * np.sqrt(gamma * xT * _p1 * rho)
    else:
        mdot = c0 * cv  * (1.0 - _px / (3.0 * gamma * xT)) * np.sqrt((_p1 - _p2) * rho)

    return mdot * upph

def CvSteamFlow(mdot, p1, p2):
    water = h2o.WaterIAPWS97()
    fp = water.SetSaturation(h2o.SatType.SatPress).SetQuality(1.0).SetCond(press=p1).Eval()
    rho = fp.SpVol.power(-1).Value(un.Density.lbm_ft3)
    gamma = (fp.SpHeatCp / fp.SpHeatCv).Value(un.Dimensionless.none) / 1.4
    xT = 0.72
    c0 = 63.3
    c1 = 0.66

    _mdot = mdot.Value(upph)
    _p1 = p1.Value(un.Pressure.psia)
    _p2 = p2.Value(un.Pressure.psia)

    if (_p1 < _p2):
        raise Exception('p1 must be greater than p2')

    _px = (_p1 - _p2) / _p1

    critical = True
    if (_px < gamma * xT):
        critical = False

    cv = 0.0

    if (critical):
        cv = _mdot / (c0 * c1 * np.sqrt(gamma * xT * _p1 * rho))
    else:
        cv = _mdot / (c0 * (1.0 - _px / (3.0 * gamma * xT)) * np.sqrt((_p1 - _p2) * rho))

    return cv

