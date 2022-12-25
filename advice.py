class Advice:
	def __init__(self, message, alg, ignore_u=False, done=False) -> None:
		self.message: str = message
		self.alg: list = alg
		self.ignore_u: bool = ignore_u
		self.done: bool = done


	def __eq__(self, other):
		if self.message != other.message:
			return False
		if self.alg != other.alg:
			return False
		if self.ignore_u != other.ignore_u:
			return False
		if self.done != other.done:
			return False
		return True


#-----------------------------------------------------------------------------------------------------------------

import unittest

class TestStringMethods(unittest.TestCase):
	def test___eq__correct(self):
		advice = Advice("test", ["f", "u2"], True, False)
		test_advice = Advice("test", ["f", "u2"], True, False)
		self.assertTrue(advice == test_advice)

	def test___eq__wrong_message(self):
		advice = Advice("test1", ["f", "u2"], True, False)
		test_advice = Advice("test", ["f", "u2"], True, False)
		self.assertTrue(advice != test_advice)

	def test___eq__wrong_algs(self):
		advice = Advice("test", ["f"], True, False)
		test_advice = Advice("test", ["f", "u2"], True, False)
		self.assertTrue(advice != test_advice)

	def test___eq__wrong_algs2(self):
		advice = Advice("test", ["f"], True, False)
		test_advice = Advice("test", ["f2"], True, False)
		self.assertTrue(advice != test_advice)

	def test___eq__wrong_ignore_u(self):
		advice = Advice("test", ["f", "u2"], True, False)
		test_advice = Advice("test", ["f", "u2"], False, False)
		self.assertTrue(advice != test_advice)

	def test___eq__wrong_done(self):
		advice = Advice("test", ["f", "u2"], True, False)
		test_advice = Advice("test", ["f", "u2"], True, True)
		self.assertTrue(advice != test_advice)
        

if __name__ == '__main__':
    unittest.main()