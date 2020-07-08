# coding: utf-8

import random
import math 
import copy
from openapi_server.models import Cart
from openapi_server.models import Pole
from openapi_server.models import Direction


class ServerModelRegression(object):
    """Runs a regression on a given ServerModel

    This class defines the primitive operations for a regression on the states of a ServerModel.
    """
    def __init__(self, sm):
        self.sm = sm
        self.ms_names = self.sm.states_varnames()
        self.sm_curr = None
        self.ms_list = []

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

    def sum(self, ms_list):
        pass