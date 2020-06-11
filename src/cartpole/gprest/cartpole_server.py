
# coding: utf-8

import random
from openapi_server.models import Cart

class CartpoleServer(object):

    """ `CartpoleServer` is the implementation of the ServerModel. 
    
    The ServerModel is a static class. The GP controller utilizes the model to store state between successive calls. The ServerModel provides CRUD functions for state access and manipulation.
    """

    # state as class variable
    _cart = None

    # set the class in a defined (initial) state
    @classmethod
    def reset(cls):
        cls._cart = None
    
    @classmethod
    def create_cart(cls):
        position = random.random()
        velocity = random.random()
        # we know the values from the models, e.g.
        #   models/cart.py or models/direction.py
        direction = random.choice(["left", "right"])
        cls._cart = Cart(position=position, velocity=velocity, direction=direction)

    @classmethod
    def read_cart(cls):
        return cls._cart
    
    @classmethod
    def update_cart(cls):
        if isinstance(cls._cart, Cart):
            cls._cart.direction='left'

    @classmethod
    def delete_cart(cls):
        cls._cart = None