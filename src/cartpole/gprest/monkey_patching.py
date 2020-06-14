# coding: utf-8

class MonkeyPatching:
    """Monkey patching changes the default behavior of a piece of code at runtime without changing its original source. 
    
    For example, we want to change the behavior of the default controller function prototype `cart_get()`. Monkey patching replaces the prototype by the GP controller. When running the testcases, the GP controller gets executed instead of the default controller.

    Attributes
    ----------
    app : FlaskApp
        a FlasApp object

    Methods
    -------
    patch(url_path, method, controller_func)
        Replaces endpoint's controller function

    """

    def __init__(self, app=None):
        self._rules = []
        self._app = app
    
    @property
    def app(self):
        return self._app
    
    @app.setter
    def app(self, app):
        self._app = app
    
    def _endpoint_exists(self, url_path, method):
        """test if endpoint config exists

        Parameters
        ----------
        url_path : str
            endpoint url path, e.g. /api/v1/cart

        method : str 
            HTTP request method, e.g. GET, POST, etc.

        """
        self._rules = []
        
        for r in self._app.url_map.iter_rules():
            if (url_path == str(r)) and (method.upper() in r.methods):
                self._rules.append(r)
                return True
        return False

    # gets the endpoint's view function
    # returns the default controller functio
    def _unwrap(self, view_func):
        wrapped_func = view_func
        try:
            while wrapped_func.__wrapped__ :
                wrapped_func = wrapped_func.__wrapped__
        except Exception:
            # this is the default_controller_func
             return wrapped_func
    
    # 
    def patch(self, url_path, method, controller_func):
        """Replaces endpoint's controller function with the one from the parameters

        Parameters
        ----------
        url_path : str
            endpoint url path, e.g. /api/v1/cart

        method : str 
            HTTP request method, e.g. GET, POST, etc.

        controller_func : function
            Controller function replacing the original one

        """

        if self._endpoint_exists(url_path, method):
            rule = self._rules[0]
            view_func = self._app.view_functions[rule.endpoint]
            default_controller_func = self._unwrap(view_func)
            default_controller_func.__code__ = controller_func.__code__
            return True
        
        return False

class GP_Controller:
    """Encapsulates the gp_controller function for execution

    MonkeyPatching requires a function with a `__code__` section. However, the GP created controller program is a partial function, which does not have a `__code__` section. As a consequence, the `GP_Controller` static class wraps the GP created partial function into a function with a `__code__` section.

    Src: https://stackoverflow.com/questions/56881670/partial-function-object-has-no-attribute-code
    
    """
    
    _gp_controller = None
    
    @classmethod
    def set_controller_func(cls, func):
        cls._gp_controller = func

    @staticmethod
    def gp_controller_func():
        """ Runs the gp_controller.
        
            gp_controller_func is called from a different scope, so it needs to 
            search through all imported modules for the GP_Controller class in
            order to access the class variable _gp_controller.

            CAUTION: 
            This is fragile. It finds the first occurance of the GP_Controller
            within all imported modules.
        """
        gpc_pointer = None
        for m_name in sys.modules:
            try:
                gpc_pointer = getattr(sys.modules[m_name], 'GP_Controller')
                break
            except AttributeError:
                continue
        return gpc_pointer._gp_controller()
    
gpc = GP_Controller