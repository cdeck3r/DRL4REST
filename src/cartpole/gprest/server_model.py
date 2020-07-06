
# coding: utf-8

import random
import math 
import copy
from openapi_server.models import Cart
from openapi_server.models import Pole
from openapi_server.models import Direction

class CartpoleServer(object):

    """ `CartpoleServer` is the implementation of the ServerModel. 
    
    The ServerModel is a static class. The GP controller utilizes the model to store state between successive calls. The ServerModel provides CRUD functions for state access and manipulation.
    """

    # state as class variable
    _cart = None
    _pole = None
    _direction = None

    # stores data from client
    _from_client = None

    # list of ServerModel instances
    _instances = None

    # set the class in a defined (initial) state
    @classmethod
    def reset(cls):
        cls._cart = None
        cls._pole = None
        cls._direction = None
        cls._from_client = None
    
    # creates n instances of the ServerModel
    # it is a factory method
    @classmethod
    def n_instances(cls, n=10, init_w_data=True):
        create_methods = [k for k in dir(cls) if k.startswith('create')]

        def init_data():
            for c in create_methods:
                try:
                    # calls all create_* methods  
                    vars(cls)[c].__get__(None, cls)()
                except:
                    pass

        # reset instances
        cls._instances = []
        for i in range(n):
            # 1. create instance 
            inst = cls()
            # 2. add class vars as instance vars
            cls_vars = [k for k in dir(cls)
                        if not k.startswith(('__', 'create', 'read', 'update', 'delete', 'reset')) # standard CRUD
                        and not k.startswith(('_from_client')) # data 
                        and not k.startswith(('_instances', 'n_instances')) # other methods and vars
                        ]
            # 3. init class with data 
            if init_w_data:
                init_data()
            # 4. ... and deep copy the class vars into instance vars
            for var in cls_vars:
                org_val = vars(cls)[var]
                setattr(inst, var, copy.deepcopy(org_val))
            # 5. add to list
            cls._instances.append(inst)

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
        # this check makes the operation safe
        if isinstance(cls._cart, Cart) and cls._from_client is not None:
            # encapsulating makes the operation safe when process. data
            try:
                # 1. de-serialize _from_client
                # 2. update
                # 3. reset _from_client data
                direction_from_client = Direction.from_dict(cls._from_client) 
                if isinstance(direction_from_client, Direction):
                    cls._cart.direction = direction_from_client.direction
                    cls._from_client = None
            except: 
                # someting went wrong, we can't handle
                pass

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
        raise NotImplementedError("Direction have no create method")
    
    @classmethod
    def read_direction(cls):
        raise NotImplementedError("Direction have no read method")

    @classmethod
    def update_direction(cls):
        raise NotImplementedError("Direction have no read method")

    @classmethod
    def delete_direction(cls):
        raise NotImplementedError("Direction have no delete method")

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
        
    options = {
        'cart': pset_cart,
        'pole': pset_pole,
    }

    # add CRUD functions to pset
    options[model_name]()
    return pset