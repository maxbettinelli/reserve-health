import pandas as pd

# Function to process the data and return a DataFrame
def process_liquidation_data(response):
    # Create a dictionary for the renaming
    rename_dict = {
        '0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15': 'ETH+/eUSD',
        '0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f': 'WBTC/eUSD',
        '0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23': 'wstETH/eUSD',
        '0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011': 'ETH+/WETH',
        '0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf': 'bsdETH/eUSD (Base)',
        '0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31': 'hyUSD/eUSD (Base)',
        '0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d': 'cbETH/eUSD (Base)',
        '0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea': 'wstETH/eUSD (Base)'
    }

    # Transform the response into a pandas DataFrame
    items = response['transactions']['items']
    df = pd.json_normalize(items)

    # Sort the DataFrame by blockNumber in descending order
    df = df.sort_values(by='blockNumber', ascending=True)

    # Create a new column 'total_liquidations'
    df['total_liquidations'] = df.groupby('data.market.uniqueKey')['data.seizedAssetsUsd'].cumsum()

    # Apply the renaming to the 'data.market.uniqueKey' column
    df['data.market.uniqueKey'] = df['data.market.uniqueKey'].map(rename_dict).fillna(df['data.market.uniqueKey'])

    # Select relevant columns and rename them
    df_selected = df[['blockNumber', 'type', 'user.address', 'data.market.uniqueKey', 'data.seizedAssetsUsd', 'hash', 'total_liquidations']]
    df_selected.columns = ['blockNumber', 'type', 'user', 'market', 'seizedAssetsUsd', 'hash', 'liquidations_total']

    return df_selected

# Function to get the ending totals by market
def get_ending_totals(df_selected):
    ending_totals_df = df_selected.groupby('market').agg({
        'liquidations_total': 'last'
    }).reset_index()

    # Sort the DataFrame by 'liquidations_total' in descending order
    ending_totals_df = ending_totals_df.sort_values(by='liquidations_total', ascending=False)

    return ending_totals_df

def process_market_data(response):
    target_unique_keys = {
        "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15",
        "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f",
        "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23",
        "0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011",
        "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf",
        "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31",
        "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d",
        "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea"
    }

    market_chain_mapping = {
        "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15": "Mainnet",
        "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f": "Mainnet",
        "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23": "Mainnet",
        "0x9ec52d7195bafeba7137fa4d707a0f674a04a6d658c9066bcdbebc6d81eb0011": "Mainnet",
        "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf": "Base",
        "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31": "Base",
        "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d": "Base",
        "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea": "Base"
    }

    extracted_data_list = []
    for data in response['markets']['items']:
        if data["uniqueKey"] in target_unique_keys:
            market_name = f"{data['collateralAsset']['symbol']}/{data['loanAsset']['symbol']}"
            chain = market_chain_mapping[data["uniqueKey"]]

            extracted_data = {
                "marketName": market_name,
                "lltv": float(data["lltv"])/ 10 ** 18,
                "utilization": round(data["state"]["utilization"], 4),
                "supplyAssetsUsd": round(data["state"]["supplyAssetsUsd"]),
                "borrowAssetsUsd": round(data["state"]["borrowAssetsUsd"]),
                "Idle Funds": round(data["state"]["supplyAssetsUsd"] - data["state"]["borrowAssetsUsd"]),
                "supplyApy": data["state"]["supplyApy"],
                "borrowApy": data["state"]["borrowApy"],
                "chain": chain
            }
            extracted_data_list.append(extracted_data)

    df = pd.DataFrame(extracted_data_list)
    df.sort_values(by='chain', ascending=False, inplace=True)
    
    return df