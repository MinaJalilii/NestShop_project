# import traceback
# from itertools import count
# from unittest import TestCase
# import mytest
#
#
# class TestMytest(TestCase):
#     def test_simple_take(self):
#         t = mytest.take(range(5), 3)
#         self.assertEqual(t, [0, 1, 2])
#
#     def test_null_take(self):
#         t = mytest.take(range(5), 0)
#         self.assertEqual(t, [])
#
#     def test_negative_take(self):
#         self.assertRaises(ValueError, lambda: mytest.take(range(5), -2))
#
#     def test_take_too_much(self):
#         t = mytest.take(range(5), 10)
#         self.assertEqual(t, [0, 1, 2, 3, 4])
#
#
# class TestChunked(TestCase):
#     def test_even(self):
#         t = list(mytest.chunked('abcd', 2))
#         self.assertEqual(t, [['a', 'b'], ['c', 'd']])
#
#     def test_odd(self):
#         t = list(mytest.chunked('abcde', 2))
#         self.assertEqual(t, [['a', 'b'], ['c', 'd'], ['e']])
#
#     def test_none(self):
#         t = list(mytest.chunked('abcd', None))
#         self.assertEqual(t, [['a', 'b', 'c', 'd']])
#
#     def test_strict_false(self):
#         t = list(mytest.chunked('abcde', 2, strict=False))
#         self.assertEqual(t, [['a', 'b'], ['c', 'd'], ['e']])
#
#     def test_strict_true(self):
#         t = list(mytest.chunked('abcd', 2, strict=True))
#
#         def t1():
#             return list(mytest.chunked('abcde', 2, strict=True))
#
#         self.assertEqual(t, [['a', 'b'], ['c', 'd']])
#         self.assertRaisesRegex(ValueError, "iterable isn't divisible by n!", t1)
#
#     def test_strict_true_size_none(self):
#         def t():
#             return list(mytest.chunked('abcd', None, strict=True))
#
#         self.assertRaisesRegex(ValueError, "n can't be none!", t)
#
#
# class TestFirst(TestCase):
#     def test_many(self):
#         self.assertEqual(mytest.first([1, 2, 3, 4]), 1)
#
#     def test_one(self):
#         self.assertEqual(mytest.first([1]), 1)
#
#     def test_empty_with_default(self):
#         self.assertEqual(mytest.first([], default='hey'), 'hey')
#
#     def test_empty_without_default(self):
#         try:
#             mytest.first([])
#         except ValueError:
#             formatted_exc = traceback.format_exc()
#             self.assertIn('StopIteration', formatted_exc)
#             self.assertIn('The above exception was the direct cause', formatted_exc)
#         else:
#             self.fail()
#
#     def test_not_iterable_object(self):
#         try:
#             mytest.first(111)
#         except TypeError:
#             formatted_exc = traceback.format_exc()
#             self.assertIn('TypeError', formatted_exc)
#             self.assertIn('The above exception was the direct cause', formatted_exc)
#         else:
#             self.fail()
#
#
# class TestLast(TestCase):
#     def test_basic(self):
#         cases = [
#             (range(5), 4),
#             (iter(range(5)), 4),
#             (range(1), 0),
#             (iter(range(1)), 0),
#             ({i: str(i) for i in range(5)}, 4),
#         ]
#         for iterable, expected in cases:
#             with self.subTest(iterable=iterable):
#                 self.assertEqual(mytest.last(iterable), expected)
#
#     def test_default(self):
#         cases = [
#             (range(5), None, 4),
#             (iter(range(5)), None, 4),
#             (None, None, None),
#             ([], 'hello', 'hello'),
#             ({}, None, None),
#             (iter([]), 'hey', 'hey'),
#             (range(0), 'boo', 'boo'),
#         ]
#         for iterable, default, expected in cases:
#             with self.subTest(iterable=iterable, default=default):
#                 self.assertEqual(mytest.last(iterable, default=default), expected)
#
#     def test_empty(self):
#         for iterable in ([], iter(range(0))):
#             with self.subTest(iterable=iterable):
#                 with self.assertRaises(ValueError):
#                     mytest.last(iterable)
#
#     def test_not_iterable_object(self):
#         try:
#             mytest.last(111)
#         except TypeError:
#             formatted_exc = traceback.format_exc()
#             self.assertIn('TypeError', formatted_exc)
#             self.assertIn('The above exception was the direct cause', formatted_exc)
#         else:
#             self.fail()
#
#
# class TestNthOrLast(TestCase):
#     def test_basic(self):
#         self.assertEqual(mytest.nth_or_last(range(5), 3), 3)
#         self.assertEqual(mytest.nth_or_last(range(5), 10), 4)
#
#     def test_default(self):
#         default = 50
#         self.assertEqual(mytest.nth_or_last(range(0), 12, default), default)
#
#     def test_empty_iterable_no_default(self):
#         self.assertRaises(ValueError, lambda: mytest.nth_or_last(range(0), 12))
#
#
# class TestOne(TestCase):
#     def test_basic(self):
#         self.assertEqual(mytest.one(range(1)), 0)
#         self.assertEqual(mytest.one([1]), 1)
#
#     def test_too_short(self):
#         iterable = []
#         for too_short, exc_type in [
#             (None, ValueError),
#             (IndexError, IndexError)
#         ]:
#             with self.subTest(too_short=too_short):
#                 try:
#                     mytest.one(iterable, too_short=too_short)
#                 except exc_type:
#                     formatted_exc = traceback.format_exc()
#                     self.assertIn('StopIteration', formatted_exc)
#                     self.assertIn('The above exception was the direct cause', formatted_exc)
#                 else:
#                     self.fail()
#
#     def test_too_long(self):
#         iterable = count()
#         # iterable = [0, 1, 2, 3, 4, 5, 6]
#         self.assertRaises(ValueError, lambda: mytest.one(iterable))
#         self.assertEqual(next(iterable), 2)
#         self.assertRaises(TypeError, lambda: mytest.one(iterable, too_long=TypeError))
#
#     def test_too_long_default_message(self):
#         iterable = count()
#         self.assertRaisesRegex(ValueError, 'Expected exactly one item in iterable, but got 0, 1.',
#                                lambda: mytest.one(iterable))
#
#
# class TestInterleave(TestCase):
#     def test_basic(self):
#         entry = list(mytest.interleave([1, 4, 7], [2, 5, 8], [3, 6, 9]))
#         expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
#         self.assertEqual(entry, expected)
#
#     def test_not_even_iterables(self):
#         entry = list(mytest.interleave([1, 4, 7], [2, 5], [3, 6, 9]))
#         expected = [1, 2, 3, 4, 5, 6]
#         self.assertEqual(entry, expected)
#
#     def test_mix_types(self):
#         entry = list(mytest.interleave(count(), ['mina', 'bita', 'hossein'], ['jalili', 'jalali', 'rezaei']))
#         expected = [0, 'mina', 'jalili', 1, 'bita', 'jalali', 2, 'hossein', 'rezaei']
#         self.assertEqual(entry, expected)
