
import os, sys

# auto-loading classes from test_*.py
path = os.path.dirname(os.path.abspath(__file__))
for py in [f[:-3] for f in os.listdir(path) if f.endswith('.py') 
            and not f.endswith('__init__.py')
            and not f.endswith('test_all.py') 
            and not f.endswith('conftest.py')]:
    mod = __import__('.'.join([py]), fromlist=[py])
    classes = [getattr(mod, x) for x in dir(mod) if isinstance(getattr(mod, x), type)]
    for cls in classes:
        setattr(sys.modules[__name__], cls.__name__, cls)

import unittest

if __name__ == '__main__':
    # add each TestCase to TestSuite
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Test_CartpoleServer)
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_GP_TestDefaultController))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_MonkeyPatching))
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(Test_ServerModel))
    # run suite
    unittest.TextTestRunner(verbosity=2).run(suite)
