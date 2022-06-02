import statsmodels.api as sm
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from pandas_datareader import data as web
import pandas as pd
import seaborn as sns
import scipy.stats as sp
import random

df_pct_changes = pd.DataFrame()
tbill_monthly_return = pd.DataFrame()

start_year = 1985
end_year = 2021

# Yahoo request
# for stock in stock_names:
#     raw_data = web.get_data_yahoo(stock, start='1999-12-29', end='2021-12-29', interval='m')['Adj Close']
#     data_xx = pd.DataFrame(raw_data)
#     xx_return = data_xx['Adj Close'].pct_change()
#     df_pct_changes.insert(0, stock, xx_return)
#
# # filtered_df = df_pct_changes.loc[(df_pct_changes['date'] >= '2002-01-01') & (df['date'] < '2002-12-31')]
#
# # print(df_pct_changes.head())
#
# # write df to csv
# df_pct_changes.to_csv('df_pct_changes.csv')

# read df from csv
df_pct_changes = pd.read_csv('rd_100_2.csv')
print(df_pct_changes)

stock_names = df_pct_changes.columns

# # FRED Request for TBILL data
# TBILL_3MS = web.get_data_fred('TB3MS',
#                             start='1984-12-01',
#                             end='2021-12-29',
#                             )
#
# # write TBILL df to csv
# TBILL_3MS.to_csv('TBILL_3MS.csv')


# read TBILL df from csv
TBILL_3MS = pd.read_csv('TBILL_3MS.csv')

data_xx = pd.DataFrame(TBILL_3MS)

tbill_monthly_return['Date'] = TBILL_3MS['DATE']
tbill_monthly_return['TB1YR'] = TBILL_3MS['TB3MS'] / 100 / 12

# _STEP_1
# Market and assets monthly return
market_monthly_return_df = df_pct_changes[['Date', '^NYA']]
assets_monthly_return_df = df_pct_changes.drop('^NYA', axis=1)

# replace NaN with 0
market_monthly_return_df = market_monthly_return_df.replace(np.NaN, 0)
assets_monthly_return_df = assets_monthly_return_df.replace(np.NaN, 0)

asset_names = assets_monthly_return_df.columns[1:]
market_index = market_monthly_return_df.columns[1]


# _STEP_2
# initialise dataframe to store yearly percent changes
df_yearly_stocks_return = pd.DataFrame()
df_yearly_stocks_return[stock_names] = np.NaN

# initialise temporary list to store yearly percent changes
this_year_changes = pd.DataFrame()
df_yearly_pct_changes = pd.DataFrame()

for year in range(start_year, end_year):
    for stock in stock_names:
        filtered_df = assets_monthly_return_df.loc[
            (assets_monthly_return_df['Date'] >= str(year) + '-01-01') & (
                    assets_monthly_return_df['Date'] < str(year) + '-12-31')]
        df_temp_02 = filtered_df.mean(axis=0, skipna=False)
        df_yearly_stocks_return[year] = df_temp_02

# _STEP_3
# tracking period in years
# 1 -> n=12
# 2 -> n=24
tracking_period = 1

# obtain the sample size
T = len(df_yearly_stocks_return.index)

# init portfolio dfs _od_
winner_parent_df = pd.DataFrame(columns=["Date", "winner_mean"])
winner_parent_df = winner_parent_df.set_index('Date')
loser_parent_df = pd.DataFrame(columns=["Date", "loser_mean"])
loser_parent_df = loser_parent_df.set_index('Date')
df_Rdt_loser_winner_diff_parent = pd.DataFrame(columns=["Date", "Rdt"])
df_Rdt_loser_winner_diff_parent = df_Rdt_loser_winner_diff_parent.set_index('Date')
df_Rdt_loser_winner_diff = pd.DataFrame()

quantile_percentage_length = 0.2
portfolio_period = 2 * tracking_period

parent_winner_returns = {}
parent_losers_returns = {}
parent_w_l_diff_return = {}

parent_test1_alphas_list = {}
parent_test1_betas_list = {}
parent_test1_alphas_p_value_list = {}
parent_test1_betas_p_value_list = {}

parent_test2_alphas_list = {}
parent_test2_betas_list = {}
parent_test2_alphas_p_value_list = {}
parent_test2_betas_p_value_list = {}

# MAKING WINNER AND LOSER PORTFOLIOS ON BASIS OF YEARLY  RETURNS
for c_year in range(start_year, end_year, (2 * tracking_period)):

    full_period_bucket_df = pd.DataFrame()
    observation_bucket_df = pd.DataFrame()
    tracking_bucket_df = pd.DataFrame()
    winner_portfolio_y_df = pd.DataFrame()
    loser_portfolio_y_df = pd.DataFrame()
    all_winner_buckets_returns = pd.DataFrame()
    all_loser_buckets_returns = pd.DataFrame()

    observation_start_year = c_year
    observation_end_year = c_year + tracking_period - 1
    tracking_start_year = c_year + tracking_period
    tracking_end_year = c_year + 2 * tracking_period

    ## filtering stocks down to this portfolio [eriod
    df_this_bucket_monthly_stock_return = df_pct_changes.set_index('Date')

    df_this_bucket_monthly_stock_return = df_this_bucket_monthly_stock_return.loc[
        (df_this_bucket_monthly_stock_return.index >= str(observation_start_year) + '-01-01') & (
                df_this_bucket_monthly_stock_return.index < str(tracking_end_year) + '-01-01')]

    ## filtering market data down to this portfolio period
    df_this_bucket_monthly_market_return = market_monthly_return_df.set_index('Date')
    df_this_bucket_monthly_market_return = df_this_bucket_monthly_market_return[
        df_this_bucket_monthly_market_return.columns[0]]
    df_this_bucket_monthly_market_return = df_this_bucket_monthly_market_return.loc[
        (df_this_bucket_monthly_market_return.index >= str(observation_start_year) + '-01-01') & (
                df_this_bucket_monthly_market_return.index < str(tracking_end_year) + '-01-01')]

    ## filtering tbill data down to this portfolio period
    df_this_bucket_monthly_tbill_return = tbill_monthly_return.set_index('Date')
    df_this_bucket_monthly_tbill_return = df_this_bucket_monthly_tbill_return[
        df_this_bucket_monthly_tbill_return.columns[0]]
    df_this_bucket_monthly_tbill_return = df_this_bucket_monthly_tbill_return.loc[
        (df_this_bucket_monthly_tbill_return.index >= str(observation_start_year) + '-01-01') & (
                df_this_bucket_monthly_tbill_return.index < str(tracking_end_year) + '-01-01')]

    obs_year_pos_in_df = df_yearly_stocks_return.columns.get_loc(observation_start_year)

    ## getting observation period bucket for all stocks
    for this_bucket_year in range(observation_start_year, tracking_start_year):
        observation_bucket_df.insert(0, this_bucket_year, df_yearly_stocks_return[this_bucket_year])

    observation_period_yearly_return_mean = observation_bucket_df.mean(axis=1)

    ## sorting observation period stocks
    sorted_stock_returns_observation_period = observation_period_yearly_return_mean.sort_values(ascending=False)

    winner_bucket_lower_limit = int(T * quantile_percentage_length)
    loser_bucket_upper_limit = int(T * (1 - quantile_percentage_length))

    winner_portfolio_y_df = sorted_stock_returns_observation_period.iloc[0:winner_bucket_lower_limit]
    loser_portfolio_y_df = sorted_stock_returns_observation_period.iloc[loser_bucket_upper_limit:]

    ## making winners and losers df
    this_portfolio_winner_stocks_list = winner_portfolio_y_df.index
    this_winner_portfolio_stocks_pct_changes_df = df_this_bucket_monthly_stock_return[this_portfolio_winner_stocks_list]
    this_winner_portfolio_mean_returns_df = this_winner_portfolio_stocks_pct_changes_df.mean(axis=1)


    this_portfolio_loser_stocks_list = loser_portfolio_y_df.index
    this_loser_portfolio_stocks_pct_changes_df = df_this_bucket_monthly_stock_return[this_portfolio_loser_stocks_list]
    this_loser_portfolio_mean_returns_df = this_loser_portfolio_stocks_pct_changes_df.mean(axis=1)

    # loser - winner
    this_portfolio_losers_minus_winners = this_loser_portfolio_mean_returns_df - this_winner_portfolio_mean_returns_df

    parent_winner_returns[observation_start_year] = this_winner_portfolio_mean_returns_df.mean()
    parent_losers_returns[observation_start_year] = this_loser_portfolio_mean_returns_df.mean()
    parent_w_l_diff_return[observation_start_year] = this_portfolio_losers_minus_winners.mean()

    ### plotting
    this_portfolio_losers_minus_winners_mean = this_portfolio_losers_minus_winners.mean()

    plt.figure(0)
    plt.plot(this_portfolio_losers_minus_winners.index, this_portfolio_losers_minus_winners, label=observation_start_year)

    #####    test 1
    this_portfolio_dates_constant = pd.Series(index=this_portfolio_losers_minus_winners.index)
    this_portfolio_dates_constant.loc[:] = 1
    model0 = sm.OLS(endog=this_portfolio_losers_minus_winners.astype(float),
                    exog=sm.add_constant(this_portfolio_dates_constant))

    results0 = model0.fit()

    # obtain alpha_hat and beta_hat:
    alpha_beta = results0.params
    this_alpha = alpha_beta[alpha_beta.index[0]]
    # this_beta = alpha_beta[alpha_beta.index[1]]
    parent_test1_alphas_list[observation_start_year] = this_alpha
    # parent_test1_betas_list[observation_start_year] = this_beta

    ## obtain alpha and beta p value
    alpha_beta_p_value = results0.pvalues
    this_alpha_p_value = alpha_beta_p_value[alpha_beta_p_value.index[0]]
    # this_beta_p_value = alpha_beta_p_value[alpha_beta_p_value.index[1]]
    parent_test1_alphas_p_value_list[observation_start_year] = this_alpha_p_value
    # parent_test1_betas_p_value_list[observation_start_year] = this_beta_p_value

    #####    test 2
    df_this_bucket_monthly_market_excess_return = df_this_bucket_monthly_market_return - df_this_bucket_monthly_tbill_return

    model = sm.OLS(endog=this_portfolio_losers_minus_winners.astype(float),
                   exog=sm.add_constant(df_this_bucket_monthly_market_excess_return))

    # execute OLS:
    results = model.fit()

    # obtain alpha_hat and beta_hat:
    alpha_beta = results.params
    this_alpha = alpha_beta[alpha_beta.index[0]]
    this_beta = alpha_beta[alpha_beta.index[1]]
    parent_test2_alphas_list[observation_start_year] = this_alpha
    parent_test2_betas_list[observation_start_year] = this_beta

    ## obtain alpha and beta p value
    alpha_beta_p_value = results.pvalues
    this_alpha_p_value = alpha_beta_p_value[alpha_beta_p_value.index[0]]
    this_beta_p_value = alpha_beta_p_value[alpha_beta_p_value.index[1]]
    parent_test2_alphas_p_value_list[observation_start_year] = this_alpha_p_value
    parent_test2_betas_p_value_list[observation_start_year] = this_beta_p_value

    # fitted_line = alpha_beta['const'] + alpha_beta['market'] * data_am.market
    alpha_beta.fillna(0)

    fitted_line = alpha_beta.iloc[0] + alpha_beta.iloc[1] * df_this_bucket_monthly_market_excess_return

    rgb = [random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)]

    plt.figure(1)
    plt.plot(this_portfolio_losers_minus_winners, df_this_bucket_monthly_market_excess_return, 'o', color=rgb,
             label=str(c_year) + ' points')

    rgb = [random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)]
    plt.plot(df_this_bucket_monthly_market_excess_return, fitted_line, linestyle=':', color=rgb,
             label=str(c_year) + ' fitted line')

plt.legend()
plt.show()


df_030 = pd.DataFrame(parent_winner_returns.values(), index=parent_winner_returns.keys())
df_031 = pd.DataFrame(parent_losers_returns.values(), index=parent_losers_returns.keys())
df_032 = pd.DataFrame(parent_w_l_diff_return.values(), index=parent_w_l_diff_return.keys())

df_033 = pd.DataFrame(parent_test1_alphas_list.values(), index=parent_test1_alphas_list.keys())
df_034 = pd.DataFrame(parent_test1_alphas_p_value_list.values(), index=parent_test1_alphas_p_value_list.keys())

df_035 = pd.DataFrame(parent_test2_alphas_list.values(), index=parent_test2_alphas_list.keys())
df_036 = pd.DataFrame(parent_test2_betas_list.values(), index=parent_test2_betas_list.keys())
df_037 = pd.DataFrame(parent_test2_alphas_p_value_list.values(), index=parent_test2_alphas_p_value_list.keys())
df_038 = pd.DataFrame(parent_test2_betas_p_value_list.values(), index=parent_test2_betas_p_value_list.keys())

df_output_final_csv = pd.DataFrame()

df_output_final_csv["Winners Returns"] = df_030[0]
df_output_final_csv["Losers Returns"] = df_031[0]
df_output_final_csv["Loser - Winners Returns"] = df_032[0]
df_output_final_csv["Test 1 Alpha Coefficient"] = df_033[0]
df_output_final_csv["Test 1 Alpha P-Value"] = df_034[0]
df_output_final_csv["Test 2 Alpha Coefficient"] = df_035[0]
df_output_final_csv["Test 2 Alpha P-Value"] = df_036[0]
df_output_final_csv["Test 2 Beta Coefficient"] = df_037[0]
df_output_final_csv["Test 2 Beta P-Value"] = df_038[0]

print(df_output_final_csv)
df_output_final_csv.to_csv('result.csv')



