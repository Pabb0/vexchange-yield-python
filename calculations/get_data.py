from calculations.get_lp_amount import get_lp_amount
import pandas as pd
from datetime import date


def get_data(name: str, info: dict, price_of_vet: float, price_of_vtho: float):
    """
    Given its name, info and VET + VTHO prices, updates the dataframe of the token.
    A tuple containing the dataframe and the name of the token is returned.
    """
    # Get the token_address (contract address) of the token and the amount of initial LP tokens.
    token_address: str = info['address']
    my_liquidity: float = info['amount']

    # Get data on chain
    total_liquidity, total_other_amount, total_vet_amount = get_lp_amount(token_address)

    pool_percentage: float = my_liquidity / total_liquidity

    amount_of_vet: float = total_vet_amount * pool_percentage
    amount_of_other: float = total_other_amount * pool_percentage
    price_of_other: float = price_of_vet * total_vet_amount / total_other_amount

    start_date = date(info['year'], info['month'], info['day'])
    date_now = date.today()
    days_since: int = (date_now - start_date).days

    df = pd.read_csv(f'./data/{name}.csv', index_col='Days passed')

    initial_amount_of_vet: float = df.iloc[0]['VET']
    initial_amount_of_other: float = df.iloc[0][name]
    vtho_per_vet_per_day: float = 0.000432

    vtho_generation: float = initial_amount_of_vet * vtho_per_vet_per_day * days_since

    earnings_initial_amount: float = (initial_amount_of_vet * price_of_vet) + (vtho_generation * price_of_vtho) + (
                initial_amount_of_other * price_of_other)
    earnings_now: float = amount_of_vet * price_of_vet + amount_of_other * price_of_other

    if name == 'VTHO':
        print(f'Market rate VTHO/VET   : {price_of_vet / price_of_vtho}')
        print(f'Vexchange rate VTHO/VET: {amount_of_other / amount_of_vet}')
        print(f'Initial rate VTHO/VET  : {initial_amount_of_other / initial_amount_of_vet}')
        print(f'Using vexchange you earned ${earnings_now-earnings_initial_amount} extra in {days_since} days')

    apy: float = (((earnings_now / earnings_initial_amount) - 1) * (365 / days_since))

    df.loc[days_since] = [amount_of_vet, amount_of_other, apy]
    df.to_csv(f'./data/{name}.csv')

    return (df, name)
