# Vexchange Yield Calculator - Python version

This project tracks the APY of the most popular tokens on Vexchange (in an LP with VET):
  - VeThor Token
  - OceanEx
  - Safe Haven
  - VIMworld
  - VPunks Token
  
## How to run for the first time
- Clone the repository
- Add your info to [initial JSON file](data/token_addresses.json)
  - For every token you can set the amount of LP tokens you have (check [Vexchange](https://www.vexchange.io) for this (or find it by interacting with the contract (similar to [this](calculations/get_lp_amount.py))) (or just leave it at 1000 if you just want to see the APY)
  - For every token you need to set the start date ( = current date).
  - Don't touch the address of the token (needed to interact with the contract)
- Install the required packages
- Run the [script](main.py)
After running the script, a HTML page will open showing the forecasted APY's.

## Add tokens
- You can add other tokens on Vexchange by adding them to the [initial JSON file](data/token_addresses.json).
- You would also need to initalise a new CSV file in the [data folder](data) called f'{token}.csv, with token being the name of the token. Enter the column names in this file and your initial amounts.

## Disclaimer
This project is not affiliated with the Vexchange team. It was purely built for fun.



