import conftest

import unittest
from deap import gp
from cartpole.gprest.server_model import CartpoleServer
import cartpole.gprest.server_model as sm

class Test_ServerModel(unittest.TestCase):
    # small test routine for the ServerModel
      
    def setUp(self):
        self.s=CartpoleServer
        self.cps_crud_func = [func for func in dir(self.s) if callable(getattr(self.s, func)) 
               and not func.startswith('__')
               and not func.startswith('reset')]
    
    def _crud_funcs(self, model_name):
        cps_model_func = [m for m in self.cps_crud_func if m.endswith(model_name)]
        pset = gp.PrimitiveSet("MAIN", 0)
        pset = sm.add_CRUD_pset(pset, self.s, model_name)
        crud_func = [f for f in pset.mapping]
        self.assertEqual(set(crud_func), set(cps_model_func))

    def test_add_cart_CRUD(self):
        model_name = 'cart'
        self._crud_funcs(model_name)

    def test_add_pole_CRUD(self):
        model_name = 'pole'
        self._crud_funcs(model_name)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_ServerModel)
    unittest.TextTestRunner(verbosity=2).run(suite)