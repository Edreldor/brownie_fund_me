from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_script import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3


def deploy_fund_me():
    account = get_account()

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise use mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active(
        )]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me_contract = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify")
    )
    print("FundMe Contract Deployed on {} at: {}".format(
        network.show_active(), fund_me_contract.address))
    return(fund_me_contract)


def main():
    deploy_fund_me()
