import unittest
from cartpole.gprest.gp_test_default_controller import GP_TestDefaultController
from openapi_server.models import Cart


class Test_GP_TestDefaultController(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gp_test = GP_TestDefaultController()

    def setUp(self):
        self.gp_test = Test_GP_TestDefaultController.gp_test

    def test_default(self):
        gp_cart = self.gp_test.test_cart_get()
        gp_cart = Cart.from_dict(gp_cart.json)
        self.assertIsInstance(gp_cart, Cart)


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        Test_GP_TestDefaultController
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
