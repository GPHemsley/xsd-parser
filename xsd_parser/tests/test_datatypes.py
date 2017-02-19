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

class TestDatatypesAuxiliaryFunctions(unittest.TestCase):

	def test__digitValue(self) -> None:
		valid_digits = [
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

		invalid_digits = [
			"10",
			"1.1",
			"foo",
		]

		# Test valid digits have valid output.
		for (s, i) in valid_digits:
			with self.subTest(s=s, i=i):
				self.assertEqual(_digitValue(s), i)

		# Test invalid digits raise TypeError.
		for s in invalid_digits:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_digitValue(s)

	def test__digitSequenceValue(self) -> None:
		valid_digit_sequences = [
			("", 0),
			("0", 0),
			("1", 1),
			("123", 123),
			("0123", 123),
			("1230", 1230),
			("01230", 1230),
		]

		invalid_digit_sequences = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid digits have valid output.
		for (s, i) in valid_digit_sequences:
			with self.subTest(s=s, i=i):
				self.assertEqual(_digitSequenceValue(s), i)

		# Test invalid digits raise TypeError.
		for s in invalid_digit_sequences:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_digitSequenceValue(s)

	def test__fractionDigitSequenceValue(self) -> None:
		valid_fraction_digit_sequences = [
			("", decimal.Decimal("0")),
			("0", decimal.Decimal("0.0")),
			("1", decimal.Decimal("0.1")),
			("123", decimal.Decimal("0.123")),
			("0123", decimal.Decimal("0.0123")),
			("1230", decimal.Decimal("0.1230")),
			("01230", decimal.Decimal("0.01230")),
		]

		invalid_fraction_digit_sequences = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid digits have valid output.
		for (s, i) in valid_fraction_digit_sequences:
			with self.subTest(s=s, i=i):
				self.assertEqual(_fractionDigitSequenceValue(s), i)

		# Test invalid digits raise TypeError.
		for s in invalid_fraction_digit_sequences:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_fractionDigitSequenceValue(s)

	def test__fractionFragValue(self) -> None:
		valid_fraction_frags = [
			("0", decimal.Decimal("0.0")),
			("1", decimal.Decimal("0.1")),
			("123", decimal.Decimal("0.123")),
			("0123", decimal.Decimal("0.0123")),
			("1230", decimal.Decimal("0.1230")),
			("01230", decimal.Decimal("0.01230")),
		]

		invalid_fraction_frags = [
			"",
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid digits have valid output.
		for (s, i) in valid_fraction_frags:
			with self.subTest(s=s, i=i):
				self.assertEqual(_fractionFragValue(s), i)

		# Test invalid digits raise TypeError.
		for s in invalid_fraction_frags:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_fractionFragValue(s)

	def test__digit(self) -> None:
		valid_digit_values = [
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

		invalid_digit_values = [
			10,
			1.1,
			"foo",
		]

		# Test valid digit values have valid output.
		for (i, s) in valid_digit_values:
			with self.subTest(i=i, s=s):
				self.assertEqual(_digit(i), s)

		# Test invalid digit values raise TypeError.
		for i in invalid_digit_values:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					_digit(i)

	def test__digitRemainderSeq(self) -> None:
		valid_input = [
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

		invalid_input = [
			-1,
			1.1,
			"foo",
		]

		# Test valid digit values have valid output.
		for (i, n, s) in valid_input:
			with self.subTest(i=i, n=n, s=s):
				self.assertEqual(list(itertools.islice(_digitRemainderSeq(i), n)), s)

		# Test invalid digit values raise TypeError.
		for i in invalid_input:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_digitRemainderSeq(i))

	def test__digitSeq(self) -> None:
		valid_input = [
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

		invalid_input = [
			-1,
			1.1,
			"foo",
		]

		# Test valid digit values have valid output.
		for (i, n, s) in valid_input:
			with self.subTest(i=i, n=n, s=s):
				self.assertEqual(list(itertools.islice(_digitSeq(i), n)), s)

		# Test invalid digit values raise TypeError.
		for i in invalid_input:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_digitSeq(i))

	def test__lastSignificantDigit(self) -> None:
		valid_sequence_values = [
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

		invalid_sequence_values = [
			...
		]

		# Test valid sequence values have valid output.
		for (s, i) in valid_sequence_values:
			with self.subTest(s=s, i=i):
				self.assertEqual(_lastSignificantDigit(s), i)

		# Test invalid sequence values raise TypeError.
		for s in invalid_sequence_values:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					_lastSignificantDigit(s)

	def test__fractionDigitRemainderSeq(self) -> None:
		def d(f: str) -> decimal.Decimal:
			return decimal.Decimal(f)

		valid_input = [
			(d("0.4567"), 6, [d("4.5670"), d("5.6700"), d("6.7000"), d("7.0000"), d("0.0000"), d("0.0000")]),
			(d("0.0"), 10, [d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0"), d("0.0")]),
			(d("0.1"), 3, [d("1.0"), d("0.0"), d("0.0")]),
			(d("0.2"), 3, [d("2.0"), d("0.0"), d("0.0")]),
			(d("0.3"), 3, [d("3.0"), d("0.0"), d("0.0")]),
			(d("0.4"), 3, [d("4.0"), d("0.0"), d("0.0")]),
			(d("0.5"), 3, [d("5.0"), d("0.0"), d("0.0")]),
			(d("0.6"), 3, [d("6.0"), d("0.0"), d("0.0")]),
			(d("0.7"), 3, [d("7.0"), d("0.0"), d("0.0")]),
			(d("0.8"), 3, [d("8.0"), d("0.0"), d("0.0")]),
			(d("0.9"), 3, [d("9.0"), d("0.0"), d("0.0")]),
			(d("0.123"), 5, [d("1.230"), d("2.300"), d("3.000"), d("0.000"), d("0.000")]),
			(d("0.1023"), 6, [d("1.0230"), d("0.2300"), d("2.3000"), d("3.0000"), d("0.0000"), d("0.0000")]),
			(d("0.1230"), 6, [d("1.2300"), d("2.3000"), d("3.0000"), d("0.0000"), d("0.0000"), d("0.0000")]),
		]

		invalid_input = [
			-1,
			1.1,
			"foo",
			d("10.234"),
			d("-1.23"),
		]

		# Test valid digit values have valid output.
		for (f, n, s) in valid_input:
			with self.subTest(f=f, n=n, s=s):
				self.assertEqual(list(itertools.islice(_fractionDigitRemainderSeq(f), n)), s)

		# Test invalid digit values raise TypeError.
		for f in invalid_input:
			with self.subTest(f=f):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_fractionDigitRemainderSeq(f))

	def test__fractionDigitSeq(self) -> None:
		valid_input = [
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

		invalid_input = [
			-1,
			1.1,
			"foo",
		]

		# Test valid digit values have valid output.
		for (i, n, s) in valid_input:
			with self.subTest(i=i, n=n, s=s):
				self.assertEqual(list(itertools.islice(_fractionDigitSeq(i), n)), s)

		# Test invalid digit values raise TypeError.
		for i in invalid_input:
			with self.subTest(i=i):
				with self.assertRaises(TypeError):
					# Generator doesn't raise exception until used.
					next(_fractionDigitSeq(i))

	def test__fractionDigitsCanonicalFragmentMap(self) -> None:
		valid_input = [
			(decimal.Decimal("0.4567"), "4567"),
			(decimal.Decimal("0.0"), "0"),
			(decimal.Decimal("0.1"), "1"),
			(decimal.Decimal("0.123"), "123"),
			(decimal.Decimal("0.0123"), "0123"),
			(decimal.Decimal("0.1230"), "123"),
			(decimal.Decimal("0.01230"), "0123"),
			(decimal.Decimal("0.10230"), "1023"),
		]

		invalid_input = [
			"",
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
		]

		# Test valid digits have valid output.
		for (f, s) in valid_input:
			with self.subTest(f=f, s=s):
				self.assertEqual(_fractionDigitsCanonicalFragmentMap(f), s)

		# Test invalid digits raise TypeError.
		for f in invalid_input:
			with self.subTest(f=f):
				with self.assertRaises(TypeError):
					_fractionDigitsCanonicalFragmentMap(f)


...


class TestDatatypesMappings(unittest.TestCase):
	pass

...


class TestDatatypesDatatypes(unittest.TestCase):

	@unittest.mock.patch.multiple(Datatype, __abstractmethods__=set())
	def test_Datatype(self) -> None:
		with self.assertRaises(NotImplementedError):
			Datatype("x")

		class ExampleDatatype(Datatype):
			@classmethod
			def in_lexical_space(cls, literal: str) -> bool:
				return True

			@classmethod
			def lexical_mapping(cls, lexical_representation: str) -> typing.Any:
				assert cls.in_lexical_space(lexical_representation)

				return lexical_representation

			@classmethod
			def canonical_mapping(cls, value: typing.Any) -> str:
				return value

		ExampleDatatype("x")

	def test_String(self) -> None:
		valid_input = [
			("foo", "foo", "foo"),
		]

		invalid_input = [
		]

		for (s, lm, cm) in valid_input:
			x = String(s)

			with self.subTest(s=s):
				self.assertTrue(x.in_lexical_space(s))

			with self.subTest(s=s, lm=lm):
				self.assertEqual(x.lexical_mapping(s), lm)

			with self.subTest(s=s, cm=cm):
				self.assertEqual(x.canonical_mapping(s), cm)


		for s in invalid_input:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					String(s)
