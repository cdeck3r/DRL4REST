import random
import unittest
from openapi_server.models import Cart
from cartpole.gprest.server_model import CartpoleServer
from cartpole.gprest.server_model_regression import ServerModelRegression

# small test routine for the regression on a ServerModel
class Test_ServerModelRegression(unittest.TestCase):
    def setUp(self):
        self.sm = CartpoleServer
        self.sm.reset()
        self.sm.n_instances()
        self.smr = ServerModelRegression(self.sm)

    def test_add_cart(self):
        weight = random.randint(1, 10)
        max_sm_instances = len(self.sm._instances)
        inst_num = random.randint(1, max_sm_instances - 1)
        ms = '_cart'
        ms_list = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)
        self.assertEqual(len(ms_list), weight)
        self.assertIsInstance(ms_list[0], Cart)

    def test_add_direction(self):
        weight = random.randint(1, 10)
        max_sm_instances = len(self.sm._instances)
        inst_num = random.randint(1, max_sm_instances - 1)
        ms = '_direction'
        ms_list = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)
        # since _direction is None, nothing is added
        self.assertEqual(len(ms_list), 0)

    def _cart_list(self, n=0):
        if n == 0:
            weight = random.randint(1, 10)
        else:
            weight = n
        max_sm_instances = len(self.sm._instances)
        inst_num = random.randint(1, max_sm_instances - 1)
        ms = '_cart'
        ms_list1 = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)

        return ms_list1

    def test_concat_carts_and_poles(self):
        weight = random.randint(1, 10)
        max_sm_instances = len(self.sm._instances)
        inst_num = random.randint(1, max_sm_instances - 1)
        ms = '_cart'
        ms_list1 = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)
        ms = '_pole'
        ms_list2 = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)

        self.assertEqual(len(ms_list1), weight)
        self.assertEqual(len(ms_list2), weight)
        ms_list = self.smr.concat(ms_list1, ms_list2)

        self.assertEqual(len(ms_list), 2 * weight)

    def test_concat_carts_and_none(self):
        ms_list1 = self._cart_list()
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, None)
        self.assertEqual(len(ms_list), weight)

        ms_list = self.smr.concat(None, ms_list1)
        self.assertEqual(len(ms_list), weight)

    def test_concat_none_and_none(self):
        ms_list = self.smr.concat(None, None)
        self.assertEqual(len(ms_list), 0)

    def test_max(self):
        ms_list1 = self._cart_list(n=10)
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, ms_list1)
        self.assertEqual(len(ms_list), 2 * weight)

        ms_list_max = self.smr.max(ms_list, ms_list1)
        self.assertEqual(len(ms_list_max), len(ms_list))

        ms_list_max = self.smr.max(ms_list1, ms_list)
        self.assertEqual(len(ms_list_max), len(ms_list))

        ms_list2 = self._cart_list(n=10)
        ms_list_max = self.smr.max(ms_list1, ms_list2)
        self.assertIs(ms_list1, ms_list_max)

    def test_max_none(self):
        ms_list1 = self._cart_list()
        weight = len(ms_list1)

        ms_list_max = self.smr.max(ms_list1, None)
        self.assertEqual(len(ms_list_max), len(ms_list1))

        ms_list_max = self.smr.max(None, ms_list1)
        self.assertEqual(len(ms_list_max), len(ms_list1))

        ms_list_max = self.smr.max(None, None)
        self.assertEqual(len(ms_list_max), 0)

    def test_min(self):
        ms_list1 = self._cart_list(n=10)
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, ms_list1)
        self.assertEqual(len(ms_list), 2 * weight)

        ms_list_min = self.smr.min(ms_list, ms_list1)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.min(ms_list1, ms_list)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list2 = self._cart_list(n=10)
        ms_list_min = self.smr.min(ms_list1, ms_list2)
        self.assertIs(ms_list1, ms_list_min)

    def test_min_none(self):
        ms_list1 = self._cart_list()
        weight = len(ms_list1)

        ms_list_min = self.smr.min(ms_list1, None)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.max(None, ms_list1)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.min(None, None)
        self.assertEqual(len(ms_list_min), 0)

    def test_sum_cart(self):
        ms_list1 = self._cart_list()
        weight = len(ms_list1)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_ServerModelRegression)
    unittest.TextTestRunner(verbosity=2).run(suite)
