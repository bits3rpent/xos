import os
import base64
from planetstack.config import Config

class Deleter:
	model=None # Must be overridden

        def __init__(self, *args, **kwargs):
                pass

	def call(self, pk, model_dict):
		# Fetch object from PlanetStack db and delete it
		pass

	def __call__(self, *args, **kwargs):
		return self.call(*args, **kwargs)
