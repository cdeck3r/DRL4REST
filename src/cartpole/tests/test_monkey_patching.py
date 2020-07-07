import unittest
from cartpole.gprest.gp_test_default_controller import GP_TestDefaultController

# functions replacing the default controller by Monkey Patching
from openapi_server.models import Cart


def testcase_all_correct():
    return Cart(position=1.1, velocity=2.2, direction='left')


def testcase_empty_return_object():
    return Cart()


def testcase_return_none():
    return None


def testcase_program_with_exception():
    raise Exception('Program raises an exception')


def testcase_return_string_type():
    return 'some string'


def testcase_return_obj_type():
    return type('obj', (object,), {'attribute' : 'attribute value'})


# the testcase with test methods
class Test_MonkeyPatching(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.gp_test = GP_TestDefaultController()

    def setUp(self):
        self.url_path = '/api/v1/cart'
        self.gp_test = Test_MonkeyPatching.gp_test

    def test_all_correct(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_all_correct
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()

    def test_empty_return_object(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_empty_return_object
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()

    @unittest.expectedFailure
    def test_return_none(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_return_none
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()

    @unittest.expectedFailure
    def test_program_with_exception(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_program_with_exception
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()

    @unittest.expectedFailure
    def test_return_string_type(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_return_string_type
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()

    @unittest.expectedFailure
    def test_return_obj_type(self):
        ret = self.gp_test.endpoint_config(
            self.url_path, 'get', testcase_return_obj_type
        )
        self.assertTrue(ret)
        self.gp_test.test_cart_get()


if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(
        Test_MonkeyPatching
    )
    unittest.TextTestRunner(verbosity=2).run(suite)
