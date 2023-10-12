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
        
    BaseTypeName = 'Dimension'

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


class Quantity:
    def __init__(self, qty = None):
        if qty is None:
            self._val = np.nan
            self._dimension = None
        elif type(qty) == Quantity:
            self._val = qty._val
            self._dimension = qty._dimension
        elif type(qty) == float:
            self._val = qty
            self._dimension = Dimensionless
        elif type(qty) == int:
            self._val = float(qty)
            self._dimension = Dimensionless
        else:
            raise TypeError("Invalid Unit argument: %s " % qty)


    @classmethod
    def Create(cls, val : float, dimension : Dimension) -> Quantity:
        qty = Quantity()
        qty._val = val
        qty._dimension = dimension
        return qty


    BaseTypeName = 'Quantity'


    @property
    def SIValue(self) -> float:
        return self._val


    @property
    def SIValueStr(self) -> str:
        return f'{self._val} {self.Dimension}'


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
        return self.Format(unit)


    def Similar(self, other) -> bool:
        if other.BaseTypeName == Quantity.BaseTypeName:
            return self.Dimension == other.Dimension
        if other.BaseTypeName == Unit.BaseTypeName:
           return self.Dimension == other.Dimension
        if other.BaseTypeName == Dimension.BaseTypeName:
           return self.Dimension == other
            
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
        if other.BaseTypeName == Quantity.BaseTypeName:
            if self.Similar(other):
                return Quantity.Create(self._val + other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __radd__(self, other : Quantity) -> Quantity:
        if other.BaseTypeName == Quantity.BaseTypeName:
            if self._unit.Similar(other):
                return Quantity.Create(self._val + other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __sub__(self, other : Quantity) -> Quantity:
        if other.BaseTypeName == Quantity.BaseTypeName:
            if self.Similar(other):
                return Quantity.Create(self._val - other._val, self._dimension)
            else:
                raise ValueError("Quantities must be dimensionally equal")
        raise TypeError("Unable to convert %s to Quantity" % other)


    def __mul__(self, other) -> Quantity:
        if type(other) == float:
            return Quantity.Create(self._val * other, self._dimension)
        
        if type(other) == np.double:
            return Quantity.Create(self._val * other, self._dimension)
        
        if type(other) == int:
            return Quantity.Create(self._val * float(other), self._dimension)
        
        if other.BaseTypeName == Quantity.BaseTypeName:
            return Quantity.Create(self._val * other._val, self._dimension * other._dimension)
        
        raise TypeError(f"***Unable to multiply type {type(other)} of {other} to Quantity")
            

    def __rmul__(self, other) -> Quantity:
        return self.__mul__(other)


    def __truediv__(self, other) -> Quantity:
        if type(other) == float:
            return Quantity.Create(self._val / other, self._dimension)
        
        if type(other) == np.double:
            return Quantity.Create(self._val / other, self._dimension)
        
        if type(other) == int:
            return Quantity.Create(self._val / float(other), self._dimension)
        
        if other.BaseTypeName == Quantity.BaseTypeName:
            return Quantity.Create(self._val / other._val, self._dimension / other._dimension)
        
        raise TypeError("Unable to divide Quantity by %s" % other)


    def __rtruediv__(self, other) -> Quantity:
        return other * self.power(-1)


    def power(self, numer, denom = 1) -> Quantity:
        v = pow(self._val, numer / denom)
        d = self._dimension.power(int(numer), int(denom))
        return Quantity.Create(v, d)


    def sqrt(self) -> Quantity:
        return self.power(1, 2)


    def squared(self) -> Quantity:
        return self.power(2)


    def cubed(self) -> Quantity:
        return self.power(3)
    

    def Value(self, unit : Unit = None)-> float:
        if (unit is None):
            return self._val # base SI value
        else:
            return unit.Value(self)


    def Format(self, unit : Unit = None, format_spec : str = '') -> str:
        if (unit is None):
            if len(format_spec) == 0:
                return f'{self._val} {self.Dimension}'
            else:
                return f'{self._val}:{format_spec} {self.Dimension}'

        if not self.Similar(unit.Factor):
            raise ValueError(f'invalid unit conversion: {unit.Symbol}')

        if len(format_spec) == 0:
            result = f'{self.Value(unit)} {unit.Symbol}'
        else:
            xxx = self.Value(unit)
            result = f'{xxx:{format_spec}} {unit.Symbol}'
            #result = f'{self.Value(unit):{format_spec}} {unit.Symbol}'
        return result

class Unit(Quantity):

    def __init__(self, symbol : str, factor : Quantity, offset : Quantity = None):
        if factor.SIValue <= 0.0:
            raise ValueError("factor must be positive: %s " % factor)
        if not offset is None:
            if not factor.Similar(offset):
                raise ValueError("factor and offset must have equal dimensions")

        # user_val = (base_val - offset) / factor) 
        # base_val = user_val * factor + offset
        if symbol is None:
            self._symbol = factor.Dimension.__str__()
        else:
            self._symbol = symbol
        
        self._factor = factor
        if offset is None:
            self._offset = 0.0 * factor
        else:
            self._offset = offset
    

    @classmethod
    def Create(cls, symbol: str, dimension : Dimension, factor : float, offset : float = 0.0) -> Unit:
        return Unit(symbol, Quantity.Create(factor, dimension), Quantity.Create(offset, dimension))


    def Value(self, qty : Quantity) -> float:
        if (qty.Similar(self._factor)):
            return (qty.SIValue - self._offset.SIValue) / self._factor.SIValue
        else:
            raise ValueError(f'qty can not be expressed in {self._symbol} units')


    BaseTypeName = 'Unit'


    @property
    def Factor(self) -> Quantity:
        return self._factor


    @property
    def Offset(self) -> Quantity:
        return self._offset


    @property
    def Symbol(self) -> str:
        return self._symbol


    @property
    def HasDimension(self) -> bool:
        return True


    @property
    def Dimension(self) -> Dimension:
        return self.Factor.Dimension


    def __repr__(self):
        if self._offset.SIValue == 0.0:
            return f'Unit({self._symbol}, Dimension({self._factor.Dimension}), factor={self._factor.SIValue})'
        else:
            return f'Unit({self._symbol}, Dimension({self._factor.Dimension}), factor={self._factor.SIValue} offset={self._offset.SIValue})'


    def __str__(self):
        foo = 1.0 * self
        return f'{foo.SIValue} {self.Dimension} = {self.Value(foo)} {self._symbol}'


    def __eq__(self, other) -> bool:
        if type(other) == Unit:
            if self.Factor == other.Factor:
                if self.Offset == other.Offset:
                    return True

        return False


    # user_val = (base_val - offset) / factor) 
    # base_val = user_val * factor + offset
    def __mul__(self, other) -> Quantity:
        return other * self.Factor + self.Offset
            

    def __rmul__(self, other) -> Quantity:
        return self.__mul__(other)
            

    def __truediv__(self, other) -> Quantity:
        if self._offset.SIValue == 0.0:
            return self._factor / other
        else:
            raise ValueError('division of Units with offsets is invalid')


    def __rtruediv__(self, other) -> Quantity:
        if self._offset.SIValue == 0.0:
            return other / self.Factor
        else:
            raise ValueError('division by Units with offsets is invalid')


    def power(self, numer, denom = 1) -> Quantity:
        if self._offset.SIValue == 0.0:
            return self.Factor.power(numer, denom)
        else:
            raise ValueError('power() is invalid with Units with offsets')


    def sqrt(self) -> Quantity:
        if self._offset.SIValue == 0.0:
            return self.Factor.sqrt()
        else:
            raise ValueError('sqrt() is invalid with Units with offsets')


    def squared(self) -> Quantity:
        if self._offset.SIValue == 0.0:
            return self.Factor.squared()
        else:
            raise ValueError('squared() is invalid with Units with offsets')


    def cubed(self) -> Quantity:
        if self._offset.SIValue == 0.0:
            return self.Factor.cubed()
        else:
            raise ValueError('cubed() is invalid with Units with offsets')

"""
class Unit(Quantity):

    def __init__(self, symbol : str, factor : Quantity, offset : Quantity = None):
        super().__init__(factor)
        if factor.SIValue <= 0.0:
            raise ValueError("Factor must be positive: %s " % factor)

        # user_val = (base_val - offset) / factor) 
        # base_val = user_val * factor + offset
        if symbol is None:
            self._symbol = self._dimension.__str__()
        else:
            self._symbol = symbol
        
        if offset is None:
            self._offset = 0.0
        else:
            self._offset = offset.SIValue
    

    @classmethod
    def Create(cls, symbol: str, dimension : Dimension, factor : float, offset : float = 0.0) -> Unit:
        q_factor = Quantity.Create(factor, dimension)
        q_offset = Quantity.Create(offset, dimension)
        unit = Unit(symbol, q_factor, q_offset)
        return unit


    def Value(self, qty : Quantity) -> float:
        return (qty.SIValue - self._offset) / self.Factor


    @property
    def Factor(self) -> float:
        return super().SIValue


    @property
    def Offset(self) -> float:
        return self._offset


    @property
    def Symbol(self) -> str:
        return self._symbol


    def __repr__(self):
        if self._offset == 0.0:
            return f'Unit({self._symbol}, Dimension({super().Dimension}), factor={self.Factor})'
        else:
            return f'Unit({self._symbol}, Dimension({super().Dimension}), factor={self.Factor} offset={self.Offset})'


    def __str__(self):
        foo = 1.0
        return f'{foo} {self._dimension} = {self.Value(foo)} {self._symbol}'


    def __eq__(self, other) -> bool:
        if self.Similar(other):
            if self.SIValue == other.SIValue:
                if self._offset == other._offset:
                    return True

        return False


    def __mul__(self, other) -> Quantity:
        result = super().__mul__(other)
        result._val += self._offset
        return result
            

    def __rmul__(self, other) -> Quantity:
        return self.__mul__(other)
            

    def __truediv__(self, other) -> Quantity:
        if self._offset == 0.0:
            return super().__truediv__(other)
        else:
            raise ValueError('division of Units with offsets is invalid')


    def __rtruediv__(self, other) -> Quantity:
        if self._offset == 0.0:
            return super().__rtruediv__(other)
        else:
            raise ValueError('division by Units with offsets is invalid')


    def power(self, numer, denom = 1) -> Quantity:
        if self._offset == 0.0:
            return super().power(numer, denom)
        else:
            raise ValueError('power() is invalid with Units with offsets')


    def sqrt(self) -> Quantity:
        if self._offset == 0.0:
            return super().sqrt()
        else:
            raise ValueError('sqrt() is invalid with Units with offsets')


    def squared(self) -> Quantity:
        if self._offset == 0.0:
            return super().squared()
        else:
            raise ValueError('squared() is invalid with Units with offsets')


    def cubed(self) -> Quantity:
        if self._offset == 0.0:
            return super().cubed()
        else:
            raise ValueError('cubed() is invalid with Units with offsets')

"""
# Create the fundamental units
# 'kg', 'm', 's', 'A', 'K', 'mol', 'cd', '$'
# unitless = Unit('', Quantity(1.0, Dimensionless))
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
        newUnit = Unit(symbol, Quantity(factor, explist), Quantity(offset, explist))
        ud[symbol] = newUnit
    
    return ud


# qtynan = np.nan * unitless


if __name__ == '__main__':
    # Dimension handles exponents
    # Quantity contains float and Dimension
    # Unit is (derived from) Quantity with symbol string and offset (pressure and temperature)
    # Quantity q1 = float * Unit
    # sq1 = q1.Format(Unit, fmt) returns string of Value formatted 
    # Unit u1 = value, offset, dimension, symbol
    # su1 = u1.Format(Unit, fmt) returns string of Value formatted

    def main():
        unitless = Unit(' ', Quantity.Create(1.0, Dimensionless))

        _dim = Length_dimension

        um    = Unit('m',    Quantity.Create(1.0, _dim))
        ucm   = Unit('cm',   um / 100.0)
        umm   = Unit('mm',   um / 1000.0)
        uKm   = Unit('Km',   um * 1000.0)
        uft   = Unit('ft',   um * 0.3048)
        uftUS = Unit('ftUS', Quantity.Create(0.304800609601, _dim))
        uinch = Unit('in',   uft / 12.0)
        umil  = Unit('mil',  Quantity.Create(0.0000254, _dim))
        umile = Unit('mi',   Quantity.Create(1609.344, _dim))
        umiUS = Unit('miUS', Quantity.Create(1609.34721869, _dim))
        unmi  = Unit('nmi',  Quantity.Create(1852.0, _dim))
        uyd   = Unit('yd',   uft * 3.0)

        d1 = 2.0 * uyd
        d9 = 3.0 * d1
        d2 = 36.0 * uinch
        d3 = d1 + d2
        a1 = d1.squared()
        v1 = d1 * d2 * d3
        
#        fu = d3.Value(uinch)
#        fu = 1.0 * fu

#        sss = f'd3 = {d3.Format(uinch, "0.2f")}'
#        print(sss)

        print(f'd3 = {d3.Format(uinch, "0.2f")}')
        print(f'd3 = {d3.Format(uft, "0.3f")}')
        print(f'd3 = {d3.Format(uyd, "0.4f")}')

        q1 = 3.0 / um.squared()
        print(q1)


    main()