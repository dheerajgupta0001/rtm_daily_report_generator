import json
import pandas as pd
from typing import List, Any

jsonConfig: dict = {}


def initConfigs():
    loadJsonConfig()


def loadJsonConfig(fName="config.json") -> dict:
    global jsonConfig
    with open(fName) as f:
        data = json.load(f)
        jsonConfig = data
        return jsonConfig


def getJsonConfig() -> dict:
    global jsonConfig
    return jsonConfig