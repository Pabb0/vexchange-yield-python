from get_lp_amount import get_lp_amount
import pandas as pd
from datetime import date


def get_data(name, info, price_of_vet, price_of_vtho):
    token_address = info['address']
    total_liquidity, total_other_amount, total_vet_amount = get_lp_amount(token_address)

    my_liquidity = info['amount']
    pool_percentage = my_liquidity / total_liquidity

    amount_of_vet = total_vet_amount * pool_percentage
    amount_of_other = total_other_amount * pool_percentage

    start_date = date(info['year'], info['month'], info['day'])
    date_now = date.today()
    days_since = (date_now - start_date).days

    vtho_per_vet_per_day = 0.000432
    price_of_other = price_of_vet * total_vet_amount / total_other_amount

    df = pd.read_csv(f'./data/{name}.csv', index_col='Days passed')

    initial_amount_of_vet = df.iloc[0]['VET']
    initial_amount_of_other = df.iloc[0][name]

    vtho_generation = initial_amount_of_vet * vtho_per_vet_per_day * days_since

    earnings_initial_amount = (initial_amount_of_vet * price_of_vet) + (vtho_generation * price_of_vtho) + (
                initial_amount_of_other * price_of_other)
    earnings_now = amount_of_vet * price_of_vet + amount_of_other * price_of_other

    APY = (((earnings_now / earnings_initial_amount) - 1) * (365 / days_since))

    df.loc[days_since] = [amount_of_vet, amount_of_other, APY]

    df.to_csv(f'./data/{name}.csv')
    return (df, name)
