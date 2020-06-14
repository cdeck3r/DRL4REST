
# coding: utf-8

import random
import math 
from openapi_server.models import Cart
from openapi_server.models import Pole

class CartpoleServer(object):

    """ `CartpoleServer` is the implementation of the ServerModel. 
    
    The ServerModel is a static class. The GP controller utilizes the model to store state between successive calls. The ServerModel provides CRUD functions for state access and manipulation.
    """

    # state as class variable
    _cart = None
    _pole = None
    _direction = None

    # set the class in a defined (initial) state
    @classmethod
    def reset(cls):
        cls._cart = None
        cls._pole = None
        cls._direction = None
    
    @classmethod
    def create_cart(cls):
        position = random.random()
        velocity = random.random()
        # we know the values from the models, e.g.
        #   models/cart.py or models/direction.py
        direction = random.choice(['left', 'right'])
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

    @classmethod
    def create_pole(cls):
        angle = math.pi * random.random()
        velocity = random.random()
        # we know the values from the models, e.g.
        #   models/pole.py 
        cls._pole = Pole(angle=angle, velocity=velocity)

    @classmethod
    def read_pole(cls):
        return cls._pole
    
    @classmethod
    def update_pole(cls):
        # there is no PUT method in the spec
        pass

    @classmethod
    def delete_pole(cls):
        cls._pole = None

    @classmethod
    def create_direction(cls):
        direction = random.choice(['left', 'right'])
        # we know the values from the models, e.g.
        #   models/pole.py 
        cls._direction = Direction(direction=direction)

    @classmethod
    def read_direction(cls):
        return cls._direction
    
    @classmethod
    def update_direction(cls, direction):
        cls._direction = direction

    @classmethod
    def delete_direction(cls):
        cls._direction = None


#############################################
#
#############################################

def add_CRUD_pset(pset, sm, model_name):
    """Adds the ServerModel CRUD function to the Primitve Set
    
    Parameters
    ----------
    pset : PrimitiveSet
        the primitive set for adding the controller functions
    sm : ServerModel
        the ServerModel with the CRUD functions
    model_name : str
        the name of the OpenAPI model referring to its CRUD functions in the ServerModel ['cart' | 'pole' | 'direction']
        
    Returns
    -------
    PrimitiveSet
        the primitive set containing the ServerModel's CRUD function
    """
    def pset_cart():
        # cart CRUD functions
        pset.addTerminal(sm.create_cart)
        pset.addTerminal(sm.read_cart)
        pset.addTerminal(sm.update_cart)
        pset.addTerminal(sm.delete_cart)

    def pset_pole():
        # cart CRUD functions
        pset.addTerminal(sm.create_pole)
        pset.addTerminal(sm.read_pole)
        pset.addTerminal(sm.update_pole)
        pset.addTerminal(sm.delete_pole)
        
    def pset_direction():
        # cart CRUD functions
        pset.addTerminal(sm.create_direction)
        pset.addTerminal(sm.read_direction)
        pset.addTerminal(sm.update_direction)
        pset.addTerminal(sm.delete_direction)

    options = {
        'cart': pset_cart,
        'pole': pset_pole,
        'direction': pset_direction,
    }

    # add CRUD functions to pset
    options[model_name]()
    return pset