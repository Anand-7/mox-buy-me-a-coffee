from script.deploy import deploy_coffee
from script.deploy import deploy_aggregatorV3_feed
import pytest
from moccasin.config import get_active_network
from eth_utils import to_wei
import boa

SEND_VALUE = to_wei(0.0008, "ether")

@pytest.fixture(scope= "session")
def account():
    return get_active_network().get_default_account()

@pytest.fixture(scope= "session")
def eth_usd_price_feed():
    return deploy_aggregatorV3_feed()

@pytest.fixture(scope = "function")
def coffee_contract(eth_usd_price_feed):
    return deploy_coffee(eth_usd_price_feed.address)

@pytest.fixture(scope= "function")
def coffee_funded(coffee_contract, account):
    boa.env.set_balance(account.address, SEND_VALUE)
    with boa.env.prank(account.address):
        coffee_contract.fund(value = SEND_VALUE)
    return coffee_contract

