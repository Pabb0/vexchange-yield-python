from calculations.get_data import get_data

import json
import cryptocompare

import plotly.graph_objects as go

import multiprocessing
from itertools import repeat


def main() -> None:
    # Get the current market VET and VTHO prices
    prices: dict = cryptocompare.get_price(['VET', 'VTHO'], currency='USD')
    vet_price: float = prices['VET']['USD']
    vtho_price: float = prices['VTHO']['USD']

    # Get our initial information (token addresses and starting info)
    with open('data/token_addresses.json', 'r') as f:
        token_data: dict = dict(json.load(f))

    # Get the data by using multiple processes
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # zip([0,1], [a,b]) == [[0,a], [1,b]]
        # data is a list of tuples: (Pandas dataframe, string)
        data = pool.starmap(get_data,
                            zip(token_data.keys(), token_data.values(), repeat(vet_price), repeat(vtho_price)))

    # Plot the data
    plot_data(data)


def plot_data(data) -> None:
    """
    Plots the given list of DataFrames.
    """
    # Make a figure
    fig = go.Figure()
    fig.update_layout(
        title="Overview of the APY of different tokens",
        xaxis_title="Days since",
        yaxis_title="APY"
    )

    # Add every token to the figure
    for (df, name) in data:
        fig.add_trace(go.Scatter(x=df.index, y=df['APY'],
                                 mode='lines',
                                 name=name))

    # Save a HTML copy
    fig.write_html('APY.html', auto_open=True)


if __name__ == "__main__":
    main()
