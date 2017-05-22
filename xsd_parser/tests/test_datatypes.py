#!/usr/bin/env python3

import decimal
import itertools
import typing
import unittest
import unittest.mock

from ..datatypes import (
	_digitValue,
	_digitSequenceValue,
	_fractionDigitSequenceValue,
	_fractionFragValue,
	_digit,
	_digitRemainderSeq,
	_digitSeq,
	_lastSignificantDigit,
	_fractionDigitRemainderSeq,
	_fractionDigitSeq,
	_fractionDigitsCanonicalFragmentMap,
)
from ..datatypes import *

class TestDatatypesHelpers(unittest.TestCase):

	def test_check_meets_condition(self) -> None:
		with self.subTest():
			self.assertIsNone(check_meets_condition(True, "always true", True))

		with self.subTest():
			with self.assertRaises(TypeError):
				check_meets_condition(False, "always false", False)

	def test_production(self) -> None:
		with self.subTest():
			self.assertEqual(production("foo"), "(foo)")

		with self.subTest():
			with self.assertRaises(TypeError):
				production(False)

	def test_check_matches_production(self) -> None:
		with self.subTest():
			self.assertIsNone(check_matches_production(production("foo"), "foo"))

		with self.subTest():
			with self.assertRaises(TypeError):
				check_matches_production(production("bar"), "foo")


class TestDatatypesAuxiliaryFunctions(unittest.TestCase):

	def test__digitValue(self) -> None:
		valid_inputs = [
			("0", 0),
			("1", 1),
			("2", 2),
			("3", 3),
			("4", 4),
			("5", 5),
			("6", 6),
			("7", 7),
			("8", 8),
			("9", 9),
		]

		invalid_inputs = [
			"10",
			"1.1",
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (s, i) in valid_inputs:
			with self.subTest(s=s, i=i):
				self.assertEqual(_digitValue(s), i)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_digitValue(s)

	def test__digitSequenceValue(self) -> None:
		valid_inputs = [
			("", 0),
			("0", 0),
			("1", 1),
			("123", 123),
			("0123", 123),
			("1230", 1230),
			("01230", 1230),
			(["1", "2", "3"], 123),
		]

		invalid_inputs = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
			[1, 2, 3],
		]

		# Test valid inputs have valid outputs.
		for (seq, i) in valid_inputs:
			with self.subTest(seq=seq, i=i):
				self.assertEqual(_digitSequenceValue(seq), i)

		# Test invalid inputs raise TypeError.
		for seq in invalid_inputs:
			with self.subTest(seq=seq):
				with self.assertRaises(TypeError):
					_digitSequenceValue(seq)

	def test__fractionDigitSequenceValue(self) -> None:
		valid_inputs = [
			("", decimal.Decimal("0")),
			("0", decimal.Decimal("0.0")),
			("1", decimal.Decimal("0.1")),
			("123", decimal.Decimal("0.123")),
			("0123", decimal.Decimal("0.0123")),
			("1230", decimal.Decimal("0.1230")),
			("01230", decimal.Decimal("0.01230")),
			(["1", "2", "3"], decimal.Decimal("0.123")),
		]

		invalid_inputs = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
			[1, 2, 3],
		]

		# Test valid inputs have valid outputs.
		for (seq, d) in valid_inputs:
			with self.subTest(seq=seq, d=d):
				self.assertEqual(_fractionDigitSequenceValue(seq), d)

		# Test invalid inputs raise TypeError.
		for seq in invalid_inputs:
			with self.subTest(seq=seq):
				with self.assertRaises(TypeError):
					_fractionDigitSequenceValue(seq)

	def test__fractionFragValue(self) -> None:
		valid_inputs = [
			("0", decimal.Decimal("0.0")),
			("1", decimal.Decimal("0.1")),
			("123", decimal.Decimal("0.123")),
			("0123", decimal.Decimal("0.0123")),
			("1230", decimal.Decimal("0.1230")),
			("01230", decimal.Decimal("0.01230")),
		]

		invalid_inputs = [
			"",
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid inputs have valid outputs.
		for (s, d) in valid_inputs:
			with self.subTest(s=s, d=d):
				self.assertEqual(_fractionFragValue(s), d)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_fractionFragValue(s)

	def test__digit(self) -> None:
		valid_inputs = [
			(0, "0"),
			(1, "1"),
			(2, "2"),
			(3, "3"),
			(4, "4"),
			(5, "5"),
			(6, "6"),
			(7, "7"),
			(8, "8"),
			(9, "9"),
		]

		invalid_inputs = [
			10,
			1.1,
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (i, s) in valid_inputs:
			with self.subTest(i=i, s=s):
				self.assertEqual(_digit(i), s)

		# Test invalid inputs raise TypeError.
		for i in invalid_inputs:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					_digit(i)

	def test__digitRemainderSeq(self) -> None:
		valid_inputs = [
			(123, 5, [123, 12, 1, 0, 0]),
			(0, 10, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(1, 3, [1, 0, 0]),
			(2, 3, [2, 0, 0]),
			(3, 3, [3, 0, 0]),
			(4, 3, [4, 0, 0]),
			(5, 3, [5, 0, 0]),
			(6, 3, [6, 0, 0]),
			(7, 3, [7, 0, 0]),
			(8, 3, [8, 0, 0]),
			(9, 3, [9, 0, 0]),
			(1023, 6, [1023, 102, 10, 1, 0, 0]),
			(1230, 6, [1230, 123, 12, 1, 0, 0]),
		]

		invalid_inputs = [
			-1,
			1.1,
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (i, n, seq) in valid_inputs:
			with self.subTest(i=i, n=n, seq=seq):
				self.assertEqual(list(itertools.islice(_digitRemainderSeq(i), n)), seq)

		# Test invalid inputs raise TypeError.
		for i in invalid_inputs:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_digitRemainderSeq(i))

	def test__digitSeq(self) -> None:
		valid_inputs = [
			(123, 5, [3, 2, 1, 0, 0]),
			(0, 10, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(1, 3, [1, 0, 0]),
			(2, 3, [2, 0, 0]),
			(3, 3, [3, 0, 0]),
			(4, 3, [4, 0, 0]),
			(5, 3, [5, 0, 0]),
			(6, 3, [6, 0, 0]),
			(7, 3, [7, 0, 0]),
			(8, 3, [8, 0, 0]),
			(9, 3, [9, 0, 0]),
			(1023, 6, [3, 2, 0, 1, 0, 0]),
			(1230, 6, [0, 3, 2, 1, 0, 0]),
		]

		invalid_inputs = [
			-1,
			1.1,
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (i, n, seq) in valid_inputs:
			with self.subTest(i=i, n=n, seq=seq):
				self.assertEqual(list(itertools.islice(_digitSeq(i), n)), seq)

		# Test invalid inputs raise TypeError.
		for i in invalid_inputs:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_digitSeq(i))

	def test__lastSignificantDigit(self) -> None:
		valid_inputs = [
			(_digitRemainderSeq(123), 2),
			(_fractionDigitRemainderSeq(decimal.Decimal("0.4567")), 3),
			(_digitSeq(0), 0),
			(_digitSeq(1), 0),
			(_digitSeq(12), 1),
			(_digitSeq(123), 2),
			(_digitSeq(1023), 1), # BUG: 3?
			(_digitSeq(1230), 0), # BUG: 3? 1?
			(_digitSeq(123000), 0), # BUG: 5? 3?
		]

		invalid_inputs = [
			...
		]

		# Test valid inputs have valid outputs.
		for (seq, i) in valid_inputs:
			with self.subTest(seq=seq, i=i):
				self.assertEqual(_lastSignificantDigit(seq), i)

		# Test invalid inputs raise TypeError.
		for seq in invalid_inputs:
			with self.subTest(seq=seq):
				with self.assertRaises(TypeError):
					_lastSignificantDigit(seq)

	def test__fractionDigitRemainderSeq(self) -> None:
		def dec(f: str) -> decimal.Decimal:
			return decimal.Decimal(f)

		valid_inputs = [
			(dec("0.4567"), 6, [dec("4.5670"), dec("5.6700"), dec("6.7000"), dec("7.0000"), dec("0.0000"), dec("0.0000")]),
			(dec("0.0"), 10, [dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0"), dec("0.0")]),
			(dec("0.1"), 3, [dec("1.0"), dec("0.0"), dec("0.0")]),
			(dec("0.2"), 3, [dec("2.0"), dec("0.0"), dec("0.0")]),
			(dec("0.3"), 3, [dec("3.0"), dec("0.0"), dec("0.0")]),
			(dec("0.4"), 3, [dec("4.0"), dec("0.0"), dec("0.0")]),
			(dec("0.5"), 3, [dec("5.0"), dec("0.0"), dec("0.0")]),
			(dec("0.6"), 3, [dec("6.0"), dec("0.0"), dec("0.0")]),
			(dec("0.7"), 3, [dec("7.0"), dec("0.0"), dec("0.0")]),
			(dec("0.8"), 3, [dec("8.0"), dec("0.0"), dec("0.0")]),
			(dec("0.9"), 3, [dec("9.0"), dec("0.0"), dec("0.0")]),
			(dec("0.123"), 5, [dec("1.230"), dec("2.300"), dec("3.000"), dec("0.000"), dec("0.000")]),
			(dec("0.1023"), 6, [dec("1.0230"), dec("0.2300"), dec("2.3000"), dec("3.0000"), dec("0.0000"), dec("0.0000")]),
			(dec("0.1230"), 6, [dec("1.2300"), dec("2.3000"), dec("3.0000"), dec("0.0000"), dec("0.0000"), dec("0.0000")]),
		]

		invalid_inputs = [
			-1,
			1.1,
			"foo",
			dec("10.234"),
			dec("-1.23"),
		]

		# Test valid inputs have valid outputs.
		for (d, n, seq) in valid_inputs:
			with self.subTest(d=d, n=n, seq=seq):
				self.assertEqual(list(itertools.islice(_fractionDigitRemainderSeq(d), n)), seq)

		# Test invalid inputs raise TypeError.
		for d in invalid_inputs:
			with self.subTest(d=d):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_fractionDigitRemainderSeq(d))

	def test__fractionDigitSeq(self) -> None:
		valid_inputs = [
			(decimal.Decimal("0.4567"), 6, [4, 5, 6, 7, 0, 0]),
			(decimal.Decimal("0.0"), 10, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(decimal.Decimal("0.1"), 3, [1, 0, 0]),
			(decimal.Decimal("0.2"), 3, [2, 0, 0]),
			(decimal.Decimal("0.3"), 3, [3, 0, 0]),
			(decimal.Decimal("0.4"), 3, [4, 0, 0]),
			(decimal.Decimal("0.5"), 3, [5, 0, 0]),
			(decimal.Decimal("0.6"), 3, [6, 0, 0]),
			(decimal.Decimal("0.7"), 3, [7, 0, 0]),
			(decimal.Decimal("0.8"), 3, [8, 0, 0]),
			(decimal.Decimal("0.9"), 3, [9, 0, 0]),
			(decimal.Decimal("0.123"), 5, [1, 2, 3, 0, 0]),
			(decimal.Decimal("0.1023"), 6, [1, 0, 2, 3, 0, 0]),
			(decimal.Decimal("0.1230"), 6, [1, 2, 3, 0, 0, 0]),
		]

		invalid_inputs = [
			-1,
			1.1,
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (d, n, seq) in valid_inputs:
			with self.subTest(d=d, n=n, seq=seq):
				self.assertEqual(list(itertools.islice(_fractionDigitSeq(d), n)), seq)

		# Test invalid inputs raise TypeError.
		for d in invalid_inputs:
			with self.subTest(d=d):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_fractionDigitSeq(d))

	def test__fractionDigitsCanonicalFragmentMap(self) -> None:
		valid_inputs = [
			(decimal.Decimal("0.4567"), "4567"),
			(decimal.Decimal("0.0"), "0"),
			(decimal.Decimal("0.1"), "1"),
			(decimal.Decimal("0.123"), "123"),
			(decimal.Decimal("0.1023"), "1023"),
			(decimal.Decimal("0.0123"), "0123"),
			(decimal.Decimal("0.1230"), "123"),
			(decimal.Decimal("0.01230"), "0123"),
			(decimal.Decimal("0.10230"), "1023"),
		]

		invalid_inputs = [
			"",
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid inputs have valid outputs.
		for (d, s) in valid_inputs:
			with self.subTest(d=d, s=s):
				self.assertEqual(_fractionDigitsCanonicalFragmentMap(d), s)

		# Test invalid inputs raise TypeError.
		for d in invalid_inputs:
			with self.subTest(d=d):
				with self.assertRaises(TypeError):
					_fractionDigitsCanonicalFragmentMap(d)


...


class TestDatatypesMappings(unittest.TestCase):

	def test_unsignedNoDecimalMap(self) -> None:
		valid_inputs = [
			("0", 0),
			("123", 123),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			"123.456",
			"-123",
			"-123.456",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, i) in valid_inputs:
			with self.subTest(s=s, i=i):
				self.assertEqual(unsignedNoDecimalMap(s), i)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					unsignedNoDecimalMap(s)

	def test_noDecimalMap(self) -> None:
		valid_inputs = [
			("0", 0),
			("123", 123),
			("-0", -0),
			("-123", -123),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			"123.456",
			"-123.456",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, i) in valid_inputs:
			with self.subTest(s=s, i=i):
				self.assertEqual(noDecimalMap(s), i)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					noDecimalMap(s)

	def test_unsignedDecimalPtMap(self) -> None:
		valid_inputs = [
			("0.", decimal.Decimal("0.")),
			("123.", decimal.Decimal("123.")),
			("0.0", decimal.Decimal("0.0")),
			("123.0", decimal.Decimal("123.0")),
			("123.456", decimal.Decimal("123.456")),
			("0.456", decimal.Decimal("0.456")),
			(".456", decimal.Decimal(".456")),
			("123.4560", decimal.Decimal("123.4560")),
			("0.4560", decimal.Decimal("0.4560")),
			(".4560", decimal.Decimal(".4560")),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			"123",
			"-123",
			"-123.456",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, d) in valid_inputs:
			with self.subTest(s=s, d=d):
				self.assertEqual(unsignedDecimalPtMap(s), d)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					unsignedDecimalPtMap(s)

	def test_decimalPtMap(self) -> None:
		valid_inputs = [
			("0.", decimal.Decimal("0.")),
			("123.", decimal.Decimal("123.")),
			("0.0", decimal.Decimal("0.0")),
			("123.0", decimal.Decimal("123.0")),
			("123.456", decimal.Decimal("123.456")),
			("0.456", decimal.Decimal("0.456")),
			(".456", decimal.Decimal(".456")),
			("-0.", decimal.Decimal("-0.")),
			("-123.", decimal.Decimal("-123.")),
			("-0.0", decimal.Decimal("-0.0")),
			("-123.0", decimal.Decimal("-123.0")),
			("-123.456", decimal.Decimal("-123.456")),
			("-0.456", decimal.Decimal("-0.456")),
			("-.456", decimal.Decimal("-.456")),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			"123",
			"-123",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, d) in valid_inputs:
			with self.subTest(s=s, d=d):
				self.assertEqual(decimalPtMap(s), d)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					decimalPtMap(s)

	def test_scientificMap(self) -> None:
		valid_inputs = [
			("0e0", decimal.Decimal("0")),
			("123e0", decimal.Decimal("123")),
			("-0e0", decimal.Decimal("-0")),
			("-123e0", decimal.Decimal("-123")),
			("0.e0", decimal.Decimal("0.")),
			("123.e0", decimal.Decimal("123.")),
			("0.0e0", decimal.Decimal("0.0")),
			("123.0e0", decimal.Decimal("123.0")),
			("123.456e0", decimal.Decimal("123.456")),
			("0.456e0", decimal.Decimal("0.456")),
			(".456e0", decimal.Decimal(".456")),
			("-0.e0", decimal.Decimal("-0.")),
			("-123.e0", decimal.Decimal("-123.")),
			("-0.0e0", decimal.Decimal("-0.0")),
			("-123.0e0", decimal.Decimal("-123.0")),
			("-123.456e0", decimal.Decimal("-123.456")),
			("-0.456e0", decimal.Decimal("-0.456")),
			("-.456e0", decimal.Decimal("-.456")),
			("0E0", decimal.Decimal("0")),
			("123E0", decimal.Decimal("123")),
			("-0E0", decimal.Decimal("-0")),
			("-123E0", decimal.Decimal("-123")),
			("0.E0", decimal.Decimal("0.")),
			("123.E0", decimal.Decimal("123.")),
			("0.0E0", decimal.Decimal("0.0")),
			("123.0E0", decimal.Decimal("123.0")),
			("123.456E0", decimal.Decimal("123.456")),
			("0.456E0", decimal.Decimal("0.456")),
			(".456E0", decimal.Decimal(".456")),
			("-0.E0", decimal.Decimal("-0.")),
			("-123.E0", decimal.Decimal("-123.")),
			("-0.0E0", decimal.Decimal("-0.0")),
			("-123.0E0", decimal.Decimal("-123.0")),
			("-123.456E0", decimal.Decimal("-123.456")),
			("-0.456E0", decimal.Decimal("-0.456")),
			("-.456E0", decimal.Decimal("-.456")),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			"123",
			"-123",
			"123.456",
			"-123.456",
			".456",
			"-.456",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, d) in valid_inputs:
			with self.subTest(s=s, d=d):
				self.assertEqual(scientificMap(s), d)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					scientificMap(s)

	...

	def test_unsignedNoDecimalPtCanonicalMap(self) -> None:
		valid_inputs = [
			(0, "0"),
			(123, "123"),
			(1230, "1230"),
			(12300, "12300"),
			(12305, "12305"),
		]

		invalid_inputs = [
			-123,
			123.456,
			-123.456,
			"foo",
			"123",
			"-123",
			"123.456",
			"-123.456",
		]

		# Test valid inputs have valid outputs.
		for (i, s) in valid_inputs:
			with self.subTest(i=i, s=s):
				self.assertEqual(unsignedNoDecimalPtCanonicalMap(i), s)

		# Test invalid inputs raise TypeError.
		for i in invalid_inputs:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					unsignedNoDecimalPtCanonicalMap(i)

	def test_noDecimalPtCanonicalMap(self) -> None:
		valid_inputs = [
			(0, "0"),
			(123, "123"),
			(1230, "1230"),
			(12300, "12300"),
			(12305, "12305"),
			(-0, "0"),
			(-123, "-123"),
			(-1230, "-1230"),
			(-12300, "-12300"),
			(-12305, "-12305"),
		]

		invalid_inputs = [
			123.456,
			-123.456,
			"foo",
			"123",
			"-123",
			"123.456",
			"-123.456",
		]

		# Test valid inputs have valid outputs.
		for (i, s) in valid_inputs:
			with self.subTest(i=i, s=s):
				self.assertEqual(noDecimalPtCanonicalMap(i), s)

		# Test invalid inputs raise TypeError.
		for i in invalid_inputs:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					noDecimalPtCanonicalMap(i)

	def test_unsignedDecimalPtCanonicalMap(self) -> None:
		valid_inputs = [
			(decimal.Decimal("0"), "0.0"),
			(decimal.Decimal("123"), "123.0"),
			(decimal.Decimal("1230"), "1230.0"),
			(decimal.Decimal("12300"), "12300.0"),
			(decimal.Decimal("12305"), "12305.0"),
			(decimal.Decimal("0."), "0.0"),
			(decimal.Decimal("123."), "123.0"),
			(decimal.Decimal("1230."), "1230.0"),
			(decimal.Decimal("12300."), "12300.0"),
			(decimal.Decimal("12305."), "12305.0"),
			(decimal.Decimal(".0"), "0.0"),
			(decimal.Decimal(".123"), "0.123"),
			# (decimal.Decimal(".1230"), "0.1230"),
			# (decimal.Decimal(".12300"), "0.12300"),
			# (decimal.Decimal(".12305"), "0.12305"),
			(decimal.Decimal("0.0"), "0.0"),
			(decimal.Decimal("0.123"), "0.123"),
			# (decimal.Decimal("0.1230"), "0.1230"),
			# (decimal.Decimal("0.12300"), "0.12300"),
			# (decimal.Decimal("0.12305"), "0.12305"),
			(decimal.Decimal("456.0"), "456.0"),
			(decimal.Decimal("456.123"), "456.123"),
			# (decimal.Decimal("456.1230"), "456.1230"),
			# (decimal.Decimal("456.12300"), "456.12300"),
			# (decimal.Decimal("456.12305"), "456.12305"),
			(decimal.Decimal("406.0"), "406.0"),
			(decimal.Decimal("406.123"), "406.123"),
			# (decimal.Decimal("406.1230"), "406.1230"),
			# (decimal.Decimal("406.12300"), "406.12300"),
			# (decimal.Decimal("406.12305"), "406.12305"),
		]

		invalid_inputs = [
			decimal.Decimal("-123"),
			decimal.Decimal("-123."),
			decimal.Decimal("-123.0"),
			decimal.Decimal("-123.456"),
			decimal.Decimal("-0.456"),
			decimal.Decimal("-.456"),
			-123,
			123.456,
			-123.456,
			"foo",
			"123",
			"-123",
			"123.456",
			"-123.456",
		]

		# Test valid inputs have valid outputs.
		for (d, s) in valid_inputs:
			with self.subTest(d=d, s=s):
				self.assertEqual(unsignedDecimalPtCanonicalMap(d), s)

		# Test invalid inputs raise TypeError.
		for d in invalid_inputs:
			with self.subTest(d=d):
				with self.assertRaises(TypeError):
					unsignedDecimalPtCanonicalMap(d)

	...

	def test_decimalLexicalMap(self) -> None:
		valid_inputs = [
			("0", decimal.Decimal("0")),
			("123", decimal.Decimal("123")),
			("-0", decimal.Decimal("-0")),
			("-123", decimal.Decimal("-123")),
			("0.", decimal.Decimal("0.")),
			("123.", decimal.Decimal("123.")),
			("0.0", decimal.Decimal("0.0")),
			("123.0", decimal.Decimal("123.0")),
			("123.456", decimal.Decimal("123.456")),
			("0.456", decimal.Decimal("0.456")),
			(".456", decimal.Decimal(".456")),
			("-0.", decimal.Decimal("-0.")),
			("-123.", decimal.Decimal("-123.")),
			("-0.0", decimal.Decimal("-0.0")),
			("-123.0", decimal.Decimal("-123.0")),
			("-123.456", decimal.Decimal("-123.456")),
			("-0.456", decimal.Decimal("-0.456")),
			("-.456", decimal.Decimal("-.456")),
		]

		invalid_inputs = [
			123,
			123.456,
			-123,
			"foo",
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, d) in valid_inputs:
			with self.subTest(s=s, d=d):
				self.assertEqual(decimalLexicalMap(s), d)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					decimalLexicalMap(s)

	...

	def test_stringLexicalMap(self) -> None:
		valid_inputs = [
			("foo", "foo"),
		]

		invalid_inputs = [
			123,
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, S) in valid_inputs:
			with self.subTest(s=s, S=S):
				self.assertEqual(stringLexicalMap(s), S)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					stringLexicalMap(s)

	def test_booleanLexicalMap(self) -> None:
		valid_inputs = [
			("true", True),
			("false", False),
			("1", True),
			("0", False),
		]

		invalid_inputs = [
			"foo",
			123,
			True,
		]

		# Test valid inputs have valid outputs.
		for (s, B) in valid_inputs:
			with self.subTest(s=s, B=B):
				self.assertEqual(booleanLexicalMap(s), B)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					booleanLexicalMap(s)

	def test_stringCanonicalMap(self) -> None:
		valid_inputs = [
			("foo", "foo"),
		]

		invalid_inputs = [
			123,
			True,
		]

		# Test valid inputs have valid outputs.
		for (S, s) in valid_inputs:
			with self.subTest(S=S, s=s):
				self.assertEqual(stringCanonicalMap(S), s)

		# Test invalid inputs raise TypeError.
		for S in invalid_inputs:
			with self.subTest(S=S):
				with self.assertRaises(TypeError):
					stringCanonicalMap(S)

	def test_booleanCanonicalMap(self) -> None:
		valid_inputs = [
			(True, "true"),
			(False, "false"),
		]

		invalid_inputs = [
			"true",
			"false",
			"1",
			"0",
			1,
			0,
			"foo",
			123,
		]

		# Test valid inputs have valid outputs.
		for (B, b) in valid_inputs:
			with self.subTest(B=B, b=b):
				self.assertEqual(booleanCanonicalMap(B), b)

		# Test invalid inputs raise TypeError.
		for B in invalid_inputs:
			with self.subTest(B=B):
				with self.assertRaises(TypeError):
					booleanCanonicalMap(B)



...


class TestDatatypesDatatypes(unittest.TestCase):

	@unittest.mock.patch.multiple(Datatype, __abstractmethods__=set())
	def test_Datatype(self) -> None:
		# Test in_lexical_space().
		with self.subTest():
			with self.assertRaises(NotImplementedError):
				Datatype.in_lexical_space("x")

		# Test lexical_mapping().
		with self.subTest():
			with self.assertRaises(NotImplementedError):
				Datatype.lexical_mapping("x")

		# Test canonical_mapping().
		with self.subTest():
			with self.assertRaises(NotImplementedError):
				Datatype.canonical_mapping("x")

		class ExampleDatatype(Datatype):
			@classmethod
			def in_lexical_space(cls, literal: str) -> bool:
				return False if literal is None else True

			@classmethod
			def lexical_mapping(cls, lexical_representation: str) -> typing.Any:
				assert cls.in_lexical_space(lexical_representation)

				return lexical_representation

			@classmethod
			def canonical_mapping(cls, value: typing.Any) -> str:
				return value

		# Test __init__() and lexical_representation.setter with good input.
		x = ExampleDatatype("x")

		# Test lexical_representation.
		with self.subTest():
			self.assertEqual(x.lexical_representation, "x")

		# Test __repr__().
		with self.subTest():
			self.assertEqual(Datatype.__repr__(x), "ExampleDatatype('x')")

		# Test value.
		with self.subTest():
			self.assertEqual(x.value, "x")

		# Test canonical_representation.
		with self.subTest():
			self.assertEqual(x.canonical_representation, "x")

		# Test __init__() and lexical_representation.setter with bad input.
		with self.subTest():
			with self.assertRaises(TypeError):
				ExampleDatatype(None)


	def test_String(self) -> None:
		valid_inputs = [
			("foo", "foo", "foo"),
		]

		invalid_inputs = [
			123,
			True,
			False,
			None,
			123.456,
		]

		# Test valid inputs have valid outputs.
		for (s, lm, cm) in valid_inputs:
			x = String(s)

			with self.subTest(s=s):
				self.assertTrue(x.in_lexical_space(s))

			with self.subTest(s=s, lm=lm):
				self.assertEqual(x.lexical_mapping(s), lm)

			with self.subTest(lm=lm, cm=cm):
				self.assertEqual(x.canonical_mapping(lm), cm)

			with self.subTest(s=s, lm=lm, cm=cm):
				self.assertEqual(x.canonical_mapping(x.lexical_mapping(s)), cm)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					String(s)

	def test_Boolean(self) -> None:
		valid_inputs = [
			("true", True, "true"),
			("false", False, "false"),
			("1", True, "true"),
			("0", False, "false"),
		]

		invalid_inputs = [
			"foo",
		]

		# Test valid inputs have valid outputs.
		for (s, lm, cm) in valid_inputs:
			x = Boolean(s)

			with self.subTest(s=s):
				self.assertTrue(x.in_lexical_space(s))

			with self.subTest(s=s, lm=lm):
				self.assertEqual(x.lexical_mapping(s), lm)

			with self.subTest(lm=lm, cm=cm):
				self.assertEqual(x.canonical_mapping(lm), cm)

			with self.subTest(s=s, lm=lm, cm=cm):
				self.assertEqual(x.canonical_mapping(x.lexical_mapping(s)), cm)

		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					Boolean(s)
