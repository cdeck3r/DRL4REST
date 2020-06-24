import conftest

import unittest
from cartpole.gprest.server_model import CartpoleServer
from openapi_server.models import Cart

class Test_CartpoleServer(unittest.TestCase):
    # small test routine for the CartpoleServer
      
    def setUp(self):
        self.s=CartpoleServer
        self.cps_crud_func = [func for func in dir(self.s) if callable(getattr(self.s, func)) 
               and not func.startswith('__')
               and not func.startswith('reset')]
        
    def test_CartpoleServer(self):
        self.s.reset()

        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

        self.s.create_cart()
        c = self.s.read_cart()
        self.assertTrue( isinstance(type(c), type(Cart)) )

        c2 = self.s.read_cart()
        assert c == c2
        self.assertEqual(c.to_dict(), c2.to_dict())

        self.s.delete_cart()
        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

        self.s.create_cart()
        c = self.s.read_cart()
        self.assertTrue( isinstance(type(c), type(Cart)) )
        c2 = self.s.read_cart()
        self.assertEqual(c, c2)
        self.assertEqual(c.to_dict(), c2.to_dict())

        self.s.reset()
        c = self.s.read_cart()
        self.assertEqual(type(c), type(None))

    def _crud_funcs(self, model_name):
        model_crud = [crud_func + '_' + model_name for crud_func in ['create', 'read', 'update', 'delete']] 
        cps_model_func = [m for m in self.cps_crud_func if m.endswith(model_name)]

        self.assertEqual(set(cps_model_func), set(model_crud)) 

    def test_CRUD_cart(self):
        model_name = 'cart'
        self._crud_funcs(model_name)        

    def test_CRUD_pole(self):
        model_name = 'pole'
        self._crud_funcs(model_name)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_CartpoleServer)
    unittest.TextTestRunner(verbosity=2).run(suite)