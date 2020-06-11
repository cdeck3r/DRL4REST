# coding: utf-8

from openapi_server.test.test_default_controller import TestDefaultController
from cartpole.gprest.monkey_patching import MonkeyPatching

class GP_TestDefaultController(TestDefaultController):
    """Extends the unit tests from the TestDefaultController in order to enable additional checks of the response data. 
    
    The OpenAPI generator creates the unittest `TestDefaultController` containing test mesthods for each default controller. This class extends 
    them for GP's `evaluate()` function. 

    Furthermore, this class enables the Monkey Patching of the controller function. As a result, the `test_cart_get()` function from this class actually tests the GP controller function.
    """

    def __init__(self, mp=MonkeyPatching(), app_config_testing=True, assert_score=1000):
        """
        Parameters
        ----------
        mp : MonkeyPatching, optional
            Contains functions for patching the controller (default is MonkeyPatching()) 
        app_config_testing : bool, optional
            Sets the FlaskApp in testing mode (defaul is True)
        assert_score : int, optional
            Score, if an exception occurs during testing (default is 1000)
        """
        super().__init__()
        self.app = super().create_app()
        self.app.config['TESTING'] = app_config_testing
        self.client = self.app.test_client()
       
        # associate with MonkeyPatching
        self.mp = mp
        self.mp.app = self.app    
        
        # score for response evaluation
        self._score = -1
        self._assert_score = assert_score
        
        self._prev_responses = []

        
    @property
    def score(self):
        return self._score
    
    @score.setter
    def score(self, s):
        if s < 0:
            self._score = -1
        else:
            self._score = s
        
    def reset_score(self):
        self.score = -1
        self._prev_responses = []
        
    def score_response(self, resp):
        """Quantify the response, we use the status code as score

        Parameters
        ----------
        resp : Response
            Flask Response object

        """
        # src: https://stackoverflow.com/a/3844832
        def checkEqualEntries(iterator):
            return len(set(iterator)) <= 1
        
        # store the response body
        self._prev_responses.append(str(resp.json))
        # compare all responses 
        if len(self._prev_responses) > 1 and checkEqualEntries(self._prev_responses):
            # expect them the same, neutralize increasing score to keep them small
            self.score -= resp.status_code
        
        self.score += resp.status_code
    
    def endpoint_config(self, url_path, method, controller_func):
        """Changes the behavior of a url_path with a new controller function
        
        Returns True if endpoint was found and successfully patched

        Limits: 
        * works only if method is unique for url_path 
        * does not support aliases
        """
        return self.mp.patch(url_path, method, controller_func)

    def test_cart_get(self):
        """Overrides the default test_cart_get()

           Checks for the correct content_type in the responds.
        """
        response = super().test_cart_get() #assert200(response)
        # add another important assertion
        self.assertEqual(response.content_type, 
                    'application/vnd.cartpole.cart+json', 
                    'Please check the openapi.yaml for unique content-type in response section'
                   )
        return response

    # safe version of test_cart_get(), i.e. avoids exceptions 
    def safe_test_cart_get(self):
        try:
            response = super().test_cart_get() #assert200(response)        
            self.assertEqual(response.content_type, 
                        'application/vnd.cartpole.cart+json', 
                        'Please check the openapi.yaml for unique content-type in response section'
                       )
        except AssertionError as error:
            # score an assertion
            self.score += self._assert_score
            return
            
        self.score_response(response)