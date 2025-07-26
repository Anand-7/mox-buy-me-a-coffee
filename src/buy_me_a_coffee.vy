# pragma version ^0.4.0

# Natspec Metadata
"""
@license MIT
@title Buy Me A Coffee
@author Me!
@notice This contract is for creating a sample funding contract
"""
# get funds from users
# Withdraw funds
# set a minimum funding value in usd

# ABI: ABI is a specification of how different apps can interact with the smart contract 
# AggregatorV3Interface gives the ABI
from interfaces import AggregatorV3Interface
import get_price_module
# No need to initialize get_price_module, since get_price_module module doesn't have any storage variable only constant variable

# Constants & Immutables reduces the usage of gas
# Constants are not stored in storage slots, but are stored directly as part of contract's bytecode
MINIMUM_USD : public(constant(uint256)) = 2 * (10**18) #since we will need to compare the eth/usd price having 18 decimals
# MINIMUM_USD : public(constant(uint256)) = as_wei_value(5, 'ether')
PRICE_FEED : public(immutable(AggregatorV3Interface)) #0x694AA1769357215DE4FAC081bf1f309aDC325306 -> Sepolia USD/ETH
OWNER : public(immutable(address))

# storage variables
funders : public(DynArray[address, 1000])
funders_to_amount_funded : public(HashMap[address, uint256])

@deploy
def __init__(price_feed_address: address):
    # Since immutables are constants, we don't refer it with self.owner
    PRICE_FEED = AggregatorV3Interface(price_feed_address)
    OWNER = msg.sender

@external
@payable
def fund():
    '''
    Allows users to send money $ to this contract
    #Minimum $ amount send

    1. How to send ETH to this contract
    '''
    # s_wei_value is an inbuilt function
    usd_value_of_eth: uint256 = get_price_module._get_eth_to_usd_rate(PRICE_FEED, msg.value)
    # Revert undoes all the actions that has been done and sends back the remaining gas fees.
    assert usd_value_of_eth >= MINIMUM_USD, "You must spend more ETH!"
    self.funders.append(msg.sender)
    self.funders_to_amount_funded[msg.sender] += msg.value #Since the price of ETH changes, need to save the WEI value


@external
def withdraw():
    assert msg.sender == OWNER, "Not the contract owner!"
    send(OWNER, self.balance)
    for funder: address in self.funders:
        self.funders_to_amount_funded[funder]= 0
    self.funders = []


@external 
@view
def get_eth_to_usd_rate(eth_amount: uint256) -> uint256:
    return get_price_module._get_eth_to_usd_rate(PRICE_FEED, eth_amount)

@external
@view
def get_contract_balance() -> uint256:
    assert msg.sender == OWNER, "Only Owner can view the balance"
    return self.balance
