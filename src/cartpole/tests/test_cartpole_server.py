import random
import unittest
from cartpole.gprest.server_model import CartpoleServer
from openapi_server.models import Cart
from openapi_server.models import Pole


class Test_CartpoleServer(unittest.TestCase):
    # small test routine for the CartpoleServer

    def setUp(self):
        self.s = CartpoleServer
        self.cps_crud_func = [
            func for func in dir(self.s)
            if callable(getattr(self.s, func))
            and not func.startswith('__')
            and not func.startswith('reset')
        ]
        self.s.reset()

    def test_CartpoleServer(self):
        self.s.reset()

        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

        self.s.create_cart()
        c = self.s.read_cart()
        self.assertTrue(isinstance(type(c), type(Cart)))

        c2 = self.s.read_cart()
        assert c == c2
        self.assertEqual(c.to_dict(), c2.to_dict())

        self.s.delete_cart()
        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

        self.s.create_cart()
        c = self.s.read_cart()
        self.assertTrue(isinstance(type(c), type(Cart)))
        c2 = self.s.read_cart()
        self.assertEqual(c, c2)
        self.assertEqual(c.to_dict(), c2.to_dict())

        self.s.reset()
        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

    def _crud_funcs(self, model_name):
        model_crud = [
            crud_func + '_' + model_name
            for crud_func in ['create', 'read', 'update', 'delete']
        ]
        cps_model_func = [
            m for m in self.cps_crud_func if m.endswith(model_name)
        ]

        self.assertEqual(set(cps_model_func), set(model_crud))

    def test_CRUD_cart(self):
        model_name = 'cart'
        self._crud_funcs(model_name)

    def test_CRUD_pole(self):
        model_name = 'pole'
        self._crud_funcs(model_name)

    def test_instances_wo_data(self):
        self.s.n_instances(init_w_data=False)

        for inst in self.s._instances:
            self.assertIsInstance(vars(inst)['_cart'], type(None))
            self.assertIsInstance(vars(inst)['_pole'], type(None))
            self.assertIsInstance(vars(inst)['_direction'], type(None))

    def test_instances_const_data(self):
        self.s.create_cart()
        self.s.create_pole()
        # create_direction() is not implemented because there is no REST interface

        # instances have const data from above
        self.s.n_instances(init_w_data=False)
        # by default, we have 10 instances
        self.assertEqual(len(self.s._instances), 10)

        # all instances have the right type
        for inst in self.s._instances:
            self.assertIsInstance(vars(inst)['_cart'], Cart)
            self.assertIsInstance(vars(inst)['_pole'], Pole)
            self.assertIsInstance(vars(inst)['_direction'], type(None))

        # assert all have the same data
        all_inst = self.s._instances
        self.assertTrue(all(vars(x) == vars(all_inst[0]) for x in all_inst))

    def test_instances_init_data(self):
        num_instances = random.randint(1, 100)

        # instances have data from create_* functions
        self.s.n_instances(n=num_instances)
        # by default, we have 10 instances
        self.assertEqual(len(self.s._instances), num_instances)

        # all instances have the right type
        for inst in self.s._instances:
            self.assertIsInstance(vars(inst)['_cart'], Cart)
            self.assertIsInstance(vars(inst)['_pole'], Pole)
            self.assertIsInstance(vars(inst)['_direction'], type(None))

        # assert all are different
        all_inst = self.s._instances
        self.assertEqual(len(set(all_inst)), num_instances)
        self.assertTrue(any(vars(x) == vars(all_inst[0]) for x in all_inst))


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_CartpoleServer)
    unittest.TextTestRunner(verbosity=2).run(suite)
