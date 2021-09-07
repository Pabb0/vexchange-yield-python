import requests
from thor_requests.connect import Connect
from thor_requests.contract import Contract
from thor_requests.utils import calc_blockRef, inject_decoded_return, inject_decoded_event


def wei_to_eth(x: float or int):
    return x / (10 ** 18)


def get_lp_amount(token_address):
    """
    Given the token_address, returns the amount of LP tokens at that token address,
    the token amount and the amount of VET.
    """
    connector: Connect = Connect("http://mainnet.veblocks.net")

    total_supply: dict = interact_with_contract(connector, token_address, 'totalSupply')
    lp_amount: float = wei_to_eth(total_supply['decoded']['0'])

    reserves: dict = interact_with_contract(connector, token_address, 'getReserves')
    token_amount: float = wei_to_eth(reserves['decoded']['0'])
    vet_amount: float = wei_to_eth(reserves['decoded']['1'])

    return lp_amount, token_amount, vet_amount


def interact_with_contract(connector: Connect, token_address: str, func_name: str):
    """
    Given a connector (to connect to the API), a token address and a function name,
    returns the decoded response of that function for that contract address.
    """
    contract_address: str = token_address
    # File gets opened relative to the filepath of the script that is executing.
    # main.py will get executed, so we write the path relative to main.py
    contract: Contract = Contract.fromFile("./contracts/IVexchangeV2Pair.json")

    # Make out clause to put it on JSON POST request
    clause: dict = connector.clause(contract=contract,
                                    func_name=func_name,
                                    func_params=[],
                                    to=contract_address)

    # Add necessary data to our JSON.
    json_data: dict = {
        'clauses': [clause],
        'blockRef': calc_blockRef(connector.get_block("best")["id"]),
        'expiration': 32,
    }

    # Make and get our POST request
    r = requests.post('https://mainnet.veblocks.net/accounts/*',
                      headers={"accept": "application/json", "Content-Type": "application/json"},
                      json=json_data
                      )
    if r.status_code == 200:
        # We only need the first clause of the response.
        first_clause = r.json()[0]  # first_clause contains the data we need
        # Decode the clause
        first_clause = inject_decoded_return(first_clause, contract, func_name)

        # If there is an event in our clause, decode it as well.
        if len(first_clause["events"]):
            first_clause["events"] = [
                inject_decoded_event(each_event, contract, contract_address)
                for each_event in first_clause["events"]
            ]

        return first_clause
