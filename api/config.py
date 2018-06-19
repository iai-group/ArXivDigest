# -*- coding: utf-8 -*-
__author__ = "Øyvind Jekteberg and Kristian Gingstad"
__copyright__ = "Copyright 2018, The ArXivDigest Project"

import json
import os

with open(os.path.dirname(__file__) + '/../config.json', 'r') as f:
    config = json.load(f)
    APIconfig = config.get('api_config')
