import random
import unittest
import statistics
from openapi_server.models import Cart
from openapi_server.models import Pole
from cartpole.gprest.server_model import CartpoleServer
from cartpole.gprest.server_model_regression import CartpoleServerRegression

# small test routine for the regression on a ServerModel
# This unittest uses the CartpoleServer as the ServerModel
class Test_ServerModelRegression(unittest.TestCase):
    def setUp(self):
        self.smr = CartpoleServerRegression()
        self.sm = self.smr.sm
        self.sm.reset()
        self.sm.n_instances()

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

    def make_ms_list(self, n, ms):
        if n == 0:
            weight = random.randint(1, 10)
        else:
            weight = n
        max_sm_instances = len(self.sm._instances)
        inst_num = random.randint(1, max_sm_instances - 1)
        ms_list = self.smr.add(weight=weight, ms=ms, inst_num=inst_num)
        return ms_list

    # little helper function 
    # Extracts and returns a list of Cart from the ServerModel instances
    # n=0 (default): list contains between 1 and 10 Carts randomly
    # n: list contains n Carts
    def make_cart_list(self, n=0):
        ms = '_cart'
        ms_list = self.make_ms_list(n=n, ms=ms)
        return ms_list

    def make_pole_list(self, n=0):
        ms = '_pole'
        ms_list = self.make_ms_list(n=n, ms=ms)
        return ms_list

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
        ms_list1 = self.make_cart_list()
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, None)
        self.assertEqual(len(ms_list), weight)

        ms_list = self.smr.concat(None, ms_list1)
        self.assertEqual(len(ms_list), weight)

    def test_concat_none_and_none(self):
        ms_list = self.smr.concat(None, None)
        self.assertEqual(len(ms_list), 0)

    def test_max(self):
        ms_list1 = self.make_cart_list(n=10)
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, ms_list1)
        self.assertEqual(len(ms_list), 2 * weight)

        ms_list_max = self.smr.max(ms_list, ms_list1)
        self.assertEqual(len(ms_list_max), len(ms_list))

        ms_list_max = self.smr.max(ms_list1, ms_list)
        self.assertEqual(len(ms_list_max), len(ms_list))

        ms_list2 = self.make_cart_list(n=10)
        ms_list_max = self.smr.max(ms_list1, ms_list2)
        self.assertIs(ms_list1, ms_list_max)

    def test_max_none(self):
        ms_list1 = self.make_cart_list()
        weight = len(ms_list1)

        ms_list_max = self.smr.max(ms_list1, None)
        self.assertEqual(len(ms_list_max), len(ms_list1))

        ms_list_max = self.smr.max(None, ms_list1)
        self.assertEqual(len(ms_list_max), len(ms_list1))

        ms_list_max = self.smr.max(None, None)
        self.assertEqual(len(ms_list_max), 0)

    def test_min(self):
        ms_list1 = self.make_cart_list(n=10)
        weight = len(ms_list1)

        ms_list = self.smr.concat(ms_list1, ms_list1)
        self.assertEqual(len(ms_list), 2 * weight)

        ms_list_min = self.smr.min(ms_list, ms_list1)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.min(ms_list1, ms_list)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list2 = self.make_cart_list(n=10)
        ms_list_min = self.smr.min(ms_list1, ms_list2)
        self.assertIs(ms_list1, ms_list_min)

    def test_min_none(self):
        ms_list1 = self.make_cart_list()
        weight = len(ms_list1)

        ms_list_min = self.smr.min(ms_list1, None)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.max(None, ms_list1)
        self.assertEqual(len(ms_list_min), len(ms_list1))

        ms_list_min = self.smr.min(None, None)
        self.assertEqual(len(ms_list_min), 0)

    def test_smr_save_current_states(self):
        n = 10 # number of Cart instances in list 
        ms_list1 = self.make_cart_list(n=n)

        # store current cart
        self.smr.save_current_states()
        cart_old = self.smr.sm_curr._cart

        # extract one of the Cart instances
        cart = ms_list1[0]
        self.assertIsInstance(cart, Cart)
        # cart model state got updated in sum 
        # so it is different from cart_old
        self.assertNotEqual(cart._position, cart_old._position)
        self.assertNotEqual(cart._velocity, cart_old._velocity)

    def test_sum_cart(self):
        n = 10 # number of Cart instances in list 
        ms_list1 = self.make_cart_list(n=n)
        weight = len(ms_list1)

        # sum to ServerModel
        sm_sum = self.smr.sum(ms_list1)
        self.assertNotEqual(sm_sum, CartpoleServer)
        self.assertIsInstance(sm_sum, CartpoleServer)

        cart = sm_sum._cart
        self.assertIsInstance(cart, Cart)
        
        # all entries in ms_list1 are the same
        # so, we select randomly one
        mean_clist_pos = ms_list1[random.randint(0, n-1)]._position
        mean_clist_vel = ms_list1[random.randint(0, n-1)]._velocity
        mean_clist_dir = ms_list1[random.randint(0, n-1)]._direction
        self.assertEqual(mean_clist_pos, cart._position)
        self.assertEqual(mean_clist_vel, cart._velocity)
        self.assertEqual(mean_clist_dir, cart._direction)

    def test_sum_pole(self):
        n = 10 # number of Cart instances in list 
        ms_list1 = self.make_pole_list(n=n)
        weight = len(ms_list1)
        # modify list: enumerate position and velocity
        for count,elem in enumerate(ms_list1):
            ms_list1[count] = Pole(angle=count, velocity=count)

        # sum to ServerModel
        sm_sum = self.smr.sum(ms_list1)
        self.assertNotEqual(sm_sum, CartpoleServer)
        self.assertIsInstance(sm_sum, CartpoleServer)

        pole = sm_sum._pole
        self.assertIsInstance(pole, Pole)

        # manual calc of mean
        # As all cart instances in ms_list1 are the same
        # the mean equals each cart
        mean_clist_vel = statistics.mean(range(weight))
        mean_clist_ang = statistics.mean(range(weight))
        self.assertEqual(mean_clist_vel, pole._velocity)
        self.assertEqual(mean_clist_ang, pole._angle)

    # adds carts with varying values
    def test_sum_cart_mean(self):
        n = 10 # number of Cart instances in list 
        ms_list1 = self.make_cart_list(n=n)
        weight = len(ms_list1)
        # modify list: enumerate position and velocity
        for count,elem in enumerate(ms_list1):
            ms_list1[count] = Cart(position=count,
                                velocity=count,
                                direction=ms_list1[count]._direction)

        # sum to ServerModel
        sm_sum = self.smr.sum(ms_list1)
        cart = sm_sum._cart
        
        # manual calc of mean
        mean_clist_pos = statistics.mean(range(weight))
        mean_clist_vel = statistics.mean(range(weight))
        mean_clist_dir = ms_list1[random.randint(0, n-1)]._direction
        self.assertEqual(mean_clist_pos, cart._position)
        self.assertEqual(mean_clist_vel, cart._velocity)
        self.assertEqual(mean_clist_dir, cart._direction)

    # adds up an empty list
    def test_sum_empty(self):
        ms_list1 = []
        sm_sum = self.smr.sum(ms_list1)
        # we expect a ServerModel instance with None vars only
        self.assertIsInstance(sm_sum, CartpoleServer)
        for var in vars(sm_sum):
            self.assertIsNone(vars(sm_sum)[var])

    # add up None
    def test_sum_none(self):
        ms_list1 = None
        sm_sum = self.smr.sum(ms_list1)
        # we expect a ServerModel instance with None vars only
        self.assertIsInstance(sm_sum, CartpoleServer)
        for var in vars(sm_sum):
            self.assertIsNone(vars(sm_sum)[var])

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_ServerModelRegression)
    unittest.TextTestRunner(verbosity=2).run(suite)
