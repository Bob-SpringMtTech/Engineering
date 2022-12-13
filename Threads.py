# Reference ASME B1.1-2003 Appendix B for the thread strength design formulas.

import math
import numpy as np

class ThreadUN:

    def __init__(self, size, tpi, series, cls):
        self._angle = 30
        self._d = size
        self._P = 1.0 / tpi
        self._series = series
        self._cls = cls
        self.__calculate_basic()
        self.__calculate_std_LE()
        self.__calculate_limits()

    def __calculate_basic(self):
        # These calculations are for UN thread profile only.  The UNR profile is not covered.

        # start by calculating the dimensions of the basic profile
        self._D = self._d                                       # Major diameter, internal thread
        self._H = math.cos(math.radians(self._angle)) * self._P # 10.1(d): Height of sharp V-thread (fundamental triangle)
        self._hs = 5.0 / 8.0 * self._H                          # 10.1(f): Height of external thread
        self._hn = self._hs                                     # 10.1(f): Height of internal thread

        # flat widths are expressed as function of pitch
        self._Fcs = 1.0 / 8.0 * self._P   # 10.1(h): Flat at crest of external thread
        self._Frs = 1.0 / 4.0 * self._P   # 10.1(h): Flat at root of external thread
        self._Fcn = self._Frs             # 10.1(k): Flat at crest of internal thread
        self._Frn =  1.0 / 8.0 * self._P  # 10.1(m): Flat at root of internal thread

        # truncations are expressed as functions of thread height
        self._fcs = 1.0 / 8.0 * self._H # 10.1(i): Truncation at crest of external tread
        self._fcn = 1.0 / 4.0 * self._H # 10.1(l): Truncation at crest of internal tread
        self._frn = 1.0 / 8.0 * self._H # 10.1(n): Truncation at root of internal tread
        self._frs = self._fcn           #          Truncation at root of external tread

        self._has = 3.0 / 8.0 * self._H  # 10.1(o): Addendum of external thread (pitch to crest of basic thread)
        self._hds = self._hs - self._has #          Dedendum of external thread (pitch to root of basic thread)
        self._hdn = self._has            #          Dedendum of internal thread (pitch to root of basic thread)
        self._han = self._hn - self._hdn #          Addendum of external thread (pitch to crest of basic thread)
        self._hb  = 2.0 * self._has      #          Table 5, column 13

        self._d2 = self._d - 2.0 * self._has # 10.1(p): Pitch diameter of external thread.
        self._d1 = self._d - 2.0 * self._hs  # 10.1(r): Minor diameter of UN external thread.
        self._D2 = self._D - 2.0 * self._hdn #          Pitch diameter of internal thread.
        self._D1 = self._D - 2.0 * self._hn  # 10.1(s): Minor diameter of internal thread.

        return self

    def __calculate_std_LE(self):
        # Section 5.1, Pitch Diameter Tolerance, All Classes
        self._LE = 0.0
        if self._series in [ 'UNC', 'UNF', '4-UN', '6-UN', '8-UN' ]:
            self._LE = self._D
        elif self._series in [ 'UNEF', '12-UN', '16-UN', '20-UN', '28-UN', '32-UN']:
            self._LE = 9.0 * self._P
        elif 'UNS' in self._series:
            self._LE = 9.0 * self._P
        elif 'Special' in self._series:
            self._LE = self._LE # Length of thread engagement must already be set.
        else:
            raise Exception(f'thread series "{self._series}" is not recognized')

        if self._cls not in [1, 2, 3]:
            raise Exception(f'thread class "{self._cls}" is not recognized.  Must be 1, 2, or 3')

        return self

    def __calculate_limits(self):
        # 5.8.1(b): Major diameter tolerance (External Threads)
        self._d_tol = 0.060 * math.pow(self._P, 2.0 / 3.0) # class 2 and 3
        if self._cls == 1:
            self._d_tol = 0.090 * math.pow(self._P, 2.0 / 3.0)

        # 5.8.1(c): Pitch diameter tolerance (External Threads)
        self._d2_tol = 0.0015 * (math.pow(self._D, 1.0 / 3.0) + math.sqrt(self._LE) + 10.0 * math.pow(self._P, 2.0 / 3.0)) # class 2
        if self._cls == 1:
            self._d2_tol *= 1.500
        elif self._cls == 3:
            self._d2_tol *= 0.750

        # 5.8.2(b): Pitch diameter tolerance (Internal Threads)
        self._D2_tol = 1.300 * self._d2_tol

        # 5.8.2(a): Major diameter tolerance (Internal Threads)
        self._D_tol = 1.0 / 6.0 * self._H + self._D2_tol

        # 5.8.2(c): Minor diameter tolerance (Internal Threads)
        D1_tol_A = 0.050 * math.pow(self._P, 2.0 / 3.0) + 0.030 * self._P / self._D - 0.002
        D1_tol_B = 0.394 * self._P
        D1_tol_C = 0.250 * self._P - 0.400 * self._P ** 2
        D1_tol_D = 0.150 * self._P
        D1_tol_E = 0.230 * self._P - 1.500 * self._P ** 2
        D1_tol_F = 0.120 * self._P

         # 5.8.2(c)(1) - not considering length of engagement because no alternate formulas were given.
        if self._cls in [1, 2]:
            if self._D < 0.250:
                self._D1_tol = D1_tol_A
                if self._D1_tol > D1_tol_B: # 5.8.2(c)(1)(a)
                    self._D1_tol = D1_tol_B
                elif self._D1_tol < D1_tol_C: # 5.8.2(c)(1)(b)
                    self._D1_tol = D1_tol_C
            else: # size is .250 and larger
                self._D1_tol = D1_tol_C
        else: # class 3 thread  # 5.8.2(c)(2)
            self._D1_tol = D1_tol_A
            if self._D1_tol > D1_tol_B: # 5.8.2(c)(2)(a)
                self._D1_tol = D1_tol_B
            else:
                if self._P < 0.08: # TPI >= 13 
                    if self._D1_tol < D1_tol_E: # 5.8.2(c)(2)(b)(1)
                        self._D1_tol = D1_tol_E
                else:
                    if self._D1_tol < D1_tol_F: # 5.8.2(c)(2)(b)(2)
                        self._D1_tol = D1_tol_F

        # 5.8.1(a): Allowance (applies to external threads only)
        self._allowance = 0.300 * self._d2_tol # class 1 and 2
        if self._cls == 3:
            self._allowance = 0.0

        # Table 17A
        self._d_max = self._d                              # Maximum major diameter
        self._d1_max = self._D1                            # Minor diameter, reference only 8.3.1(e)(1)(b)
        if self._cls in [1, 2]:
            self._d_max -= self._allowance
            self._d1_max -= self._allowance                # Maximum minor diameter, reference only 8.3.1(e)(1)(a)

        self._d_min = self._d_max - self._d_tol            # Minimum major diameter
        self._d2_max = self._d_max - self._hb              # Maximum pitch diameter
        self._d2_min = self._d2_max - self._d2_tol         # Minimum pitch diameter
        self._d1_min = self._d2_min - 0.64951905 * self._P # Minimum minor diameter, reference only 8.3.1(f)

        # Table 17B
        self._D1_min = self._D - 2.0 * self._hn            # Minimum minor diameter
        self._D1_max = self._D1_min + self._D1_tol          # Maximum minor diameter
        self._D2_min = self._D -  self._hb                 # Minimum pitch diameter
        self._D2_max = self._D2_min + self._D2_tol         # Maximum pitch diameter
        self._D_min = self._D                              # Minimum major diameter, 8.3.2(b), reference
        self._D_max = self._D_min + self._D_tol            # Maximum major diameter, 5.8.2(a)(1)

        return self

    def __str__(self):
        return f'size: {self._d} pitch: {self._P} pitch dia: {self._d2:0.4f} minor dia: {self._d1:0.4f}'

    @property
    def IncludedAngle(self):
        return (self._angle * 2.0)

    @property
    def HalfAngle(self):
        return self._angle

    @property
    def Size(self):
        return self._d

    @property
    def Pitch(self):
        return self._pitch

    @property
    def TPI(self):
        return 1.0 / self._pitch

    @property
    def Series(self):
        return self._series

    @property
    def Class(self):
        return self._cls

    @property
    def LE(self):
        return self._LE

    @LE.setter
    def LE(self, le):
        self._LE = le
        return self.__calculate_limits()

    def BasicDims(self):
        return f'major Φ: {self._d:0.4f}  pitch Φ: {self._d2:0.4f}  minor Φ: {self._d1:0.4f}  pitch: {self._P:0.4f}  hn: {self._hn:0.4f}  tsa: {self.TensileArea():0.5f}'

    def Major_External(self):
        nom = (self._d_max + self._d_min) / 2.0
        return np.round([self._d_max, nom, self._d_min], 4)

    def Pitch_External(self):
        nom = (self._d2_max + self._d2_min) / 2.0
        return np.round([self._d2_max, nom, self._d2_min], 4)

    def Minor_External(self):
        nom = (self._d1_max + self._d1_min) / 2.0
        return np.round([self._d1_max, nom, self._d1_min], 4)

    def Major_Internal(self):
        nom = (self._D_max + self._D_min) / 2.0
        return np.round([self._D_max, nom, self._D_min], 4)

    def Pitch_Internal(self):
        nom = (self._D2_max + self._D2_min) / 2.0
        return np.round([self._D2_max, nom, self._D2_min], 4)

    def Minor_Internal(self):
        nom = (self._D1_max + self._D1_min) / 2.0
        return np.round([self._D1_max, nom, self._D1_min], 4)

    def TensileArea(self, bore_dia=0.0):
        tsa = math.pi * ((self._D2 / 2.0 - 3.0 / 16.0 * self._H) ** 2)
        ba  = math.pi / 4.0 * bore_dia**2
        return tsa - ba

    def ShearAreaInternal(self):
        partA = math.pi * self._LE * self._d_min
        partB = self._P / 2.0 + 2.0 / 3.0 * math.cos(math.radians(self._angle))*(self._d_min - self._D2_max)
        return partA * partB

    def ShearAreaExternal(self):
        partA = math.pi * self._LE * self._D1_max
        partB = self._P / 2.0 + 2.0 / 3.0 * math.cos(math.radians(self._angle))*(self._d2_min - self._D1_max)
        return partA * partB

class ThreadM:
    pitch_list     = [0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.60, 0.70, 0.75, 0.80, 1.00, 1.25, 1.50, 1.75, 2.00, 2.50, 3.00, 350, 4.00, 4.50, 5.00, 5.50, 6.00, 8.00]
    basic_dia_list = [1.4, 2.8, 5.6, 11.2, 22.4, 45.0, 90.0, 180.0, 355.0]
    dia_pitch_list = [[0, 0.20], [0, 0.25], [0, 0.30], [1, 0.20], [1, 0.25], [1, 0.35], [1, 0.40], [1, 0.45], [2, 0.35], [2, 0.50], [2, 0.60], [2, 0.70], [2, 0.75], [2, 0.80], [3, 0.75], [3, 1.00], [3, 1.25], [3, 1.50], [4, 1.00], [4, 1.25], [4, 1.50], [4, 1.75], [4, 2.00], [4, 2.50], [5, 1.00], [5, 1.50], [5, 2.00], [5, 3.00], [5, 3.50], [5, 4.00], [5, 4.50], [6, 1.50], [6, 2.00], [6, 3.00], [6, 4.00], [6, 5.00], [6, 5.50], [6, 6.00], [7, 2.00], [7, 3.00], [7, 4.00], [7, 6.00], [7, 8.00], [8, 3.00], [8, 4.00], [8, 6.00], [8, 8.00]]

    table1_G = [17, 18, 18, 19, 19, 20, 20, 21, 22, 22, 24, 26, 28, 32, 34, 38, 42, 48, 53, 60, 63, 71, 75, 80, 100]
    table1_e = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, -50, -53, -56, 56, -60, -60, -63, -67, 71, -71, -80, -85, -90, -95, -100, -106, -112, -118, -140]
    table1_f = [np.nan, np.nan, np.nan, -34, -34, -35, -50, -53, -56, 56, -60, -60, -63, -67, 71, -71, -80, -85, -90, -95, -100, -106, -112, -118, -140]
    table1_g = [-17, -18, -18, -19, -19, -20, -20, -21, -22, -22, -24, -26, -28, -32, -34, -38, -42, -48, -53, -60, -63, -71, -75, -80, -100]

    def fundamental_deviation(pitch, tol_pos):
        if (tol_pos == 'H'):
            return 0.0
        if (tol_pos == 'h'):
            return 0.0

        loc = ThreadM.pitch_list.index(pitch)
        if (tol_pos == 'G'):
            return ThreadM.table1_G[loc]
        elif (tol_pos == 'e'):
            return ThreadM.table1_e[loc]
        elif (tol_pos == 'f'):
            return ThreadM.table1_f[loc]
        elif (tol_pos == 'g'):
            return ThreadM.table1_g[loc]
        
        return np.nan

    #             0    1    2    3     4     5     6     7      8     
    table2_catS = [0.5, 0.6, 0.7, 0.5, 0.6, 0.8, 1.0, 1.3, 1.0, 1.5, 1.7, 2.0, 2.2, 2.5, 2.4, 3.0,  4.0,  5.0,  3.8,  4.5,  5.6,  6.0,  8.0, 10.0,  4.0,  6.3,  8.5, 12.0, 15.0, 18.0, 21.0,  7.5,  9.5, 15.0, 19.0, 24.0, 28.0, 32.0, 12.0, 18.0, 24.0,  36.0,  45.0, 20.0, 26.0,  40.0,  50.0]
    table2_catL = [1.4, 1.7, 2.0, 1.5, 1.9, 2.6, 3.0, 3.8, 3.0, 4.5, 5.0, 6.0, 6.7, 7.5, 7.1, 9.0, 12.0, 15.0, 11.0, 13.0, 16.0, 18.0, 24.0, 30.0, 12.0, 19.0, 25.0, 36.0, 45.0, 53.0, 63.0, 22.0, 28.0, 45.0, 56.0, 71.0, 85.0, 95.0, 36.0, 53.0, 71.0, 106.0, 132.0, 60.0, 80.0, 118.0, 150.0]

    def thread_engagement_cat(dia, pitch, le):
        if (dia < 0.99):
            return np.nan
        loc = -1
        for i in range(len(ThreadM.basic_dia_list)):
            if (dia < ThreadM.basic_dia_list[i]):
                loc = i
                break
        if (loc == -1):
            return np.nan
        
        i_p = [i, pitch]
        row = ThreadM.dia_pitch_list.index(i_p)

        cat = 'N'
        if (le <= ThreadM.table2_catS[row]):
            cat = 'S'
        elif (le > ThreadM.table2_catL[row]):
            cat = 'L'

        return cat

    table3_tg4 = [38.0,     45.0,   53.0,   63.0,   71.0,   80.0,   90.0,  100.0,  112.0,  118.0, 125.0, 150.0, 170.0, 190.0, 212.0, 236.0, 280.0, 315.0, 355.0, 375.0,  425.0,  450.0,  475.0,  500.0, 630.0]
    table3_tg5 = [np.nan,   56.0,   67.0,   80.0,   90.0,  100.0,  112.0,  125.0,  140.0,  150.0, 160.0, 190.0, 212.0, 236.0, 265.0, 300.0, 355.0, 400.0, 450.0, 475.0,  530.0,  560.0,  600.0,  630.0, 800.0]
    table3_tg6 = [np.nan, np.nan,   85.0,  100.0,  112.0,  125.0,  140.0,  160.0,  180.0,  190.0, 200.0, 236.0, 265.0, 300.0, 335.0, 375.0, 450.0, 500.0, 560.0, 600.0,  670.0,  710.0,  750.0,  800.0, 1000.0]
    table3_tg7 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,  180.0,  200.0,  224.0,  236.0, 250.0, 300.0, 335.0, 375.0, 425.0, 475.0, 560.0, 630.0, 710.0, 750.0,  850.0,  900.0,  950.0, 1000.0, 1250.0]
    table3_tg8 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 315.0, 375.0, 425.0, 475.0, 530.0, 600.0, 710.0, 800.0, 900.0, 950.0, 1060.0, 1120.0, 1180.0, 1250.0, 1600.0]

    def TD1(pitch, tol_grade):
        loc = pitch_list.index(pitch)
        if (tol_grade == 4):
            return table3_tg4[loc]
        elif (tol_grade == 5):
            return table3_tg5[loc]
        elif (tol_grade == 6):
            return table3_tg6[loc]
        elif (tol_grade == 7):
            return table3_tg7[loc]
        elif (tol_grade == 8):
            return table3_tg8[loc]
        
        return np.nan

    table4_tg4 = [  36.0,   42.0,   48.0,   53.0,   60.0,   63.0,   67.0,   80.0,   90.0,   90.0,  95.0, 112.0, 132.0, 150.0, 170.0, 180.0, 212.0, 236.0, 265.0, 300.0, 315.0, 335.0, 355.0, 375.0,  450.0]
    table4_tg6 = [  56.0,   67.0,   75.0,   85.0,   95.0,  100.0,  106.0,  125.0,  140.0,  140.0, 150.0, 180.0, 212.0, 236.0, 265.0, 280.0, 335.0, 375.0, 425.0, 475.0, 500.0, 530.0, 560.0, 600.0,  710.0]
    table4_tg8 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 236.0, 280.0, 335.0, 375.0, 425.0, 450.0, 530.0, 600.0, 670.0, 750.0, 800.0, 850.0, 900.0, 950.0, 1180.0]

    def Td(pitch, tol_grade):
        loc = pitch_list.index(pitch)
        if (tol_grade == 4):
            return table4_tg4[loc]
        elif (tol_grade == 6):
            return table4_tg6[loc]
        elif (tol_grade == 8):
            return table4_tg8[loc]
        
        return np.nan

    table5_tg4 = [  40.0,   45.0,   48.0,   42.0,   48.0,   53.0,   56.0,   60.0,   56.0,   63.0,   71.0,   75.0,   75.0,  80.0,   85.0,  95.0, 100.0, 112.0, 100.0, 112.0, 118.0, 125.0, 132.0, 140.0,  106.0, 125.0, 140.0, 170.0, 180.0, 190.0, 200.0, 132.0, 150.0, 180.0, 200.0, 212.0, 224.0, 236.0, 160.0, 190.0, 212.0, 250.0, 280.0, 212.0, 236.0, 265.0, 300.0]
    table5_tg5 = [np.nan,   56.0,   60.0, np.nan,   60.0,   67.0,   71.0,   75.0,   71.0,   80.0,   90.0,   95.0,   95.0, 100.0,  106.0, 118.0, 125.0, 140.0, 125.0, 140.0, 150.0, 160.0, 170.0, 180.0,  132.0, 160.0, 180.0, 212.0, 224.0, 236.0, 250.0, 170.0, 190.0, 224.0, 250.0, 265.0, 280.0, 300.0, 200.0, 236.0, 265.0, 315.0, 355.0, 265.0, 300.0, 335.0, 375.0]
    table5_tg6 = [np.nan, np.nan,   75.0, np.nan, np.nan,   85.0,   90.0,   95.0,   90.0,  100.0,  112.0,  118.0,  118.0, 125.0,  132.0, 150.0, 160.0, 180.0, 160.0, 180.0, 190.0, 200.0, 212.0, 224.0,  170.0, 200.0, 224.0, 265.0, 280.0, 300.0, 315.0, 212.0, 236.0, 280.0, 315.0, 335.0, 355.0, 375.0, 250.0, 300.0, 335.0, 400.0, 450.0, 335.0, 375.0, 425.0, 475.0]
    table5_tg7 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan,  125.0,  140.0,  150.0,  150.0, 160.0,  170.0, 190.0, 200.0, 224.0, 200.0, 224.0, 236.0, 250.0, 265.0, 280.0,  212.0, 250.0, 280.0, 335.0, 355.0, 375.0, 400.0, 265.0, 300.0, 355.0, 400.0, 425.0, 450.0, 475.0, 315.0, 375.0, 425.0, 500.0, 560.0, 425.0, 475.0, 530.0, 600.0]
    table5_tg8 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 200.0, np.nan, 236.0, 250.0, 280.0, 250.0, 280.0, 300.0, 315.0, 335.0, 355.0, np.nan, 315.0, 335.0, 425.0, 450.0, 475.0, 500.0, 335.0, 375.0, 450.0, 500.0, 530.0, 560.0, 600.0, 400.0, 475.0, 530.0, 630.0, 710.0, 530.0, 600.0, 670.0, 750.0]

    def TD2(dia, pitch, tol_grade):
        if (dia < 0.99):
            return np.nan
        loc = -1
        for i in range(len(basic_dia_list)):
            if (dia < basic_dia_list[i]):
                loc = i
                break
        if (loc == -1):
            return np.nan
        
        if (tol_grade == 4):
            return table5_tg4[loc]
        elif (tol_grade == 5):
            return table5_tg5[loc]
        elif (tol_grade == 6):
            return table5_tg6[loc]
        elif (tol_grade == 7):
            return table5_tg7[loc]
        elif (tol_grade == 8):
            return table5_tg8[loc]

        return np.nan

    table6_tg3 = [  24.0,   26.0,   28.0,   25.0,   28.0,   32.0,   34.0,   36.0,   34.0,   38.0,   42.0,   45.0,   45.0,  48.0,   50.0,  56.0,  60.0,  67.0,  60.0,  67.0,  71.0,  75.0,  80.0,  85.0,  63.0,  75.0,  85.0, 100.0, 106.0, 112.0, 118.0,  80.0,  90.0, 106.0, 118.0, 125.0, 132.0, 140.0,  95.0, 112.0, 125.0, 150.0, 170.0, 125.0, 140.0, 160.0, 180.0]
    table6_tg4 = [  30.0,   34.0,   36.0,   32.0,   36.0,   40.0,   42.0,   45.0,   42.0,   48.0,   53.0,   56.0,   56.0,  60.0,   63.0,  71.0,  75.0,  85.0,  75.0,  85.0,  90.0,  95.0, 100.0, 106.0,  80.0,  95.0, 106.0, 125.0, 132.0, 140.0, 150.0, 100.0, 112.0, 132.0, 150.0, 160.0, 170.0, 180.0, 118.0, 140.0, 160.0, 190.0, 212.0, 160.0, 198.0, 200.0, 224.0]
    table6_tg5 = [  38.0,   42.0,   45.0,   40.0,   45.0,   50.0,   53.0,   56.0,   53.0,   60.0,   67.0,   71.0,   71.0,  75.0,   80.0,  90.0,  95.0, 106.0,  95.0, 106.0, 112.0, 118.0, 125.0, 132.0, 100.0, 118.0, 132.0, 160.0, 170.0, 180.0, 190.0, 125.0, 140.0, 170.0, 190.0, 200.0, 212.0, 224.0, 150.0, 180.0, 200.0, 236.0, 265.0, 200.0, 224.0, 250.0, 280.0]
    table6_tg6 = [  48.0,   53.0,   56.0,   50.0,   56.0,   63.0,   67.0,   71.0,   67.0,   75.0,   85.0,   90.0,   90.0,  95.0,  100.0, 112.0, 118.0, 132.0, 118.0, 132.0, 140.0, 150.0, 160.0, 170.0, 125.0, 150.0, 170.0, 200.0, 212.0, 224.0, 236.0, 160.0, 180.0, 212.0, 236.0, 250.0, 265.0, 280.0, 190.0, 224.0, 250.0, 300.0, 335.0, 250.0, 280.0, 315.0, 355.0]
    table6_tg7 = [np.nan, np.nan, np.nan, np.nan, np.nan,   80.0,   85.0,   90.0,   85.0,   95.0,  106.0,  112.0,  112.0, 118.0,  125.0, 140.0, 150.0, 170.0, 150.0, 170.0, 180.0, 190.0, 200.0, 212.0, 160.0, 190.0, 212.0, 250.0, 265.0, 280.0, 300.0, 200.0, 224.0, 265.0, 300.0, 315.0, 335.0, 355.0, 236.0, 280.0, 315.0, 375.0, 425.0, 315.0, 355.0, 400.0, 450.0]
    table6_tg8 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 150.0, np.nan, 180.0, 190.0, 212.0, 190.0, 212.0, 224.0, 236.0, 250.0, 265.0, 200.0, 236.0, 265.0, 315.0, 335.0, 355.0, 375.0, 250.0, 280.0, 335.0, 375.0, 400.0, 425.0, 450.0, 300.0, 355.0, 400.0, 475.0, 530.0, 400.0, 450.0, 500.0, 560.0]
    table6_tg9 = [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 190.0, np.nan, 224.0, 236.0, 265.0, 236.0, 365.0, 280.0, 300.0, 315.0, 335.0, 250.0, 300.0, 335.0, 400.0, 425.0, 450.0, 475.0, 315.0, 335.0, 425.0, 475.0, 500.0, 530.0, 560.0, 375.0, 450.0, 500.0, 600.0, 670.0, 500.0, 560.0, 630.0, 710.0]

    def Td2(dia, pitch, tol_grade):
        if (dia < 0.99):
            return np.nan
        loc = -1
        for i in range(len(basic_dia_list)):
            if (dia < basic_dia_list[i]):
                loc = i
                break
        if (loc == -1):
            return np.nan
        
        if (tol_grade == 3):
            return table6_tg3[loc]
        elif (tol_grade == 4):
            return table6_tg4[loc]
        elif (tol_grade == 5):
            return table6_tg5[loc]
        elif (tol_grade == 6):
            return table6_tg6[loc]
        elif (tol_grade == 7):
            return table6_tg7[loc]
        elif (tol_grade == 8):
            return table6_tg8[loc]
        elif (tol_grade == 9):
            return table6_tg9[loc]

        return np.nan



basic = 40.0
pitch = 3.00
le = 36.1
print(f'cat = {thread_engagement_cat(basic, pitch, le)}')




d = 0.5
tpi = 28
t1 = ThreadSeriesUN(d, tpi, 'UNEF', 2)
print(f'LE: {t1.LE:0.4f}   allow: {t1._allowance:0.4f}   p tol: {t1._d2_tol:0.6f}   TSA: {t1.TensileArea():0.6f}')
print(t1.BasicDims())
print(f'Ext - Maj: {t1.Major_External()}  Ext - Pitch: {t1.Pitch_External()}  Ext - Minor: {t1.Minor_External()}')
print(f'Int - Maj: {t1.Major_Internal()}  Int - Pitch: {t1.Pitch_Internal()}  Int - Minor: {t1.Minor_Internal()}')
