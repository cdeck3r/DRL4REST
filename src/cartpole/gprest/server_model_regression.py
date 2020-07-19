# coding: utf-8

import random
import math 
import copy
import statistics
from openapi_server.models import Cart
from openapi_server.models import Pole
from openapi_server.models import Direction
from cartpole.gprest.server_model import CartpoleServer


class ServerModelRegression(object):
    """Runs a regression on a given ServerModel

    This class defines the primitive operations for a regression on the states of a ServerModel.
    """
    def __init__(self, sm):
        self.sm = sm
        self.ms_names = self.sm.states_varnames()
        self.sm_curr = None
        self.ms_list = []
        self.sm_regressand = None

    # makes a deep copy of the current model states of the ServerModel
    def save_current_states(self):
        # create a ServerModel Instance
        self.sm_curr = self.sm()
        # deep copy state variabls into current ServerModel instance
        for var in self.ms_names:
            ms_val = vars(self.sm)[var]
            setattr(self.sm_curr, var, copy.deepcopy(ms_val))

    def sel_ms(self):
        return random.choice(self.ms_names)

    # add SeverModel state to list and returns list
    # that is: weight * ms[inst_num]
    def add(self, weight, ms, inst_num):
        _ms_list = []
        inst = self.sm._instances[inst_num]
        ms_inst = vars(inst)[ms]
        if ms_inst is not None:
            _ms_list.extend([ms_inst for i in range(weight)])
        return _ms_list

    # concat two lists and returns it
    # works with None for one or both params 
    def concat(self, ms_list1, ms_list2):
        _ms_list = []
        if ms_list1 is not None:
            _ms_list.extend(ms_list1)
        if ms_list2 is not None:
            _ms_list.extend(ms_list2)
        return _ms_list

    # returns the longer list
    # if both are equal, it will return ms_list1
    def max(self, ms_list1, ms_list2):
        _ms_list = []
        if ms_list1 is None and ms_list2 is None:
            return _ms_list

        if ms_list1 is None:
            return ms_list2 
        if ms_list2 is None:
            return ms_list1

        if len(ms_list1) >= len(ms_list2):
            return ms_list1
        else:
            return ms_list2

    # returns the longer list
    # if both are equal, it will return ms_list1
    def min(self, ms_list1, ms_list2):
        _ms_list = []
        if ms_list1 is None and ms_list2 is None:
            return _ms_list

        if ms_list1 is None:
            return ms_list2 
        if ms_list2 is None:
            return ms_list1

        if len(ms_list1) <= len(ms_list2):
            return ms_list1
        else:
            return ms_list2


class CartpoleServerRegression(ServerModelRegression):
    """Runs a regression on the Cartpole ServerModel

    This class defines the primitive operations specific for the CartpoleServer.
    """

    class CartpoleSum(object):
        """Sums model states by type, i.e. Cart, Pole, Direction.

        """
        def __init__(self):
            # list of model states in CartpoleServer
            self._cart_list = []
            self._pole_list = []
            self._direction_list = []
            # model states, make them explicity by defining them
            self._cart = None
            self._pole = None
            self._direction = None

        def sum_cart(self):
            position = statistics.mean([c.position for c in self._cart_list])
            velocity = statistics.mean([c.velocity for c in self._cart_list])
            direction_left = [c.direction for c in self._cart_list].count('left')
            direction_right = [c.direction for c in self._cart_list].count('right')
            if direction_left >= direction_right:
                direction = 'left'
            else:
                direction = 'right'
            self._cart = Cart(position=position, velocity=velocity, direction=direction)

        def sum_pole(self):
            angle = statistics.mean([p.angle for p in self._pole_list])
            velocity = statistics.mean([p.velocity for p in self._pole_list])
            self._pole = Pole(angle=angle, velocity=velocity)

        def sum_direction(self):
            direction_left = [d.direction for d in self._direction_list].count('left')
            direction_right = [d.direction for d in self._direction_list].count('right')
            if direction_left >= direction_right:
                direction = 'left'
            else:
                direction = 'right'
            self._direction = Direction(direction=direction)

        def __add__(self, ms):
            if isinstance(ms, Cart):
                self._cart_list.append(ms)
                self.sum_cart()
            elif isinstance(ms, Pole):
                self._pole_list.append(ms)
                self.sum_pole()
            elif isinstance(ms, Direction):
                self._direction_list.append(ms)
                self.sum_direction()

            return self

    def __init__(self):
        super().__init__(CartpoleServer)

    # sum is specific for CartpoleServer
    # it computes avg values across model states
    def sum(self, ms_list):
        # uses the builtin sum operation
        # providing a start object with overrides add operator
        # to add each element of ms_list 
        cs = self.CartpoleSum()
        if ms_list is not None:
            cs = sum(ms_list, cs)

        # create ServerModel instance as regressand
        self.sm_regressand = self.sm()
        for var in self.ms_names:
            try:
                ms_val = vars(cs)[var]
                setattr(self.sm_regressand, var, ms_val)
            except:
                # var does not exist in sum object, so continue
                continue

        return self.sm_regressand