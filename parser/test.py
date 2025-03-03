import unittest

import mona


class Test(unittest.TestCase):

    def test_reorder_transition_letters(self):
        res = mona.reorder_transition_letters(
            "X01", ["c", "d", "b"], ["a", "b", "c", "d"]
        )
        self.assertEqual(res, "X1X0")
        res = mona.reorder_transition_letters("", [], ["a", "b", "c"])
        self.assertEqual(res, "XXX")
        res = mona.reorder_transition_letters(
            "101", ["c", "d", "b"], ["c", "d", "b"]
        )
        self.assertEqual(res, "101")


if __name__ == "__main__":
    unittest.main()
