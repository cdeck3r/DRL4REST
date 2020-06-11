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