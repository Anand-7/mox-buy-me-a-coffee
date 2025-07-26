# pragma version ^0.4.0
# @licence : MIT
from interfaces import AggregatorV3Interface


PRECISION: constant(uint256) = 1 * (10 ** 18)

@internal
@view
def _get_eth_to_usd_rate(price_feed: AggregatorV3Interface,eth_amount: uint256) -> uint256:
    '''
    Chris sent us a0.01 ETH for us to buy a coffee
    '''
    # Get the price in $ to the eth amount passed
    # staticcall is used to call an external contract from a contract
    # When calling an view function and don't want to change any state, use staticcall
    price: int256 = staticcall price_feed.latestAnswer() #270784000000
    # convert 270784000000 to ETh Amount in USD
    # ETH Amount has 8 decimal places and wei has 18 decimal places
    eth_price : int256 = price * (10 ** 10) #2707840000000000000000
    eth_amount_in_usd: uint256 = (eth_amount * convert(eth_price, uint256)) // (PRECISION)
    return eth_amount_in_usd # Returns value with 18 decimals