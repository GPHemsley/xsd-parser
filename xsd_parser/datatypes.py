#!/usr/bin/env python3

import re
import math
import decimal
import itertools
import typing
import abc

###

#
# Internal type representations
#

# Primitive Datatypes
_String = str
_Boolean = bool
_Decimal = decimal.Decimal
_Float = decimal.Decimal
_Double = decimal.Decimal

###


def production(regex : str) -> str:
	return "(" + regex + ")"

# XSD 1.1, Part 2: D.1.1 Exact Lexical Mappings
digit = r"[0-9]"
unsignedNoDecimalPtNumeral = production(digit) + r"+"
noDecimalPtNumeral = r"(\+|-)?" + production(unsignedNoDecimalPtNumeral)
fracFrag = production(digit) + r"+"
unsignedDecimalPtNumeral = r"(" + production(unsignedNoDecimalPtNumeral) + r"\." + production(fracFrag) + r"?)|(\." + production(fracFrag) + r")"
unsignedFullDecimalPtNumeral = production(unsignedNoDecimalPtNumeral) + r"\." + production(fracFrag)
decimalPtNumeral = r"(\+|-)?" + production(unsignedDecimalPtNumeral)
unsignedScientificNotationNumeral = r"(" + production(unsignedNoDecimalPtNumeral) + r"|" + production(unsignedDecimalPtNumeral) + r")(e|E)" + production(noDecimalPtNumeral)
scientificNotationNumeral = r"(\+|-)?" + production(unsignedScientificNotationNumeral)
minimalNumericalSpecialRep = r"INF|-INF|NaN"
numericalSpecialRep = r"\+INF|" + production(minimalNumericalSpecialRep)

# XSD 1.1, Part 2: D.2.2 Lexical Mappings
# NOTE: The spec has an erroneous extra parenthesis in its 'yearFrag' production.
yearFrag = r"-?(([1-9]" + production(digit) + production(digit) + production(digit) + r"+)|(0" + production(digit) + production(digit) + production(digit) + r"))"
monthFrag = r"(0[1-9])|(1[0-2])"
dayFrag = r"(0[1-9])|([12]" + production(digit) + r")|(3[01])"
hourFrag = r"([01]" + production(digit) + r")|(2[0-3])"
minuteFrag = r"[0-5]" + production(digit)
secondFrag = r"([0-5]" + production(digit) + r")(\." + production(digit) + r"+)?"
endOfDayFrag = r"24:00:00(\.0+)?"
timezoneFrag = r"Z|(\+|-)((0" + production(digit) + r"|1[0-3]):" + production(minuteFrag) + r"|14:00)"

# [...]

# XSD 1.1, Part 2: 3.3.1.2 Lexical Mapping
stringRep = r"[\u0001-\uD7FF\uE000-\uFFFD\U00010000-\U0010FFFF]*"

# XSD 1.1, Part 2: 3.3.2.2 Lexical Mapping
booleanRep = r"true|false|1|0"

# XSD 1.1, Part 2: 3.3.3.1 Lexical Mapping
decimalLexicalRep = production(decimalPtNumeral) + r"|" + production(noDecimalPtNumeral)

# XSD 1.1, Part 2: 3.3.4.2 Lexical Mapping
floatRep = production(noDecimalPtNumeral) + r"|" + production(decimalPtNumeral) + r"|" + production(scientificNotationNumeral) + r"|" + production(numericalSpecialRep)

# XSD 1.1, Part 2: 3.3.5.2 Lexical Mapping
doubleRep = production(noDecimalPtNumeral) + r"|" + production(decimalPtNumeral) + r"|" + production(scientificNotationNumeral) + r"|" + production(numericalSpecialRep)

###


#
# XSD 1.1, Part 2: E.1 Generic Number-related Functions
#

def _digitValue(d: str) -> int:
	if d == "0":
		value = 0
	elif d == "1":
		value = 1
	elif d == "2":
		value = 2
	elif d == "3":
		value = 3
	elif d == "4":
		value = 4
	elif d == "5":
		value = 5
	elif d == "6":
		value = 6
	elif d == "7":
		value = 7
	elif d == "8":
		value = 8
	elif d == "9":
		value = 9
	else:
		value = None

	return value

def _digitSequenceValue(S: str) -> int:
	value = 0

	# NOTE: The spec uses 1-based indexing.
	for i in range(1, len(S) + 1):
		value += _digitValue(S[i-1]) * 10**(len(S) - i)

	return value

# NOTE: The spec says this returns an integer.
def _fractionDigitSequenceValue(S: str) -> decimal.Decimal:
	value = decimal.Decimal()

	# NOTE: The spec uses 1-based indexing.
	# NOTE: The spec subtracts the exponential and expects a non-negative integer result;
	#       this multiplies the exponential and expects a non-negative decimal number result.
	for i in range(1, len(S) + 1):
		value += decimal.Decimal(_digitValue(S[i-1]) * 10**-i)

	return value.quantize(decimal.Decimal(10) ** -len(S))

def _fractionFragValue(N: str) -> decimal.Decimal:
	return _fractionDigitSequenceValue(N)

def _digit(i : int) -> str:
	if i == 0:
		d = "0"
	elif i == 1:
		d = "1"
	elif i == 2:
		d = "2"
	elif i == 3:
		d = "3"
	elif i == 4:
		d = "4"
	elif i == 5:
		d = "5"
	elif i == 6:
		d = "6"
	elif i == 7:
		d = "7"
	elif i == 8:
		d = "8"
	elif i == 9:
		d = "9"
	else:
		d = None

	return d

# NOTE: This is a generator because the spec expects it to be infinite.
def _digitRemainderSeq(i: int) -> typing.Iterator[int]:
	while True:
		yield i
		i = i // 10

# NOTE: This is a generator because the spec expects it to be infinite.
def _digitSeq(i: int) -> typing.Iterator[int]:
	for k in _digitRemainderSeq(i):
		yield k % 10

def _lastSignificantDigit(s: typing.Iterator[int]) -> int:
	for j, k in enumerate(s):
		if k == 0:
			return j - 1 if j > 0 else 0

		j += 1

# NOTE: The spec inexplicably capitalizes the first letter of this function.
# NOTE: This is a generator because the spec expects it to be infinite.
# NOTE: The spec says subtract when it means multiply.
def _fractionDigitRemainderSeq(f: decimal.Decimal) -> typing.Iterator[decimal.Decimal]:
	k = f * 10

	while True:
		yield k

		k = (k % 1) * 10

# NOTE: This is a generator because the spec expects it to be infinite.
def _fractionDigitSeq(f: decimal.Decimal) -> typing.Iterator[int]:
	for k in _fractionDigitRemainderSeq(f):
		yield int(k // 1)

def _fractionDigitsCanonicalFragmentMap(f: decimal.Decimal) -> str:
	output = ""
	# NOTE: The spec says 'fractionDigitRemainderSeq' when it means 'fractionDigitSeq'.
	stop = _lastSignificantDigit(_fractionDigitSeq(f))

	for j, k in enumerate(_fractionDigitSeq(f)):
		output += _digit(k)

		if j == stop:
			break

	return output

# NOTE: The spec uses inequalities to define variables relative to 'nV'.
# XXX: This could be DRYed.
def _floatingPointRound(nV: decimal.Decimal, cWidth: int, eMin: int, eMax: int) -> decimal.Decimal:
	s = -1 if nV < 0 else 1

	e = math.ceil(math.log2(abs(nV))) - cWidth
	c = math.ceil(abs(nV) / decimal.Decimal(2**e))

	if eMax < e:
		if s > 0:
			return decimal.Decimal(math.inf)

		return decimal.Decimal(-math.inf)

	if e < eMin:
		e = eMin
		c = math.ceil(abs(nV) / decimal.Decimal(2**e))

	if abs(nV) > c * 2**e - 2**(e-1):
		nV = c * 2**e
	elif abs(nV) < c * 2**e - 2**(e-1):
		nV = (c - 1) * 2**e
	else:
		nV = c * 2**e if c % 2 == 0 else (c - 1) * 2**e

	if nV < 2**cWidth * 2**eMax:
		return decimal.Decimal(str(s * nV))

	if s > 0:
		return decimal.Decimal(math.inf)

	return decimal.Decimal(-math.inf)

def _round(n: decimal.Decimal, k: int) -> decimal.Decimal:
	return (((n / 10**k) + decimal.Decimal(0.5)) // 1) * 10**k

# NOTE: The spec passes int 'c' to a function expecting decimal 'n'.
def _floatApprox(c: int, e: int, j: int) -> decimal.Decimal:
	return _round(decimal.Decimal(c), j).scaleb(e)

# [...]


###


#
# XSD 1.1, Part 2: E.1 Generic Number-related Functions
#

def unsignedNoDecimalMap(N: str) -> int:
	return _digitSequenceValue(N)

def noDecimalMap(N: str) -> int:
	m = re.fullmatch(noDecimalPtNumeral, N)

	sign = m.group(1)
	U = m.group(2)

	if sign == "-":
		return -1 * unsignedNoDecimalMap(U)

	return unsignedNoDecimalMap(U)

def unsignedDecimalPtMap(D: str) -> decimal.Decimal:
	m = re.fullmatch(unsignedDecimalPtNumeral, D)

	N = m.group(2)
	F = m.group(4) if m.group(4) is not None else m.group(7)

	if F is None:
		value = decimal.Decimal(unsignedNoDecimalMap(N))
	elif N is None:
		value = _fractionFragValue(F)
	else:
		value = decimal.Decimal(unsignedNoDecimalMap(N)) + _fractionFragValue(F)

	return value.quantize(decimal.Decimal(10) ** -(len(F) if F is not None else 0))

def decimalPtMap(N: str) -> decimal.Decimal:
	m = re.fullmatch(decimalPtNumeral, N)

	sign = m.group(1)
	U = m.group(2)

	if sign == "-":
		return -unsignedDecimalPtMap(U)

	return unsignedDecimalPtMap(U)

def scientificMap(N: str) -> decimal.Decimal:
	m = re.fullmatch(scientificNotationNumeral, N)

	sign = -1 if m.group(1) is not None else +1
	C = m.group(3)
	E = m.group(16)

	# NOTE: The spec remaps the sign from 'scientificMap' onto 'unsignedNoDecimalPtNumeral' and 'unsignedDecimalPtNumeral'
	#       to make them 'noDecimalPtNumeral' and 'decimalPtNumeral', which doesn't really work.
	# NOTE: The spec says 'unsignedDecimalPtMap' when it means 'noDecimalMap'.
	if m.group(6) is not None:
		value = unsignedDecimalPtMap(C) * decimal.Decimal(10)**noDecimalMap(E)
	else:
		value = unsignedNoDecimalMap(C) * decimal.Decimal(10)**noDecimalMap(E)

	return decimal.Decimal(sign * value)

def unsignedNoDecimalPtCanonicalMap(i: int) -> str:
	canonical_representation = ""

	for j, d in enumerate(_digitSeq(i)):
		canonical_representation = _digit(d) + canonical_representation

		# NOTE: The spec says 'digitRemainderSeq' when it means 'digitSeq'.
		if j == _lastSignificantDigit(_digitSeq(i)):
			break

	return canonical_representation

def noDecimalPtCanonicalMap(i: int) -> str:
	if i < 0:
		return "-" + unsignedNoDecimalPtCanonicalMap(-i)

	return unsignedNoDecimalPtCanonicalMap(i)

def unsignedDecimalPtCanonicalMap(n: decimal.Decimal) -> str:
	return unsignedNoDecimalPtCanonicalMap(int(n // 1)) + "." + _fractionDigitsCanonicalFragmentMap(n % 1)

def decimalPtCanonicalMap(i: decimal.Decimal) -> str:
	if i < 0:
		return "-" + unsignedDecimalPtCanonicalMap(-i)

	return unsignedDecimalPtCanonicalMap(i)

def unsignedScientificCanonicalMap(n: decimal.Decimal) -> str:
	# NOTE: The spec doesn't handle the possibility of n = 0, even though n is "nonnegative".
	if n == 0:
		return unsignedDecimalPtCanonicalMap(decimal.Decimal(0)) + "E" + noDecimalPtCanonicalMap(0)

	return unsignedDecimalPtCanonicalMap(n / decimal.Decimal(10**decimal.Decimal(math.log10(n) // 1))) + "E" + noDecimalPtCanonicalMap(int(math.log10(n) // 1))

def scientificCanonicalMap(n: decimal.Decimal) -> str:
	if n < 0:
		return "-" + unsignedScientificCanonicalMap(-n)

	return unsignedScientificCanonicalMap(n)

def specialRepValue(S: str) -> decimal.Decimal:
	if S in { "INF", "+INF" }:
		return decimal.Decimal(math.inf)

	if S == "-INF":
		return decimal.Decimal(-math.inf)

	if S == "NaN":
		return decimal.Decimal(math.nan)

def specialRepCanonicalMap(c: decimal.Decimal) -> str:
	if c == decimal.Decimal(math.inf):
		return "INF"

	if c == decimal.Decimal(-math.inf):
		return "-INF"

	if math.isnan(c):
		return "NaN"

def decimalLexicalMap(LEX: str) -> _Decimal:
	m = re.fullmatch(decimalLexicalRep, LEX)

	if m.group(12) is not None:
		d = decimal.Decimal(noDecimalMap(LEX))
	else:
		d = decimalPtMap(LEX)

	return d.quantize(decimal.Decimal(10) ** -(len(m.group(7)) if m.group(7) is not None else 0))

def decimalCanonicalMap(d: _Decimal) -> str:
	if d == d.to_integral_value():
		return noDecimalPtCanonicalMap(int(d))

	return decimalPtCanonicalMap(d)

def floatLexicalMap(LEX: str) -> _Float:
	m = re.fullmatch(floatRep, LEX)

	if m.group(36) is not None:
		return specialRepValue(LEX)

	if m.group(1) is not None:
		nV = decimal.Decimal(noDecimalMap(LEX))
	elif m.group(5) is not None:
		nV = decimalPtMap(LEX)
	else:
		nV = scientificMap(LEX)

	if nV != 0:
		nV = _floatingPointRound(nV, 24, -149, 104)

	if nV == 0:
		return decimal.Decimal("-0") if LEX[0] == "-" else decimal.Decimal("0")

	return decimal.Decimal(nV)

def doubleLexicalMap(LEX: str) -> _Double:
	m = re.fullmatch(doubleRep, LEX)

	if m.group(36) is not None:
		return specialRepValue(LEX)

	if m.group(1) is not None:
		nV = decimal.Decimal(noDecimalMap(LEX))
	elif m.group(5) is not None:
		nV = decimalPtMap(LEX)
	else:
		nV = scientificMap(LEX)

	if nV != 0:
		nV = _floatingPointRound(nV, 53, -1074, 971)

	if nV == 0:
		return decimal.Decimal("-0") if LEX[0] == "-" else decimal.Decimal("0")

	return decimal.Decimal(nV)

def floatCanonicalMap(f: _Float) -> str:
	if math.isinf(f) or math.isnan(f):
		return specialRepCanonicalMap(f)

	if f.number_class() == "+Zero":
		return "0.0E0"

	if f.number_class() == "-Zero":
		return "-0.0E0"

	s = -1 if f < 0 else 1

	f_tuple = f.normalize().as_tuple()

	c = int("".join(str(x) for x in f_tuple.digits))
	e = f_tuple.exponent

	print(f, s, c, e)

	# XXX: When is 'l' not 0?
	l = 0

	# XXX: This assumes that any intervening zero is insignificant. Is that what we want to happen?
	return scientificCanonicalMap(s * _floatApprox(c, e, l))

def doubleCanonicalMap(f: _Double) -> str:
	if math.isinf(f) or math.isnan(f):
		return specialRepCanonicalMap(f)

	if f.number_class() == "+Zero":
		return "0.0E0"

	if f.number_class() == "-Zero":
		return "-0.0E0"

	s = -1 if f < 0 else 1

	f_tuple = f.normalize().as_tuple()

	c = int("".join(str(x) for x in f_tuple.digits))
	e = f_tuple.exponent

	print(f, s, c, e)

	# XXX: When is 'l' not 0?
	l = 0

	# XXX: This assumes that any intervening zero is insignificant. Is that what we want to happen?
	return scientificCanonicalMap(s * _floatApprox(c, e, l))




# [...]


# XSD 1.1, Part 2: E.4 Lexical and Canonical Mappings for Other Datatypes
def stringLexicalMap(LEX: str) -> _String:
	return LEX

def booleanLexicalMap(LEX: str) -> _Boolean:
	return True if LEX in { "true", "1" } else False

def stringCanonicalMap(s: _String) -> str:
	return s

def booleanCanonicalMap(b: _Boolean) -> str:
	return "true" if b else "false"


###


class Datatype(metaclass=abc.ABCMeta):
	def __init__(self, literal: str) -> None:
		self.lexical_representation = literal

	def __repr__(self) -> str:
		return "{}({})".format(self.__class__.__name__, repr(self.lexical_representation))

	@property
	def lexical_representation(self):
		return self._lexical_representation

	@lexical_representation.setter
	def lexical_representation(self, literal: str) -> None:
		if not self.in_lexical_space(literal):
			raise TypeError("Literal not in lexical space: {}".format(literal))

		self._lexical_representation = literal

	@property
	def value(self):
		return self.lexical_mapping(self.lexical_representation)

	@property
	def canonical_representation(self):
		return self.canonical_mapping(self.value)

	@classmethod
	@abc.abstractmethod
	def in_lexical_space(cls, literal: str) -> bool:
		raise NotImplementedError()

	@classmethod
	@abc.abstractmethod
	def lexical_mapping(cls, lexical_representation: str) -> typing.Any:
		raise NotImplementedError()

	@classmethod
	@abc.abstractmethod
	def canonical_mapping(cls, value: typing.Any) -> str:
		raise NotImplementedError()


class SpecialDatatype(Datatype):
	pass


class PrimitiveDatatype(Datatype):
	pass


class OrdinaryDatatype(Datatype):
	pass


###


# XSD 1.1, Part 2: 3.3.1 string
class String(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(stringRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _String:
		assert cls.in_lexical_space(lexical_representation)

		return stringLexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _String) -> str:
		return stringCanonicalMap(value)


# XSD 1.1, Part 2: 3.3.2 boolean
class Boolean(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(booleanRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _Boolean:
		assert cls.in_lexical_space(lexical_representation)

		return booleanLexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _Boolean) -> str:
		return booleanCanonicalMap(value)


# XSD 1.1, Part 2: 3.3.3 decimal
class Decimal(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(decimalLexicalRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _Decimal:
		assert cls.in_lexical_space(lexical_representation)

		return decimalLexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _Decimal) -> str:
		return decimalCanonicalMap(value)


# XSD 1.1, Part 2: 3.3.4 float
class Float(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(floatRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _Float:
		assert cls.in_lexical_space(lexical_representation)

		return floatLexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _Float) -> str:
		return floatCanonicalMap(value)


# XSD 1.1, Part 2: 3.3.5 double
class Double(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(floatRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _Double:
		assert cls.in_lexical_space(lexical_representation)

		return doubleLexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _Double) -> str:
		return doubleCanonicalMap(value)





# XSD 1.1, Part 2:
class _____(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch("", literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> None:
		assert cls.in_lexical_space(lexical_representation)

		return _____LexicalMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: None) -> str:
		return _____CanonicalMap(value)


