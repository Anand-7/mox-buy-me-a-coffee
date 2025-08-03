from src import buy_me_a_coffee
from moccasin.config import get_active_network

def withdraw():
    # coffee = buy_me_a_coffee.at("0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512")
    active_network = get_active_network()
    coffee = active_network.manifest_named("buy_me_a_coffee")
    # coffee = active_network.get_latest_contract_unchecked("coffee_contract")
    print(f"Working with contract {coffee.address}")
    coffee.withdraw()

def moccasin_main():
    return withdraw()