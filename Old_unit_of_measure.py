import numpy as np
from enum import Enum

import cmath

class BaseQuantity(Enum):
    Mass = 0
    Length = 1
    Time = 2
    Current = 3
    Temperature = 4
    Amount = 5
    LuminousIntensity = 6
    Currency = 7
    _Count = 8

class Dimension:
    pass

class Quantity:
    pass

class Unit:
    pass

class Dimension:
    symbol = ['kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$']
    baseTypeName = 'Dimension'

    def __init__(self, other):
        self._exp = np.zeros(BaseQuantity._Count.value, dtype=np.int8)

        if type(other) == Dimension:
            self._exp = other._exp
        elif type(other) == np.ndarray:
            if len(other) == BaseQuantity._Count.value:
                self._exp = other
        elif type(other) == list:
            if len(other) == BaseQuantity._Count.value:
                for d in range(BaseQuantity._Count.value):
                    self._exp[d] = other[d]        
        else:
            raise TypeError("Invalid argument: %s " % other)
            return NotImplemented
            
    def __repr__(self):
        return f'Dimension({self._exp}'

    def __str__(self):
        sep = '*'
        result = ''
        # scan thru the list to add exponents in the numerator
        for d in range(BaseQuantity._Count.value):
            xp = self._exp[d]
            if xp <= 0:
                continue
            result += Dimension.symbol[d]
            if xp > 1:
                result += f'^{xp}'
            result += sep
        
        # clean up any trailing separator and add the '/' to start adding the denominator
        result = result.removesuffix(sep)
        if len(result) == 0:
            result = '1'
        result += '/'
        
        # scan thru the list to add exponents in the denominator
        for d in range(BaseQuantity._Count.value):
            xp = self._exp[d]
            if xp >= 0:
                continue
            result += Dimension.symbol[d]
            if xp < -1:
                result += f'^{-xp}'
            result += sep
        
        # clean up and trailing separators
        result = result.removesuffix(sep)
        result = result.removesuffix('/')
        result = result.removesuffix('1')
        return result
        
    @property
    def BaseTypeName(self) -> str:
        return Dimension.baseTypeName

    @property
    def HasDimension(self) -> bool:
        return True

    def __eq__(self, other) -> bool:
        if not isinstance(other, Dimension):
            raise TypeError("Unable to convert %s to Dimension" % other)
            return NotImplemented

        return (self._exp == other._exp).all()
            
    def __ne__(self, other) -> bool:
        return not (self == other)

    def __mul__(self, other) -> Dimension:
        if not isinstance(other, Dimension):
            raise TypeError("Unable to convert %s to Dimension" % other)
            return NotImplemented

        return Dimension(self._exp + other._exp)
        
    def __truediv__(self, other) -> Dimension:
        if not isinstance(other, Dimension):
            raise TypeError("Unable to convert %s to Dimension" % other)
            return NotImplemented

        return Dimension(self._exp - other._exp)

    # raises each exponent to the 'numer/denom' power.  'numer' and 'denom' must
    # be integers and the result of the exponentiation must be an integer.
    # this behavior differs from the standard Python pow() function
    def power(self, numer : int, denom : int = 1) -> Dimension:
        if not isinstance(numer, int):
            raise TypeError("Only integer exponents are supported")
            return NotImplemented
        if not isinstance(denom, int):
            raise TypeError("Only integer exponents are supported")
            return NotImplemented

        _result = self._exp * numer
        if denom != 1:
            if any(_result % denom):
                raise TypeError("not supported: pow() arguments would result in non-integer exponents")        
            else:
                _result = _result // denom

        return Dimension(_result)

    def sqrt(self) -> Dimension:
        return self.power(1, 2)

    def squared(self) -> Dimension:
        return self.power(2)

    def cubed(self) -> Dimension:
        return self.power(3)

# Create the fundamental dimensions
# 'm', 'kg', 's', 'A', 'K', 'mol', 'cd', '$'
Dimensionless               = Dimension([0, 0, 0, 0, 0, 0, 0, 0])
Mass_dimension              = Dimension([1, 0, 0, 0, 0, 0, 0, 0])
Length_dimension            = Dimension([0, 1, 0, 0, 0, 0, 0, 0])
Time_dimension              = Dimension([0, 0, 1, 0, 0, 0, 0, 0])
Current_dimension           = Dimension([0, 0, 0, 1, 0, 0, 0, 0])
Temperature_dimension       = Dimension([0, 0, 0, 0, 1, 0, 0, 0])
Amount_dimension            = Dimension([0, 0, 0, 0, 0, 1, 0, 0])
LuminousIntensity_dimension = Dimension([0, 0, 0, 0, 0, 0, 1, 0])
Currency_dimension          = Dimension([0, 0, 0, 0, 0, 0, 0, 1])


class Unit:
    baseTypeName = 'Unit'

    def __init__(self, symbol : str, dimension : Dimension, factor : float, offset : float = 0.0):
        # user_val = (base_val - offset) / factor) 
        if symbol is None:
            self._symbol = dimension.__str__()
        else:
            self._symbol = symbol

        self._dimension = dimension
        
        if factor > 0.0:
            self._factor = factor 
        else:
            raise ValueError("Factor must be positive: %s " % factor)

        self._offset = offset
    
    # q = 12.0 * inch
    # t = 100 * degC

    def Create(self, symbol : str):
        self._symbol = symbol

        return self

    def Value(self, siValue : float) -> float:
        return (siValue - self._offset) / self._factor

    def SIValue(self, value : float) -> float:
        return value * self._factor + self._offset

    @property
    def BaseTypeName(self) -> str:
        return Unit.baseTypeName

    @property
    def Factor(self) -> float:
        return self._factor

    @property
    def Offset(self) -> float:
        return self._offset

    @property
    def HasDimension(self) -> bool:
        return True

    @property
    def Dimension(self) -> Dimension:
        return self._dimension

    @property
    def Symbol(self) -> str:
        return self._symbol

    def __repr__(self):
        if self._offset == 0.0:
            return 'Unit({0}, Dimension({1}), factor={2})'.format(self._symbol, self._dimension, self._factor)
        else:
            return 'Unit({0}, Dimension({1}), factor={2} offset={3})'.format(self._symbol, self._dimension, self._factor, self._offset)


    def __str__(self):
        foo = 1.0
        return f'{foo} {self._dimension} = {self.Value(foo)} {self._symbol}'
        
    def Similar(self, other) -> bool:
        if type(other) != Unit:
            raise TypeError("Argument type not supported: %s " % other)
        
        return self._dimension == other._dimension

    def __eq__(self, other) -> bool:
        if self.Similar(other):
            if self._factor == other._factor:
                if self._offset == other._offset:
                    return True

        return False
    
    def __ne__(self, other) -> bool:
        return not (self == other)

    def __mul__(self, other):
        if type(other) == Unit:
            return Unit(None, self._dimension * other._dimension, self._factor * other._factor)
        if type(other) == float:
            return Quantity.__Build__(self.SIValue(other), self._dimension)
        if type(other) == int:
            return Quantity.__Build__(self.SIValue(float(other)), self._dimension)
        else:
            raise TypeError("Unable to convert %s to Unit" % other)

    def __rmul__(self, other):
        if type(other) == Unit:
            return Unit(None, self._dimension * other._dimension, self._factor * other._factor)
        if type(other) == float:
            return Quantity.__Build__(self.SIValue(other), self._dimension)
        if type(other) == int:
            return Quantity.__Build__(self.SIValue(float(other)), self._dimension)
        else:
            raise TypeError("Unable to convert %s to Unit" % other)

        
    def __truediv__(self, other)-> Unit:
        if type(other) == Unit:
            return Unit(None, self._dimension / other._dimension, self._factor / other._factor)
        raise TypeError("Unable to convert %s to Unit" % other)

    def power(self, numer, denom, symbol = None):
        _f = pow(self._factor, numer / denom)
        _d = self._dimension.power(int(numer), int(denom))
        return Unit(symbol, _d, _f)

    def sqrt(self, symbol = None):
        return self.power(1, 2, symbol)

    def squared(self, symbol = None):
        return self.power(2, 1, symbol)

    def cubed(self, symbol = None):
        return self.power(3, 1, symbol)

# Create the fundamental units
# 'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
unitless = Unit('', Dimensionless, 1.0)
# kilogram = Unit('kg', Mass_dimension, 1.0)
# meter = Unit('m', Length_dimension, 1.0)
# second = Unit('s', Time_dimension, 1.0)
# ampere = Unit('A', Current_dimension, 1.0)
# kelvin = Unit('K', Temperature_dimension, 1.0)
# mol = Unit('mol', Amount_dimension, 1.0)
# candela = Unit('cd', LuminousIntensity_dimension, 1.0)
# dollar = Unit('$', Currency_dimension, 1.0)

import xml.etree.ElementTree as ET

def parseExp(exptxt):
    result = [0] * 8

    # 'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
    #  m:0,kg:1,s:2,A:3,°K:4,Mol:5,cd:6
    explist = exptxt.split(',')
    for dim in explist:
        exp = dim.split(':')
        if exp[0] == 'kg':
            result[0] = int(exp[1])
        if exp[0] == 'm':
            result[1] = int(exp[1])
        if exp[0] == 's':
            result[2] = int(exp[1])
        if exp[0] == 'A':
            result[3] = int(exp[1])
        if exp[0] == '°K':
            result[4] = int(exp[1])
        if exp[0] == 'mol':
            result[5] = int(exp[1])
        if exp[0] == 'cd':
            result[6] = int(exp[1])
        if exp[0] == '$':
            result[7] = int(exp[1])
    return Dimension(result)

# Import units from .xml file
# See https://en.wikipedia.org/wiki/Alt_code for Alt special unit characters
# Alt  30 = ▲ - filled triangle - used for delta
# Alt 230 = µ - micron - 19
# Alt 234 = Ω - Omega - Ohm
# Alt 248 = ° - degree - angle, temperature

def LoadUnits(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    unitList = root.get('UnitsOfMeasure')

    ud = dict()

    for u in tree.findall('Unit'):
        symbol = u.find('Symbol').text
        factor = float(u.find('Factor').text)
        offset = float(u.find('Offset').text)
        exponents = u.find('Exponents').text
        explist = parseExp(exponents)
        newUnit = Unit(symbol, explist, factor, offset)
        ud[symbol] = newUnit
    
    return ud


class Quantity:
    baseTypeName = 'Quantity'

    def __init__(self, qty = None):
        if qty is None:
            self._val = np.nan
            self._dimension = None
        elif type(qty) == Quantity:
            self._val = qty._val
            self._dimension = qty._dimension
        else:
            raise TypeError("Invalid Unit argument: %s " % qty)


    def __Build__(val : float, dimension : Dimension) -> Quantity:
        newQty = Quantity()
        newQty._val = val
        newQty._dimension = dimension
        return newQty


    @property
    def BaseTypeName(self) -> str:
        return Quantity.baseTypeName


    @property
    def SIValue(self) -> float:
        return self._val


    @property
    def SIValueStr(self) -> str:
        return f'{self._val} {self.Dimension}'


    def As(self, unit : Unit, format_spec : str = '') -> str:
        if not self.Similar(unit):
            raise ValueError(f'invalid unit conversion: {unit.Symbol}')

        if len(format_spec) == 0:
            result = f'{unit.Value(self._val)} {unit.Symbol}'
        else:
            result = f'{unit.Value(self._val):{format_spec}} {unit.Symbol}'
        return result


    def Value(self, unit : Unit)-> float:
        return unit.Value(self._val)


    @property
    def HasDimension(self) -> bool:
        return True


    @property
    def Dimension(self) -> Dimension:
        return self._dimension


    def __repr__(self) -> str:
        return f'Quantity({self._val}, Dim({self._dimension})'


    def __str__(self) -> str:
        return f'{self._val} {self._dimension}'


    def __call__(self, unit: Unit) -> str:
        return self.As(unit)


    def Similar(self, other) -> bool:
        if other.BaseTypeName == Quantity.baseTypeName:
            return self._dimension == other._dimension
        if other.BaseTypeName == Unit.baseTypeName:
           return self._dimension == other.Dimension
        if other.BaseTypeName == Dimension.baseTypeName:
           return self._dimension == other
            
        raise TypeError("Argument type not supported: %s " % other)


    def __eq__(self, other) -> bool:
        if self.Similar(other):
            if self._val == other._val:
                return True

        return False


    def __gt__(self, other) -> bool:
        if self.Similar(other):
            if self._val > other._val:
                return True

        return False


    def __ge__(self, other) -> bool:
        if self.Similar(other):
            if self._val >= other._val:
                return True

        return False


    def __lt__(self, other) -> bool:
        if self.Similar(other):
            if self._val < other._val:
                return True

        return False


    def __le__(self, other) -> bool:
        if self.Similar(other):
            if self._val <= other._val:
                return True

        return False


    def __ne__(self, other) -> bool:
        return not (self == other)


    def __add__(self, other : Quantity) -> Quantity:
        if other.BaseTypeName == Quantity.baseTypeName:
            if self.Similar(other):
                return Quantity.__Build__(self._val + other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __radd__(self, other : Quantity) -> Quantity:
        if other.BaseTypeName == Quantity.baseTypeName:
            if self._unit.Similar(other):
                return Quantity.__Build__(self._val + other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __sub__(self, other : Quantity) -> Quantity:
        if other.BaseTypeName == Quantity.baseTypeName:
            if self.Similar(other):
                return Quantity.__Build__(self._val - other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __mul__(self, other) -> Quantity:
        if type(other) == float:
            return Quantity.__Build__(self._val * other, self._dimension)
        
        if type(other) == np.double:
            return Quantity.__Build__(self._val * other, self._dimension)
        
        if type(other) == int:
            return Quantity.__Build__(self._val * float(other), self._dimension)
        
        if other.BaseTypeName == Quantity.baseTypeName:
            return Quantity.__Build__(self._val * other._val, self._dimension * other._dimension)
        
        raise TypeError(f"***Unable to multiply type {type(other)} of {other} to Quantity")
            

    def __truediv__(self, other) -> Quantity:
        if type(other) == float:
            return Quantity.__Build__(self._val / other, self._dimension)
        
        if type(other) == np.double:
            return Quantity.__Build__(self._val / other, self._dimension)
        
        if type(other) == int:
            return Quantity.__Build__(self._val / float(other), self._dimension)
        
        if other.BaseTypeName == Quantity.baseTypeName:
            return Quantity.__Build__(self._val / other._val, self._dimension / other._dimension)
        
        raise TypeError("Unable to divide Quantity by %s" % other)


    def power(self, numer, denom = 1) -> Quantity:
        v = pow(self._val, numer / denom)
        d = self._dimension.power(int(numer), int(denom))
        return Quantity.__Build__(v, d)


    def sqrt(self) -> Quantity:
        return self.power(1, 2)


    def squared(self) -> Quantity:
        return self.power(2)


    def cubed(self) -> Quantity:
        return self.power(3)


# qtynan = np.nan * unitless


if __name__ == '__main__':
    def main():
        _dim = Dimension([0,    1,   0,   0,   0,   0,     0,    0])

        um    = Unit('m',    _dim, 1.0)
        ucm   = Unit('cm',   _dim, 0.01)
        umm   = Unit('mm',   _dim, 0.001)
        uKm   = Unit('Km',   _dim, 1000.0)
        uft   = Unit('ft',   _dim, 0.3048)
        uftUS = Unit('ftUS', _dim, 0.304800609601)
        uinch = Unit('in',   _dim, 0.0254)
        umil  = Unit('mil',  _dim, 0.0000254)
        umile = Unit('mi',   _dim, 1609.344)
        umiUS = Unit('miUS', _dim, 1609.34721869)
        unmi  = Unit('nmi',  _dim, 1852.0)
        uyd   = Unit('yd',   _dim, 0.9144)

        d1 = 3.0 * um
        d2 = uinch * 6.2345
        d3 = d1 + d2
        a1 = d1.squared()
        v1 = d1 * d2 * d3
        
        print(f'd3 = {d3.As(uinch, "0.2f")}')

    main()