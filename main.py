from calculations.get_data import get_data
import plotly.graph_objects as go
import json
import cryptocompare


def main():
    vet_price = cryptocompare.get_price('VET', currency='USD')['VET']['USD']
    vtho_price = cryptocompare.get_price('VTHO', currency='USD')['VTHO']['USD']

    with open('data/token_addresses.json', 'r') as f:
        token_data = json.load(f)

    data = []
    for i in token_data:
        to_be_added_list = get_data(i, token_data[i], vet_price, vtho_price)
        data.append(to_be_added_list)
    plot_data(data)


def plot_data(data) -> None:
    fig = go.Figure()
    for i in range(len(data)):
        df, name = data[i]
        fig.add_trace(go.Scatter(x=df.index, y=df['APY'],
                                 mode='lines',
                                 text=df['APY'],
                                 name=name))

    fig.write_html('APY.html')
    fig.show()


if __name__ == "__main__":
    main()
