#
# This is the implemenation of the collection controller
# The server's controller is 
# DRL4REST/openapi/cartpole/python-flask/openapi_server/controllers
#

# flake8: noqa
from __future__ import absolute_import
# import models into model package
from openapi_server.models.cart import Cart
from openapi_server.models.direction import Direction
from openapi_server.models.pole import Pole


from random import random
from random import choice

def cart_get():  # noqa: E501
    # just return a Cart object with random values

    position = random()
    velocity = random()
    direction = choice(["left", "right"]) 

    return Cart(position=position, velocity=velocity, direction=direction)

