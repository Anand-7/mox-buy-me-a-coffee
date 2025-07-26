from src.mocks import mock_aggregatorV3
from moccasin.config import VyperContract

STARTING_DECIMALS = 8
STARTING_PRICE = int(2000e8)

def deploy_aggregatorV3_feed() -> VyperContract:
    return mock_aggregatorV3.deploy(STARTING_DECIMALS, STARTING_PRICE) 

def moccasin_main() -> VyperContract:
    return deploy_aggregatorV3_feed()