from dune_client.types import QueryParameter
from dune_client.client import DuneClient
from dune_client.query import QueryBase
# import other needed packages
import pandas as pd


dune = DuneClient(
    api_key="I7PEvvXEBi3IQvCWiklnIsoUO42nZGu7",
    base_url="https://api.dune.com",
    request_timeout=300
)

#Too slow to run
# query = QueryBase(
#     query_id=3958754,
# )
# query_result = dune.run_query_dataframe(
#   query=query
#   , ping_frequency = 10 # uncomment to change the seconds between checking execution status, default is 
# ) 

# START OF FINTECH AUM PROCESSING

fintech_aum_query_result = dune.get_latest_result_dataframe(3958754)
fintech_aum_query_result = fintech_aum_query_result.round()

# Calculate the weekly change
fintech_aum_query_result['weekly_change'] = fintech_aum_query_result['current_balance'] - fintech_aum_query_result['balance_one_week_ago']

# Sum up the current balances for Ugly Cash and Sentz
ugly_cash_total = fintech_aum_query_result.loc[fintech_aum_query_result['wallet_group'] == 'Ugly Cash', 'current_balance'].sum()
sentz_total = fintech_aum_query_result.loc[fintech_aum_query_result['wallet_group'] == 'Sentz', 'current_balance'].sum()
#Ugly Cash weekly changes
ugly_cash_weekly_change_total = fintech_aum_query_result.loc[fintech_aum_query_result['wallet_group'] == 'Ugly Cash', 'weekly_change'].sum()
sentz_weekly_change_total = fintech_aum_query_result.loc[fintech_aum_query_result['wallet_group'] == 'Sentz', 'weekly_change'].sum()

# END OF FINTECH AUM PROCESSING

