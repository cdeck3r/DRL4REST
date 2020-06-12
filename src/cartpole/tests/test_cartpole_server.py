import conftest

import unittest
from cartpole.gprest.cartpole_server import CartpoleServer
from openapi_server.models import Cart

class Test_CartpoleServer(unittest.TestCase):
    # small test routine for the CartpoleServer
      
    def setUp(self):
        self.s=CartpoleServer
        
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

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_CartpoleServer)
    unittest.TextTestRunner(verbosity=2).run(suite)