from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Function to execute the GraphQL query and return the data
def fetch_liquidation_data():
    # Define the GraphQL query
    query = gql("""
    query {
      transactions(
        where: {
          marketUniqueKey_in: [
            "0x3f4d007982a480dd99052c05d811cf6838ce61b2a2be8dc52fca107f783d1f15"
            "0x461da96754b33fec844fc5e5718bf24298a2c832d8216c5ffd17a5230548f01f"
            "0x6029eea874791e01e2f3ce361f2e08839cd18b1e26eea6243fa3e43fe8f6fa23"
            "0xf9ed1dba3b6ba1ede10e2115a9554e9c52091c9f1b1af21f9e0fecc855ee74bf"
            "0x3a5bdf0be8d820c1303654b078b14f8fc6d715efaeca56cec150b934bdcbff31"
            "0xb5d424e4af49244b074790f1f2dc9c20df948ce291fc6bcc6b59149ecf91196d"
            "0xce89aeb081d719cd35cb1aafb31239c4dfd9c017b2fec26fc2e9a443461e9aea"
          ]
          type_in: [MarketLiquidation]
        }
      ) {
        items {
          blockNumber
          hash
          type
          user {
            address
          }
          data {
            ... on MarketLiquidationTransactionData {
              seizedAssets
              repaidAssets
              seizedAssetsUsd
              repaidAssetsUsd
              badDebtAssetsUsd
              liquidator
              market {
                uniqueKey
              }
            }
          }
        }
      }
    }
    """)

    # Set up the client
    transport = RequestsHTTPTransport(
        url="https://blue-api.morpho.org/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute the query
    response = client.execute(query)
    return response


def fetch_market_data():
    query = gql("""
    query {
      markets(first: 1000) {
        items {
          uniqueKey
          lltv
          oracleAddress
          irmAddress
          loanAsset {
            address
            symbol
            decimals
          }
          collateralAsset {
            address
            symbol
            decimals
          }
          state {
            borrowApy
            borrowAssets
            borrowAssetsUsd
            supplyApy
            supplyAssets
            supplyAssetsUsd
            fee
            utilization
          }
        }
      }
    }
    """)

    # Set up the client
    transport = RequestsHTTPTransport(
        url="https://blue-api.morpho.org/graphql",
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    # Execute the query
    response = client.execute(query)
    return response