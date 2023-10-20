import numpy as np
from dataclasses import dataclass
from enum import Enum

import sys
eng_path = 'D:/SpringMountTech/Technical/Code Python/Engineering'
if not eng_path in sys.path:
    sys.path.append(eng_path)

import NIST330 as un

class WaterIAPWS97:
	pass


@dataclass
class EqnCoeff:
    I: int
    J: int
    n: float


class FluidProp:
	def __init__(self):
		self.Press = np.nan * un.Pressure.MPa
		self.Temp = np.nan * un.Temperature.degK
		self.Quality = np.nan
		self.SpVol = np.nan * un.SpVolume.m3_kg
		self.SpIntEnergy = np.nan * un.SpEnergy.kJ_kg
		self.SpEntropy = np.nan * un.SpEnergy.kJ_kg
		self.SpEnthalpy = np.nan * un.SpEnergy.kJ_kg
		self.SpHeatCp = np.nan * un.SpHeatCap.kJ_kgK
		self.SpHeatCv = np.nan * un.SpHeatCap.kJ_kgK
		self.AcousticVel = np.nan * un.Velocity.mps


class Region:
	def __init__(self):
		self.Properties = FluidProp()

	def InRange(press: un.Quantity, temp: un.Quantity):
		return False

	def Eval(self, press: un.Quantity, temp: un.Quantity):
		return self.Properties
		

class Boundary4:
	tbl34 = []
	tbl34.append(EqnCoeff(0, 0,  0.0000000000000E+00))
	tbl34.append(EqnCoeff(0, 0,  1.1670521452767E+03))
	tbl34.append(EqnCoeff(0, 0, -7.2421316703206E+05))
	tbl34.append(EqnCoeff(0, 0, -1.7073846940092E+01))
	tbl34.append(EqnCoeff(0, 0,  1.2020824702470E+04))
	tbl34.append(EqnCoeff(0, 0, -3.2325550322333E+06))
	tbl34.append(EqnCoeff(0, 0,  1.4915108613530E+01))
	tbl34.append(EqnCoeff(0, 0, -4.8232657361591E+03))
	tbl34.append(EqnCoeff(0, 0,  4.0511340542057E+05))
	tbl34.append(EqnCoeff(0, 0, -2.3855557567849E-01))
	tbl34.append(EqnCoeff(0, 0,  6.5017534844798E+02))

	def InRange(pt : un.Quantity):
		_inRange = False

		if (pt.Similar(un.Temperature.degK)):
			t = pt.Value(un.Temperature.degK)
			if (t >= 273.15 and t <= 647.096):
				_inRange = True
			
		if (pt.Similar(un.Pressure.MPa)):
			p = pt.Value(un.Pressure.MPa)
			if (p >= 0.000611213 and p <= 22.064):
				_inRange = True

		if (not _inRange):
			print(f'{pt} is outside of the range of Boundary4')
			
		return _inRange


	def Psat(temp: un.Quantity):
		if (not Boundary4.InRange(temp)):
			return np.nan * un.Pressure.MPa

		tStar = 1.0

		ts = temp.Value(un.Temperature.degK)

		tr = ts / tStar

		nu = tr + Boundary4.tbl34[9].n / (tr - Boundary4.tbl34[10].n)
		nuSq = nu ** 2

		A = nuSq + Boundary4.tbl34[1].n * nu + Boundary4.tbl34[2].n
		B = Boundary4.tbl34[3].n * nuSq + Boundary4.tbl34[4].n * nu + Boundary4.tbl34[5].n
		C = Boundary4.tbl34[6].n * nuSq + Boundary4.tbl34[7].n * nu + Boundary4.tbl34[8].n

		pr = ((2 * C) / (-B + np.sqrt((B ** 2) - 4.0 * A * C))) ** 4

		return pr * un.Pressure.MPa


	def Tsat(press: un.Quantity):
		if (not Boundary4.InRange(press)):
			return np.nan * un.Temperature.degK

		pStar = 1.0

		ps = press.Value(un.Pressure.MPa)

		pr = ps / pStar

		betaSq = np.sqrt(pr)
		beta = np.sqrt(betaSq)

		E = betaSq + Boundary4.tbl34[3].n * beta + Boundary4.tbl34[6].n
		F = Boundary4.tbl34[1].n * betaSq + Boundary4.tbl34[4].n * beta + Boundary4.tbl34[7].n
		G = Boundary4.tbl34[2].n * betaSq + Boundary4.tbl34[5].n * beta + Boundary4.tbl34[8].n

		D = (2 * G) / (-F - np.sqrt((F ** 2) - 4.0 * E * G))

		tr = Boundary4.tbl34[10].n + D - np.sqrt(((Boundary4.tbl34[10].n + D) ** 2) - 4.0 * (Boundary4.tbl34[9].n + Boundary4.tbl34[10].n * D))
		tr /= 2.0

		return tr * un.Temperature.degK


class B23:
	def __init__(self, tp: un.Quantity):
		tbl1 = [  0.0,
				  0.34805185628969e+3,
				 -0.11671859879975e+1, 
				  0.10192970039326e-2,
				  0.57254459862746e+3,
				  0.13918839778870e+2 ]

		pStar = 1.0
		tStar = 1.0

		self._temp = np.nan * un.Temperature.degK
		self._press = np.nan * un.Pressure.MPa

		if (tp.Similar(un.Temperature.degK)):
			t = tp.Value(un.Temperature.degK)

			phi = t / tStar

			pi = tbl1[1] + tbl1[2] * phi + tbl1[3] * (phi ** 2)

			p = pi * pStar

			self._press = p * un.Pressure.MPa

		if (tp.Similar(un.Pressure.MPa)):
			p = tp.Value(un.Pressure.MPa)

			pi = p / pStar

			phi = tbl1[4] + np.sqrt((pi - tbl1[5]) / tbl1[3])

			t = phi * tStar

			self._temp = t * un.Temperature.degK


	@property
	def Press(self):
		return self._press


	@property
	def Temp(self):
		return self._temp


class Region1(Region):
	tbl2 = []
	tbl2.append(EqnCoeff( 0,	 0,	 0))
	tbl2.append(EqnCoeff( 0,	-2,	 0.14632971213167))
	tbl2.append(EqnCoeff( 0,	-1,	-0.84548187169114))
	tbl2.append(EqnCoeff( 0,	 0, -0.37563603672040e1))
	tbl2.append(EqnCoeff( 0,	 1,  0.33855169168385e1))
	tbl2.append(EqnCoeff( 0, 	 2, -0.95791963387872))
	tbl2.append(EqnCoeff( 0,	 3,	 0.15772038513228))
	tbl2.append(EqnCoeff( 0,	 4, -0.16616417199501e-1))
	tbl2.append(EqnCoeff( 0,	 5,	 0.81214629983568e-3))
	tbl2.append(EqnCoeff( 1,	-9,	 0.28319080123804e-3))
	tbl2.append(EqnCoeff( 1,	-7,	-0.60706301565874e-3))
	tbl2.append(EqnCoeff( 1,	-1,	-0.18990068218419e-1))
	tbl2.append(EqnCoeff( 1,	 0,	-0.32529748770505e-1))
	tbl2.append(EqnCoeff( 1,	 1,	-0.21841717175414e-1))
	tbl2.append(EqnCoeff( 1,	 3,	-0.52838357969930e-4))
	tbl2.append(EqnCoeff( 2,	-3,	-0.47184321073267e-3))
	tbl2.append(EqnCoeff( 2,	 0,	-0.30001780793026e-3))
	tbl2.append(EqnCoeff( 2,	 1,	 0.47661393906987e-4))
	tbl2.append(EqnCoeff( 2,	 3,	-0.44141845330846e-5))
	tbl2.append(EqnCoeff( 2,	17,	-0.72694996297594e-15))
	tbl2.append(EqnCoeff( 3,	-4,	-0.31679644845054e-4))
	tbl2.append(EqnCoeff( 3,	 0,	-0.28270797985312e-5))
	tbl2.append(EqnCoeff( 3,	 6,	-0.85205128120103e-9))
	tbl2.append(EqnCoeff( 4,	-5,	-0.22425281908000e-5))
	tbl2.append(EqnCoeff( 4,	-2,	-0.65171222895601e-6))
	tbl2.append(EqnCoeff( 4,	10,	-0.14341729937924e-12))
	tbl2.append(EqnCoeff( 5,	-8,	-0.40516996860117e-6))
	tbl2.append(EqnCoeff( 8,   -11,	-0.12734301741641e-8))
	tbl2.append(EqnCoeff( 8,	-6, -0.17424871230634e-9))
	tbl2.append(EqnCoeff(21,   -29,	-0.68762131295531e-18))
	tbl2.append(EqnCoeff(23,   -31,	 0.14478307828521e-19))
	tbl2.append(EqnCoeff(29,   -38,	 0.26335781662795e-22))
	tbl2.append(EqnCoeff(30,   -39,	-0.11947622640071e-22))
	tbl2.append(EqnCoeff(31,   -40,	 0.18228094581404e-23))
	tbl2.append(EqnCoeff(32,   -41,	-0.93537087292458e-25))

	def __init__(self):
		Region.__init__(self)

	def InRange(press: un.Quantity, temp: un.Quantity):
		status = True

		t = temp.Value(un.Temperature.degK)
		p = press.Value(un.Pressure.MPa)
		ps = Boundary4.Psat(temp).Value(un.Pressure.MPa)
		
		if (t < 273.15):
			status = False
		elif (t > 623.15):
			status = False 
		elif (p < ps):
			status = False
		elif (p > 100.0):
			status = False

		if (not status):
			print(f'{press} {temp} is outside of Region1')
		else:
			print(f'{press} {temp} is inside of Region1')
			
		return status
		
	def Eval(self, press: un.Quantity, temp: un.Quantity):
		pStar = 16.53
		tStar = 1386.0

		p = press.Value(un.Pressure.MPa)
		t = temp.Value(un.Temperature.degK)

		pi = p / pStar
		tau = tStar / t

		pp = 7.1 - pi
		tt = tau - 1.222
		
		gamma = 0.0
		gammaPi = 0.0
		gammaPiPi = 0.0
		gammaTau = 0.0
		gammaTauTau = 0.0
		gammaPiTau = 0.0

		for i in range(1, 35):
			I = Region1.tbl2[i].I
			J = Region1.tbl2[i].J
			n = Region1.tbl2[i].n

			gamma += n * (pp ** I) * (tt ** J)
			gammaPi += -n * I * (pp ** (I - 1)) * (tt ** J)
			gammaPiPi += n * I * (I - 1) * (pp ** (I - 2)) * (tt ** J)
			gammaTau += n * (pp ** I) * J * (tt ** (J - 1))
			gammaTauTau += n * (pp ** I) * J * (J - 1) * (tt ** (J - 2))
			gammaPiTau += -n * I * (pp ** (I - 1)) * J * (tt ** (J - 1))

		Rc = WaterIAPWS97.Rc

		self.Properties.Press = press
		self.Properties.Temp = temp
		self.Properties.Quality = 0.0
		
		self.Properties.SpVol = Rc * temp / press * pi * gammaPi

		self.Properties.SpIntEnergy = Rc * temp * (tau * gammaTau - pi * gammaPi)
		
		self.Properties.SpEntropy = Rc * (tau * gammaTau - gamma)

		self.Properties.SpEnthalpy = Rc * temp * (tau * gammaTau)

		self.Properties.SpHeatCp = Rc * (-(tau ** 2) * gammaTauTau)

		self.Properties.SpHeatCv = Rc * (-(tau ** 2) * gammaTauTau + ((gammaPi - tau * gammaPiTau) ** 2) / gammaPiPi)

		numer = gammaPi ** 2
		denom = (gammaPi - tau * gammaPiTau) ** 2 / (tau ** 2 * gammaTauTau) - gammaPiPi
		self.Properties.AcousticVel = (Rc * temp * numer / denom).sqrt()

		return self.Properties


class Region2(Region):
	tbl10 = []
	tbl10.append(EqnCoeff( 0,	0,  0.0))
	tbl10.append(EqnCoeff( 0,  0, -9.6927686500217E+00))
	tbl10.append(EqnCoeff( 0,  1,  1.0086655968018E+01))
	tbl10.append(EqnCoeff( 0, -5, -5.6087911283020E-03))
	tbl10.append(EqnCoeff( 0, -4,  7.1452738081455E-02))
	tbl10.append(EqnCoeff( 0, -3, -4.0710498223928E-01))
	tbl10.append(EqnCoeff( 0, -2,  1.4240819171444E+00))
	tbl10.append(EqnCoeff( 0, -1, -4.3839511319450E+00))
	tbl10.append(EqnCoeff( 0,  2, -2.8408632460772E-01))
	tbl10.append(EqnCoeff( 0,  3,  2.1268463753307E-02))
	
	tbl11 = []
	tbl11.append(EqnCoeff( 0,  0,  0.0))
	tbl11.append(EqnCoeff( 1,  0, -1.7731742473213E-03))
	tbl11.append(EqnCoeff( 1,  1, -1.7834862292358E-02))
	tbl11.append(EqnCoeff( 1,  2, -4.5996013696365E-02))
	tbl11.append(EqnCoeff( 1,  3, -5.7581259083432E-02))
	tbl11.append(EqnCoeff( 1,  6, -5.0325278727930E-02))
	tbl11.append(EqnCoeff( 2,  1, -3.3032641670203E-05))
	tbl11.append(EqnCoeff( 2,  2, -1.8948987516315E-04))
	tbl11.append(EqnCoeff( 2,  4, -3.9392777243355E-03))
	tbl11.append(EqnCoeff( 2,  7, -4.3797295650573E-02))
	tbl11.append(EqnCoeff( 2, 36, -2.6674547914087E-05))
	tbl11.append(EqnCoeff( 3,  0,  2.0481737692309E-08))
	tbl11.append(EqnCoeff( 3,  1,  4.3870667284435E-07))
	tbl11.append(EqnCoeff( 3,  3, -3.2277677238570E-05))
	tbl11.append(EqnCoeff( 3,  6, -1.5033924542148E-03))
	tbl11.append(EqnCoeff( 3, 35, -4.0668253562649E-02))
	tbl11.append(EqnCoeff( 4,  1, -7.8847309559367E-10))
	tbl11.append(EqnCoeff( 4,  2,  1.2790717852285E-08))
	tbl11.append(EqnCoeff( 4,  3,  4.8225372718507E-07))
	tbl11.append(EqnCoeff( 5,  7,  2.2922076337661E-06))
	tbl11.append(EqnCoeff( 6,  3, -1.6714766451061E-11))
	tbl11.append(EqnCoeff( 6, 16, -2.1171472321355E-03))
	tbl11.append(EqnCoeff( 6, 35, -2.3895741934104E+01))
	tbl11.append(EqnCoeff( 7,  0, -5.9059564324270E-18))
	tbl11.append(EqnCoeff( 7, 11, -1.2621808899101E-06))
	tbl11.append(EqnCoeff( 7, 25, -3.8946842435739E-02))
	tbl11.append(EqnCoeff( 8,  8,  1.1256211360459E-11))
	tbl11.append(EqnCoeff( 8, 36, -8.2311340897998E+00))
	tbl11.append(EqnCoeff( 9, 13,  1.9809712802088E-08))
	tbl11.append(EqnCoeff(10,  4,  1.0406965210174E-19))
	tbl11.append(EqnCoeff(10, 10, -1.0234747095929E-13))
	tbl11.append(EqnCoeff(10, 14, -1.0018179379511E-09))
	tbl11.append(EqnCoeff(16, 29, -8.0882908646985E-11))
	tbl11.append(EqnCoeff(16, 50,  1.0693031879409E-01))
	tbl11.append(EqnCoeff(18, 57, -3.3662250574171E-01))
	tbl11.append(EqnCoeff(20, 20,  8.9185845355421E-25))
	tbl11.append(EqnCoeff(20, 35,  3.0629316876232E-13))
	tbl11.append(EqnCoeff(20, 48, -4.2002467698208E-06))
	tbl11.append(EqnCoeff(21, 21, -5.9056029685639E-26))
	tbl11.append(EqnCoeff(22, 53,  3.7826947613457E-06))
	tbl11.append(EqnCoeff(23, 39, -1.2768608934681E-15))
	tbl11.append(EqnCoeff(24, 26,  7.3087610595061E-29))
	tbl11.append(EqnCoeff(24, 40,  5.5414715350778E-17))
	tbl11.append(EqnCoeff(24, 58, -9.4369707241210E-07))

	def __init__(self):
		Region.__init__(self)

	def InRange(press: un.Quantity, temp: un.Quantity):
		t = temp.Value(un.Temperature.degK)
		p = press.Value(un.Pressure.MPa)
		ps = Boundary4.Psat(temp).Value(un.Pressure.MPa)
		p23 = B23(temp).Press.Value(un.Pressure.MPa)
		
		_inRange = False

		if (t >= 273.15) and (t <= 623.15):
			if (p > 0.0) and (p <= ps):
				_inRange = True

		if (t > 623.15) and (t <= 863.15):
			if (p > 0.0) and (p <= p23):
				_inRange = True

		if (t > 863.15) and (t <= 1073.15):
			if (p > 0.0) and (p <= 100.0):
				_inRange = True
		
		if (not _inRange):
			print(f'{press} {temp} is outside of Region2')
		else:
			print(f'{press} {temp} is inside of Region2')

		return _inRange

	def Eval(self, press: un.Quantity, temp: un.Quantity):
		pStar = 1.0
		tStar = 540.0

		p = press.Value(un.Pressure.MPa)
		t = temp.Value(un.Temperature.degK)

		pi = p / pStar
		tau = tStar / t

		# Table 13.  Calculate the ideal-gas part of the dimansionless Gibbs free energy and its derivatives
		# according to equation 16
		gammaO = np.log(pi)
		gammaOpi = 1.0 / pi
		gammaOpipi = -1.0 / (pi ** 2)
		gammaOtau = 0.0
		gammaOtautau = 0.0
		gammaOpitau = 0.0

		for i in range(1, 10):
			J = self.tbl10[i].J
			n = self.tbl10[i].n

			gammaO += n * (tau ** J)
			gammaOtau += n * J * (tau ** (J-1))
			gammaOtautau += n * J * (J-1) * (tau ** (J-2))

		# Table 14.  Calculate the residual part of the dimansionless Gibbs free energy and its derivatives
		# according to equation 17
		tt = tau-0.5
		gammaR = 0.0
		gammaRpi = 0.0
		gammaRpipi = 0.0
		gammaRtau = 0.0
		gammaRtautau = 0.0
		gammaRpitau = 0.0

		for i in range(1, 44):
			I = self.tbl11[i].I
			J = self.tbl11[i].J
			n = self.tbl11[i].n

			gammaR += n * (pi ** I) * (tt ** J)
			gammaRpi += n * I * (pi ** (I-1)) * (tt ** J)
			gammaRpipi += n * I * (I-1) * (pi ** (I-2)) * (tt ** J)
			gammaRtau +=  n * (pi ** I) * J * (tt ** (J-1))
			gammaRtautau += n * (pi ** I) * J * (J-1) * (tt ** (J-2))
			gammaRpitau += n * I * (pi ** (I-1)) * J * (tt ** (J-1))

		gamma = gammaO + gammaR
		gammaPi = gammaOpi + gammaRpi
		gammaPiPi = gammaOpipi + gammaRpipi
		gammaTau = gammaOtau + gammaRtau
		gammaTauTau = gammaOtautau + gammaRtautau
		gammaPiTau = gammaOpitau + gammaRpitau

		Rc = WaterIAPWS97.Rc

		self.Properties.Press = press
		self.Properties.Temp = temp
		self.Properties.Quality = 1.0

		self.Properties.SpVol = Rc * temp / press * pi * gammaPi

		self.Properties.SpIntEnergy = Rc * temp * (tau * gammaTau - pi * gammaPi)
		
		self.Properties.SpEntropy = Rc * (tau * gammaTau - gamma)

		self.Properties.SpEnthalpy = Rc * temp * (tau * gammaTau)

		self.Properties.SpHeatCp = Rc * (-(tau ** 2) * gammaTauTau)

		numer = (1.0 + pi * gammaRpi - tau * pi * gammaRpitau) ** 2
		denom = 1.0 - (pi ** 2) * gammaRpipi
		self.Properties.SpHeatCv = self.Properties.SpHeatCp - Rc * numer / denom

		numer = 1.0 + 2.0 * pi * gammaRpi + (pi ** 2) * (gammaRpi ** 2)
		denomA = 1.0 - (pi ** 2) * gammaRpipi
		denomB = (1.0 + pi * gammaRpi - tau * pi * gammaRpitau) ** 2
		denomC = (tau ** 2) * gammaTauTau
		denom = denomA + denomB / denomC
		self.Properties.AcousticVel = (Rc * temp * numer / denom).sqrt()

		return self.Properties


class SatType(Enum):
	SatOff = 0
	SatTemp = 1
	SatPress = 2


class WaterIAPWS97:
	uRc = un.SpHeatCap.kJ_kgK
	uT = un.Temperature.degK
	uP = un.Pressure.MPa
	uRho = un.Density.kg_m3

	pNan = np.nan * uP
	tNan = np.nan * uT

	Rc    = 0.461526 * uRc		# IF97 (1)
	Tcr   = 647.096 * uT		# IF97 (2)
	Pcr   = 22.064 * uP			# IF97 (3)
	RHOcr = 322.0 * uRho		# IF97 (4)
	Ttp   = 273.16 * uT			# IF97 (9)
	Ptp   = 611.657 * un.Pressure.Pa # IF97 (9)

	def __init__(self):
		super().__init__()
		self.Saturation = SatType.SatOff
		self.Properties = FluidProp()

	def SetCond(self, press : un.Quantity = pNan, temp : un.Quantity = tNan):
		self.Properties.Press = press
		self.Properties.Temp = temp

		if ((press == WaterIAPWS97.pNan) and (temp == WaterIAPWS97.tNan)):
			self.Saturation = SatType.SatOff	

		return self
	
	def SetSaturation(self, satCond):
		if (satCond == SatType.SatOff):
			self.Saturation = SatType.SatOff
		if (satCond == SatType.SatTemp):
			self.Saturation = SatType.SatTemp
		if (satCond == SatType.SatPress):
			self.Saturation = SatType.SatPress

		return self

	# 0.0 quality is saturated water, 1.0 is saturated vapor, ignored if atSaturation is False
	def SetQuality(self, quality: float):
		if (quality > 1.0):
			print('*** Quality ranges from 0 (liquid) to 1.0 (vapor) ***')
		self.Properties.Quality = quality
		return self
	
	def Eval(self):
		if (self.Saturation == SatType.SatTemp):
			self.Properties.Press = Boundary4.Psat(self.Properties.Temp)
		elif (self.Saturation == SatType.SatPress):
			self.Properties.Temp = Boundary4.Tsat(self.Properties.Press)

		if (self.Saturation == SatType.SatOff):
			if (Region1.InRange(press = self.Properties.Press, temp = self.Properties.Temp)):
				self.Properties = Region1().Eval(press = self.Properties.Press, temp = self.Properties.Temp)
			elif (Region2.InRange(press = self.Properties.Press, temp = self.Properties.Temp)):
				self.Properties = Region2().Eval(press = self.Properties.Press, temp = self.Properties.Temp)
		else:
			liqRegion = Region1()
			liqRegion.Eval(self.Properties.Press, self.Properties.Temp)
			
			vapRegion = Region2()
			vapRegion.Eval(self.Properties.Press, self.Properties.Temp)

			self.MixProperties(liqRegion, vapRegion)			

		return self.Properties

	def MixProperties(self, liqProp, vapProp):
		q = self.Properties.Quality
		self.Properties.SpVol = MixValues(q, liqProp.Properties.SpVol, vapProp.Properties.SpVol)
		self.Properties.SpIntEnergy = MixValues(q, liqProp.Properties.SpIntEnergy, vapProp.Properties.SpIntEnergy)
		self.Properties.SpEntropy = MixValues(q, liqProp.Properties.SpEntropy, vapProp.Properties.SpEntropy)
		self.Properties.SpEnthalpy = MixValues(q, liqProp.Properties.SpEnthalpy, vapProp.Properties.SpEnthalpy)
		self.Properties.SpHeatCp = MixValues(q, liqProp.Properties.SpHeatCp, vapProp.Properties.SpHeatCp)
		self.Properties.SpHeatCv = MixValues(q, liqProp.Properties.SpHeatCv, vapProp.Properties.SpHeatCv)
		self.Properties.AcousticVel = MixValues(q, liqProp.Properties.AcousticVel, vapProp.Properties.AcousticVel)
		# I don't think acoustic velocity follows this simple mixing rule.
		if (q > 0.0 and q < 1.0):
			self.Properties.AcousticVel = np.nan * un.Velocity.mps

def MixValues(quality, liq : un.Quantity, vap : un.Quantity):
	return (vap * quality) + (liq * (1.0 - quality))
