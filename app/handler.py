import os
import uuid
import json
from glob import glob
import numpy as np
import requests
import pandas as pd

import tornado.web
from tornado import concurrent
from tornado import gen
from concurrent.futures import ThreadPoolExecutor
from functools import singledispatch

from app.base_handler import BaseApiHandler
from app.settings import MAX_MODEL_THREAD_POOL
from source.color_extractor import getColorTag

class IndexHandler(tornado.web.RequestHandler):
    """APP is live"""
    def get(self):
        """Return Index Page"""
        print("In Get")
        self.write({"status" : True})

    def head(self):
        """Verify that App is live"""
        self.finish()

    def post(self):
        print("In POST")
        data = tornado.escape.json_decode(self.request.body)
        product_line = data["product_line"]
        weights_type = data["weights_type"]
        image_links = data["image_links"]
        result = getColorTag(product_line, weights_type, image_links)
        return self.write(result)
