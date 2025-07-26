from eth_utils import to_wei
import boa

SEND_VALUE = to_wei(1, "ether")
RANDOM_USER = boa.env.generate_address("non-owner")
RANDOM_USERS = [boa.env.generate_address("non-owner") for add in range(11)]
total_amount_funded = 0

# method name must start with test
def test_price_feed_is_correct(coffee_contract, eth_usd_price_feed):
    print("Hi")
    print(coffee_contract)
    assert coffee_contract.PRICE_FEED() == eth_usd_price_feed.address


def test_starting_values(coffee_contract):
    assert coffee_contract.MINIMUM_USD() == to_wei(5, "ether")

def test_owner_is_sender(coffee_contract, account):
    assert coffee_contract.OWNER() == account.address

def test_fund_fails_without_enough_eth(coffee_contract):
    with boa.reverts("You must spend more ETH!"):
        coffee_contract.fund()

def test_fund_with_money(coffee_funded, account):
    # # Arrange
    # boa.env.set_balance(account.address, SEND_VALUE)
    # # Act
    # coffee_contract.fund(value = SEND_VALUE)

    # Assert
    funder = coffee_funded.funders(0)
    assert funder == account.address
    assert coffee_funded.funders_to_amount_funded(funder) == SEND_VALUE

def test_non_owner_cannot_withdraw(coffee_funded,account):
    # Arrange
    # boa.env.set_balance(account.address, SEND_VALUE)
    # # boa.env.set_balance(RANDOM_USER, SEND_VALUE)
    # # Act
    # coffee_contract.fund(value = SEND_VALUE)
    # Try to withdraw fund as a random user
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Not the contract owner!"):
            coffee_funded.withdraw()

def test_owner_can_withdraw(coffee_funded, account):
    # boa.env.set_balance(account.address, SEND_VALUE)
    # coffee_contract.fund(value = SEND_VALUE)
    coffee_funded.withdraw()
    assert coffee_funded.OWNER() == account.address

def test_owner_can_withdraw_prank_user(coffee_funded):
    # boa.env.set_balance(coffee_contract.OWNER(), SEND_VALUE)
    with boa.env.prank(coffee_funded.OWNER()):
        # coffee_contract.fund(value = SEND_VALUE)
        coffee_funded.withdraw()

    
def test_fund_from_multiple_users(coffee_contract):
    for user in range (len(RANDOM_USERS)):
        # Arrange
        boa.env.set_balance(RANDOM_USERS[user], SEND_VALUE)
        # Act
        with boa.env.prank(RANDOM_USERS[user]):
            coffee_contract.fund(value = SEND_VALUE)
            # Assert
            funder = coffee_contract.funders(user)
            assert funder == RANDOM_USERS[user]
            assert coffee_contract.funders_to_amount_funded(funder) == SEND_VALUE


def test_withdraw_all_funds_by_owner(coffee_contract):
    initial_owner_balance = boa.env.get_balance(coffee_contract.OWNER())
    for user in range (len(RANDOM_USERS)-1):
        # Arrange
        boa.env.set_balance(RANDOM_USERS[user], SEND_VALUE)
        # Act
        with boa.env.prank(RANDOM_USERS[user]):
            coffee_contract.fund(value = SEND_VALUE)
            # Assert
            funder = coffee_contract.funders(user)
            assert funder == RANDOM_USERS[user]
            assert coffee_contract.funders_to_amount_funded(funder) == SEND_VALUE
    
    # total_amount_funded = boa.env.get_balance(coffee_contract.address)
    
    total_amount_funded= coffee_contract.get_contract_balance()
    with boa.env.prank(coffee_contract.OWNER()):
        coffee_contract.withdraw()
        assert boa.env.get_balance(coffee_contract.address) == 0
        assert total_amount_funded == boa.env.get_balance(coffee_contract.OWNER()) - initial_owner_balance

def test_contract_balance_non_owner(coffee_contract):
    with boa.env.prank(RANDOM_USER):
        with boa.reverts("Only Owner can view the balance"):
            coffee_contract.get_contract_balance()
    
def test_eth_to_usd(coffee_contract):
    assert coffee_contract.get_eth_to_usd_rate(SEND_VALUE) > 0