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
_Duration = typing.Dict[str, typing.Union[int, decimal.Decimal]]

# Other Built-in Datatypes
_YearMonthDuration = _Duration
_DayTimeDuration = _Duration

###


def check_meets_condition(condition: bool, description: str, value: typing.Any) -> None:
	if not condition:
		raise TypeError("Not {}: {}".format(description, value))

def production(regex: str) -> str:
	return "(" + regex + ")"

def check_matches_production(p: str, s: str) -> None:
	if not re.fullmatch(p, s):
		raise TypeError("Does not match production '{}': '{}'".format(p, s))


###


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
# BUG: The spec has an erroneous extra parenthesis in its 'yearFrag' production.
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

# XSD 1.1, Part 2: 3.3.6.2 Lexical Mapping
duYearFrag = production(unsignedNoDecimalPtNumeral) + r"Y"
duMonthFrag = production(unsignedNoDecimalPtNumeral) + r"M"
duDayFrag = production(unsignedNoDecimalPtNumeral) + r"D"
duHourFrag = production(unsignedNoDecimalPtNumeral) + r"H"
duMinuteFrag = production(unsignedNoDecimalPtNumeral) + r"M"
duSecondFrag = r"(" + production(unsignedNoDecimalPtNumeral) + r"|" + production(unsignedDecimalPtNumeral) + r")S"
duYearMonthFrag = r"(" + production(duYearFrag) + production(duMonthFrag) + r"?)|" + production(duMonthFrag)
duTimeFrag = r"T((" + production(duHourFrag) + production(duMinuteFrag) + r"?" + production(duSecondFrag) + r"?)|(" + production(duMinuteFrag) + production(duSecondFrag) + r"?)|" + production(duSecondFrag) + r")"
duDayTimeFrag = r"(" + production(duDayFrag) + production(duTimeFrag) + r"?)|" + production(duTimeFrag)
durationLexicalRep = r"-?P((" + production(duYearMonthFrag) + production(duDayTimeFrag) + r"?)|" + production(duDayTimeFrag) + r")"

# [...]

# XSD 1.1, Part 2: 3.4.26.1 The yearMonthDuration Lexical Mapping
yearMonthDurationLexicalRep = r"-?P" + production(duYearMonthFrag)

# XSD 1.1, Part 2: 3.4.27.1 The dayTimeDuration Lexical Space
dayTimeDurationLexicalRep = r"-?P" + production(duDayTimeFrag)


###


#
# XSD 1.1, Part 2: E.1 Generic Number-related Functions
#

# Auxiliary Functions for Operating on Numeral Fragments

def _digitValue(d: str) -> int:
	check_matches_production(digit, d)

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
	else:  # pragma: no cover
		raise RuntimeError

	return value

def _digitSequenceValue(S: typing.Sequence[str]) -> int:
	for s in S:
		check_matches_production(digit, s)

	value = 0

	# NOTE: The spec uses 1-based indexing.
	for i in range(1, len(S) + 1):
		value += _digitValue(S[i-1]) * 10**(len(S) - i)

	return value

# BUG: The spec says this returns an integer.
def _fractionDigitSequenceValue(S: typing.Sequence[str]) -> decimal.Decimal:
	for s in S:
		check_matches_production(digit, s)

	value = decimal.Decimal()

	# NOTE: The spec uses 1-based indexing.
	# BUG: The spec subtracts the exponential and expects a non-negative integer result;
	#       this multiplies the exponential and expects a non-negative decimal number result.
	for i in range(1, len(S) + 1):
		value += decimal.Decimal(_digitValue(S[i-1]) * 10**-i)

	return value.quantize(decimal.Decimal(10) ** -len(S))

def _fractionFragValue(N: str) -> decimal.Decimal:
	check_matches_production(fracFrag, N)

	return _fractionDigitSequenceValue(N)

# Auxiliary Functions for Producing Numeral Fragments

def _digit(i : int) -> str:
	check_meets_condition(i in { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9 }, "between 0 and 9 inclusive", i)

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
	else:  # pragma: no cover
		raise RuntimeError

	return d

# NOTE: This is a generator because the spec expects it to be infinite.
def _digitRemainderSeq(i: int) -> typing.Iterator[int]:
	check_meets_condition(isinstance(i, int) and i >= 0, "a nonnegative integer", i)

	while True:
		yield i
		i = i // 10

# NOTE: This is a generator because the spec expects it to be infinite.
def _digitSeq(i: int) -> typing.Iterator[int]:
	check_meets_condition(isinstance(i, int) and i >= 0, "a nonnegative integer", i)

	for k in _digitRemainderSeq(i):  # pragma: no branch
		yield k % 10

def _lastSignificantDigit(s: typing.Iterator[int]) -> int:
	for j, k in enumerate(s):
		if k == 0:
			return j - 1 if j > 0 else 0

		j += 1

# BUG: The spec inexplicably capitalizes the first letter of this function.
# NOTE: This is a generator because the spec expects it to be infinite.
# BUG: The spec says subtract when it means multiply.
def _fractionDigitRemainderSeq(f: decimal.Decimal) -> typing.Iterator[decimal.Decimal]:
	check_meets_condition(isinstance(f, decimal.Decimal) and f >= 0 and f < 1, "a nonnegative decimal number less than 1", f)

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

	stop = _lastSignificantDigit(_fractionDigitRemainderSeq(f))

	for j, k in enumerate(_fractionDigitSeq(f)):  # pragma: no branch
		output += _digit(k)

		if j == stop:
			break

	return output

# Auxiliary Functions for Binary Floating-point Lexical/Canonical Mappings

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

# BUG: The spec passes int 'c' to a function expecting decimal 'n'.
def _floatApprox(c: int, e: int, j: int) -> decimal.Decimal:
	return _round(decimal.Decimal(c), j).scaleb(e)

#
# XSD 1.1, Part 2: E.2 Duration-related Definitions
#

# BUG: The spec says "followed by" when it means "preceded by".
def _duYearFragmentMap(Y: str) -> int:
	m = re.fullmatch(duYearFrag, Y)

	N = m.group(1)

	return noDecimalMap(N)

# BUG: The spec says "followed by" when it means "preceded by".
def _duMonthFragmentMap(M: str) -> int:
	m = re.fullmatch(duMonthFrag, M)

	N = m.group(1)

	return noDecimalMap(N)

# BUG: The spec says "followed by" when it means "preceded by".
def _duDayFragmentMap(D: str) -> int:
	m = re.fullmatch(duDayFrag, D)

	N = m.group(1)

	return noDecimalMap(N)

# BUG: The spec says "followed by" when it means "preceded by".
def _duHourFragmentMap(H: str) -> int:
	m = re.fullmatch(duHourFrag, H)

	N = m.group(1)

	return noDecimalMap(N)

# BUG: The spec says "followed by" when it means "preceded by".
def _duMinuteFragmentMap(M: str) -> int:
	m = re.fullmatch(duMinuteFrag, M)

	N = m.group(1)

	return noDecimalMap(N)

# BUG: The spec says "followed by" when it means "preceded by".
def _duSecondFragmentMap(S: str) -> decimal.Decimal:
	m = re.fullmatch(duSecondFrag, S)

	N = m.group(1)

	if m.group(4) is not None:
		return decimalPtMap(N)

	return decimal.Decimal(noDecimalMap(N))

def _duYearMonthFragmentMap(YM: str) -> int:
	m = re.fullmatch(duYearMonthFrag, YM)

	y = _duYearFragmentMap(m.group(2)) if m.group(2) is not None else 0
	mi = _duMonthFragmentMap(m.group(5)) if m.group(5) is not None else _duMonthFragmentMap(m.group(8)) if m.group(8) is not None else 0

	return 12 * y + mi

def _duTimeFragmentMap(T: str) -> decimal.Decimal:
	m = re.fullmatch(duTimeFrag, T)

	# BUG: The spec says 'duDayFragmentMap' when it means 'duHourFragmentMap'.
	h = _duHourFragmentMap(m.group(3)) if m.group(3) is not None else 0
	mi = _duMinuteFragmentMap(m.group(6)) if m.group(6) is not None else _duMinuteFragmentMap(m.group(23)) if m.group(23) is not None else 0
	s = _duSecondFragmentMap(m.group(9)) if m.group(9) is not None else _duSecondFragmentMap(m.group(26)) if m.group(26) is not None else _duSecondFragmentMap(m.group(39)) if m.group(39) is not None else decimal.Decimal(0)

	return decimal.Decimal(3600 * h + 60 * mi + s)

def _duDayTimeFragmentMap(DT: str) -> decimal.Decimal:
	m = re.fullmatch(duDayTimeFrag, DT)

	d = _duDayFragmentMap(m.group(2)) if m.group(2) is not None else 0
	t = _duTimeFragmentMap(m.group(5)) if m.group(5) is not None else _duTimeFragmentMap(m.group(57)) if m.group(57) is not None else decimal.Decimal(0)

	return decimal.Decimal(86400 * d + t)

# XXX: This could be DRYed.
def _duYearMonthCanonicalFragmentMap(ym: int) -> str:
	y = ym // 12
	m = ym % 12

	if y != 0 and m != 0:
		return unsignedNoDecimalPtCanonicalMap(y) + "Y" + unsignedNoDecimalPtCanonicalMap(m) + "M"

	if y != 0 and m == 0:
		return unsignedNoDecimalPtCanonicalMap(y) + "Y"

	if y == 0:
		return unsignedNoDecimalPtCanonicalMap(m) + "M"

def _duDayCanonicalFragmentMap(d: int) -> str:
	return unsignedNoDecimalPtCanonicalMap(d) + "D" if d != 0 else ""

def _duHourCanonicalFragmentMap(h: int) -> str:
	return unsignedNoDecimalPtCanonicalMap(h) + "H" if h != 0 else ""

def _duMinuteCanonicalFragmentMap(m: int) -> str:
	return unsignedNoDecimalPtCanonicalMap(m) + "M" if m != 0 else ""

def _duSecondCanonicalFragmentMap(s: decimal.Decimal) -> str:
	s_is_int = True if s == s.to_integral_value() else False

	return unsignedNoDecimalPtCanonicalMap(int(s)) + "S" if s_is_int and s != 0 else unsignedDecimalPtCanonicalMap(s) + "S" if not s_is_int else ""

def _duTimeCanonicalFragmentMap(h: int, m: int, s: decimal.Decimal) -> str:
	return "T" + _duHourCanonicalFragmentMap(h) + _duMinuteCanonicalFragmentMap(m) + _duSecondCanonicalFragmentMap(s) if h != 0 or m != 0 or s != 0 else ""

def _duDayTimeCanonicalFragmentMap(ss: decimal.Decimal) -> str:
	d = int(ss // 86400)
	h = int((ss % 86400) // 3600)
	m = int((ss % 3600) // 60)
	s = ss % 60

	return _duDayCanonicalFragmentMap(d) + _duTimeCanonicalFragmentMap(h, m, s) if ss != 0 else "T0S"

# [...]


###


#
# XSD 1.1, Part 2: E.1 Generic Number-related Functions
#

# Generic Numeral-to-Number Lexical Mappings

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

	# BUG: The spec remaps the sign from 'scientificMap' onto 'unsignedNoDecimalPtNumeral' and 'unsignedDecimalPtNumeral'
	#       to make them 'noDecimalPtNumeral' and 'decimalPtNumeral', which doesn't really work.
	# BUG: The spec says 'unsignedDecimalPtMap' when it means 'noDecimalMap'.
	if m.group(6) is not None:
		value = unsignedDecimalPtMap(C) * decimal.Decimal(10)**noDecimalMap(E)
	else:
		value = unsignedNoDecimalMap(C) * decimal.Decimal(10)**noDecimalMap(E)

	return decimal.Decimal(sign * value)

# Generic Number to Numeral Canonical Mappings

def unsignedNoDecimalPtCanonicalMap(i: int) -> str:
	canonical_representation = ""

	for j, d in enumerate(_digitSeq(i)):
		canonical_representation = _digit(d) + canonical_representation

		# BUG: The spec says 'digitRemainderSeq' when it means 'digitSeq'.
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
	# BUG: The spec doesn't handle the possibility of n = 0, even though n is "nonnegative".
	if n == 0:
		return unsignedDecimalPtCanonicalMap(decimal.Decimal(0)) + "E" + noDecimalPtCanonicalMap(0)

	return unsignedDecimalPtCanonicalMap(n / decimal.Decimal(10**decimal.Decimal(math.log10(n) // 1))) + "E" + noDecimalPtCanonicalMap(int(math.log10(n) // 1))

def scientificCanonicalMap(n: decimal.Decimal) -> str:
	if n < 0:
		return "-" + unsignedScientificCanonicalMap(-n)

	return unsignedScientificCanonicalMap(n)

# Lexical Mapping for Non-numerical 'Special Values' Used With Numerical Datatypes

def specialRepValue(S: str) -> decimal.Decimal:
	if S in { "INF", "+INF" }:
		return decimal.Decimal(math.inf)

	if S == "-INF":
		return decimal.Decimal(-math.inf)

	if S == "NaN":
		return decimal.Decimal(math.nan)

# Canonical Mapping for Non-numerical 'Special Values' Used with Numerical Datatypes

def specialRepCanonicalMap(c: decimal.Decimal) -> str:
	if c == decimal.Decimal(math.inf):
		return "INF"

	if c == decimal.Decimal(-math.inf):
		return "-INF"

	if math.isnan(c):
		return "NaN"

# Lexical Mapping

def decimalLexicalMap(LEX: str) -> _Decimal:
	m = re.fullmatch(decimalLexicalRep, LEX)

	if m.group(12) is not None:
		d = decimal.Decimal(noDecimalMap(LEX))
	else:
		d = decimalPtMap(LEX)

	return d.quantize(decimal.Decimal(10) ** -(len(m.group(7)) if m.group(7) is not None else 0))

# Canonical Mapping

def decimalCanonicalMap(d: _Decimal) -> str:
	if d == d.to_integral_value():
		return noDecimalPtCanonicalMap(int(d))

	return decimalPtCanonicalMap(d)

# Lexical Mapping

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

# Lexical Mapping

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

# Canonical Mapping

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

# Canonical Mapping

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

#

def durationMap(DUR: str) -> _Duration:
	m = re.fullmatch(durationLexicalRep, DUR)

	# NOTE: The spec doesn't use a capture group for the sign.
	sign = -1 if DUR[0] == "-" else 1

	months = sign * _duYearMonthFragmentMap(m.group(3)) if m.group(3) is not None else 0
	seconds = sign * _duDayTimeFragmentMap(m.group(14)) if m.group(14) is not None else sign * _duDayTimeFragmentMap(m.group(123)) if m.group(123) is not None else decimal.Decimal(0)

	return { "months": months, "seconds": seconds }

def yearMonthDurationMap(YM: str) -> _YearMonthDuration:
	m = re.fullmatch(yearMonthDurationLexicalRep, YM)

	# NOTE: The spec doesn't use a capture group for the sign.
	sign = -1 if YM[0] == "-" else 1

	months = sign * _duYearMonthFragmentMap(m.group(1))
	seconds = decimal.Decimal(0)

	return { "months": months, "seconds": seconds }

# BUG: The spec says "a dayTimeDuration value" when it means "matches dayTimeDurationLexicalRep".
def dayTimeDurationMap(DT: str) -> _DayTimeDuration:
	m = re.fullmatch(dayTimeDurationLexicalRep, DT)

	# NOTE: The spec doesn't use a capture group for the sign.
	sign = -1 if DT[0] == "-" else 1

	print(m.re)
	print(list(enumerate(m.groups(), start=1)))

	months = 0
	seconds = sign * _duDayTimeFragmentMap(m.group(1))

	return { "months": months, "seconds": seconds }

def durationCanonicalMap(v: _Duration) -> str:
	m = v["months"]
	s = v["seconds"]
	sgn = "-" if m < 0 or s < 0 else ""

	if m != 0 and s != 0:
		return sgn + "P" + _duYearMonthCanonicalFragmentMap(int(abs(m))) + _duDayTimeCanonicalFragmentMap(s.copy_abs())

	if m != 0 and s == 0:
		return sgn + "P" + _duYearMonthCanonicalFragmentMap(int(abs(m)))

	if m == 0:
		return sgn + "P" + _duDayTimeCanonicalFragmentMap(s.copy_abs())


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
	def lexical_representation(self) -> str:
		return self._lexical_representation

	@lexical_representation.setter
	def lexical_representation(self, literal: str) -> None:
		if not self.in_lexical_space(literal):
			raise TypeError("Literal not in lexical space: {}".format(literal))

		self._lexical_representation = literal

	@property
	def value(self) -> typing.Any:
		return self.lexical_mapping(self.lexical_representation)

	@property
	def canonical_representation(self) -> str:
		return self.canonical_mapping(self.value)

	@classmethod
	@abc.abstractmethod
	def in_lexical_space(cls, literal: str) -> bool:
		raise NotImplementedError

	@classmethod
	@abc.abstractmethod
	def lexical_mapping(cls, lexical_representation: str) -> typing.Any:
		raise NotImplementedError

	@classmethod
	@abc.abstractmethod
	def canonical_mapping(cls, value: typing.Any) -> str:
		raise NotImplementedError


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

# XSD 1.1, Part 2: 3.3.6 duration
class Duration(PrimitiveDatatype):
	@classmethod
	def in_lexical_space(cls, literal: str) -> bool:
		return bool(re.fullmatch(durationLexicalRep, literal))

	@classmethod
	def lexical_mapping(cls, lexical_representation: str) -> _Duration:
		assert cls.in_lexical_space(lexical_representation)

		return durationMap(lexical_representation)

	@classmethod
	def canonical_mapping(cls, value: _Duration) -> str:
		return durationCanonicalMap(value)






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


