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
		]

		invalid_inputs = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
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
		]

		invalid_inputs = [
			"123.456",
			"foo",
			["f", "o", "o"],
			"123foo",
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
		valid_inputs = [
			("foo", "foo", "foo"),
		]

		invalid_inputs = [
		]

		# Test valid inputs have valid outputs.
		for (s, lm, cm) in valid_inputs:
			x = String(s)

			with self.subTest(s=s):
				self.assertTrue(x.in_lexical_space(s))

			with self.subTest(s=s, lm=lm):
				self.assertEqual(x.lexical_mapping(s), lm)

			with self.subTest(s=s, cm=cm):
				self.assertEqual(x.canonical_mapping(s), cm)


		# Test invalid inputs raise TypeError.
		for s in invalid_inputs:
			with self.subTest(s=s):
				with self.assertRaises(TypeError):
					String(s)
