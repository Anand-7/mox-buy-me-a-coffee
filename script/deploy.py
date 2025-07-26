from moccasin.config import get_active_network
from src import buy_me_a_coffee
from moccasin.boa_tools import VyperContract
from script.deploy_mocks import deploy_aggregatorV3_feed

def deploy_coffee(price_feed: VyperContract) -> VyperContract:
    coffee_contract: VyperContract = buy_me_a_coffee.deploy(price_feed)
    # active_network = get_active_network()
    # if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
    #     result = active_network.moccasin_verify(coffee_contract)
    #     result.wait_for_verification()
    return coffee_contract

def moccasin_main() -> VyperContract:
    active_network = get_active_network()
    # Deploys the price feed based on the network
    print(f" Active Network : {active_network}")
    price_feed: VyperContract = active_network.manifest_named("price_feed")
    print(f"On Network {active_network.name}, using price feed {price_feed.address}")
    # price_feed : VyperContract = deploy_aggregatorV3_feed()
    # coffee_contract = buy_me_a_coffee.deploy(price_feed)
    # print(f"Coffe contract deployed at {coffee_contract.address}")
    # print(coffee_contract.get_eth_to_usd_rate(10000))
    return deploy_coffee(price_feed)
    # if active_network.name == "Sepolia":
    #     price_feed = "0x694AA1769357215DE4FAC081bf1f309aDC325306"
