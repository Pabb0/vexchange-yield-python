import requests
from thor_requests.connect import Connect
from thor_requests.contract import Contract
from thor_requests.utils import calc_blockRef, inject_decoded_return, inject_decoded_event
import sys


def wei_to_eth(x):
    return x / (10 ** 18)


def get_lp_amount(token_address):
    connector = Connect("http://mainnet.veblocks.net")

    total_supply = interact_with_contract(connector, token_address, 'totalSupply')
    lp_amount = wei_to_eth(total_supply['decoded']['0'])

    reserves = interact_with_contract(connector, token_address, 'getReserves')
    token_amount = wei_to_eth(reserves['decoded']['0'])
    vet_amount = wei_to_eth(reserves['decoded']['1'])

    return lp_amount, token_amount, vet_amount


def interact_with_contract(connector, token_address, func_name):
    _contract_address = token_address
    # File gets opened relative to the filepath of the script that is executing.
    # main.py will get executed, so we write the path relative to main.py
    _contract = Contract.fromFile("./contracts/IVexchangeV2Pair.json")

    clause = connector.clause(contract=_contract,
                              func_name=func_name,
                              func_params=[],
                              to=_contract_address)
    json_data = {
        'clauses': [clause],
        'blockRef': calc_blockRef(connector.get_block("best")["id"]),
        'expiration': 32,
    }

    r = requests.post('https://mainnet.veblocks.net/accounts/*',
                      headers={"accept": "application/json", "Content-Type": "application/json"},
                      json=json_data
                      )

    # decode the "return data" from the function call
    first_clause = r.json()[0]
    first_clause = inject_decoded_return(first_clause, _contract, func_name)
    # decode the "event" from the function call
    if len(first_clause["events"]):
        first_clause["events"] = [
            inject_decoded_event(each_event, _contract, _contract_address)
            for each_event in first_clause["events"]
        ]

    return first_clause
