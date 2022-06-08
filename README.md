# Market Overreaction Study
A python based replication study of the market overreaction hypothesis by Clare and Thomas (1995) on selected S&amp;P 500 stocks
# Introduction
The objective of this exercise is to emulate “*The overreaction hypothesis and the UK Stock market*” study done by Andrew Clare and Stephen Thomas. In the paper, the authors evaluate whether loser stocks tend to outperform the winner stocks over a period of two to four years. At the end of the time period the loser stocks become winners and the former winners become losers. The overreaction hypothesis has been analyzed by numerous scholars over the years who have been able to explain how some of the overreaction may be explained by phenomenon like the January effect and the size effect. This study will focus on 12 months and 24 months time periods for each block of time. 

# Data and methodology
**Reviews of the additional articles**

Before the data collection, the two further articles have been reviewed to better understand the overreaction hypothesis and its practical uses.

A study by De Bondt (R. & De Bondt, 1985) cocludes that market overreaction could be explained by an adopted strategy of past losers’ purchases and past winners’ selling, since the market would soon move into the next reaction period when top performance stocks would be beaten by bottom performance stocks. However, there is one more abnormal time point which should be noted. The single significant outperform month for long-term losers is January. 

Another article by Mr. Hegadesseh and Mr. Titman theorizes more practical implementations as trading strategies. In this study, the monthly historical data was grouped into 4 groups as 1st, 2nd, 3rd and 4th quarters’ stock groups. In addition to that, they rebalance the 4 groups within each quarter which results in total 16 different strategies. It is important to recognize the fact that this paper studied the groups with independent time periods as compared to the first paper which divided the data into non-overlapping time blocks.

**Data collection procedure**

In this paper, we start with S&P 500 stock list and filter out the stocks that have been listed only recently or have delisted before the end of 2021. This leaves us with about 184 stocks that loosely fit our criterion. We further filter out the stocks which have missing data and nuisance values and choose the best fitting 100 stocks. We carry out this study in two parts:  

**1]** by dividing the time period into portfolios on the basis of 12 month observation and tracking period(n=12)

**2]** by dividing the time period into portfolios on the basis of 24 month observation and tracking period(n=24)

Comparing to N. & S.’s paper in this essay the test chose to use the observation and tracking method as De Bondt and Thaler’s one using separate time periods for observation and tracking to avoid the overlapping biases.


The stock market return is represented by NYSE index return and the risk-free rate is represented by the United States 3-month Treasury Bill rate of return.

The Yahoo API in python was used to request each individual S&P 500 stocks’ month start adjusted close price. This data was manually filtered on basis of the aforementioned criterion. The results show the earliest listed stock in S&P 500 is HSY which went public in 1957. 

**Asset/stock allocation and grouping**

The first 12 (or 24) month period of each time block is the observation period in which stocks are divided in to buckets and the winner and loser portfolios are identified. The next 12 (or 24) month period is the tracking period in which we determine whether the losers do in fact outperform the winners or not. 

**Statistical significance tests**

Aiming to get the research’s results showing the statistical significance there would be two tests being required. The first one would be a regression test of a constant value (‘1’ in this case of regression) against the difference between the returns of ‘losers’ and the returns of ‘winners. through the results of the first test the interpretation could be the outperformance test between the and losers and winners. Aiming to determine a constant value for X-value. The model looks like this:

**`Return ‘losers’ – Return ‘winners’  = 1 + η`**

In addition, the market return and risk free return should also be considered. The second test take the other factors into account. The X-value of the second regression would be the market risk premium. This model looks like this:

**`Return ‘losers’ – Return ‘winners’* = *β2 \* (Market return – Risk free) + α2 + η`**

The main findings of the python program are summarized in a table and exported into a csv file named “result.csv

The complete dataframe of all the 100 analyzed stocks’ returns have been saved into a csv file named “rd\_100\_2.csv”.
#
# Results and limitation 

The main findings of the python program are summarized in a table and exported into a csv file named “result.csv”. The results for the 24 month are explained as below:



In *Figure1,* We plot the *Return ‘losers’ – Return ‘winners’ against dates* 

In *Figure2,* We plot the *Return ‘losers’ – Return ‘winners’ against Market return – Risk free. It also shows the fitted lines calculated from the alpha and beta values from the OLS model regression.*

![image](https://user-images.githubusercontent.com/40740483/172577680-a5de7773-2a30-47c5-a72c-257a5e8ddcd3.png)

<p align="center"> Figure 1 Market Overreaction - Time Series Movement </p>

While momentum strategies can deliver market excess returns, it comes with taking risks, which can sometimes be huge. This is known as a “Momentum Crash”(Moskowitz, Asness, & Pedersen, 2013). As shown in the chart above, the Momentum factor yields the lowest returns when the market bottoms out. 

For example, if the year period comes to the 7th one marked with the pink color, one might find the huge decline of the difference of the returns between losers’ and winners’ portfolios. It suggests that the investors may take a huge risk to using the constrain strategy created by Mr. Hegadesseh and Mr. Titman (N. & S., 2022).


All in all, the momentum factor and the value factor are common phenomena in various capital markets, and the timing of outperforming the market varies. Some of our common perceptions about the momentum factor are wrong. Taking advantage of the negative correlation between the two in a portfolio result in a higher risk-adjusted return and Sharpe ratio.

![image](https://user-images.githubusercontent.com/40740483/172578090-738694d6-16bd-4467-b05c-ade9fe490a7e.png)

<p align="center"> Figure 2 Market Overreaction - Regressions over time periods </p>

The existence of momentum is a huge challenge to the Efficient Market Hypothesis for a investor in practice. Although the proponents of the efficient market hypothesis believe that these anomalies can be explained by market risk premiums, the capital market is ultimately a “human” market, and human nature is fully exposed in market transactions, so investors’ behavioral deviations (behavior bias) is a more acceptable explanation.

To examine the true effects from the market. Two tests of regressions have been done and the results of the periods do show the trends of exchange between the losers and winners:

During the whole period there are 3 subperiods shew a positive significant correlation between the difference of the returns against the market risk premium and 2 subperiods shew a negative significant correlation in between. Thus, the results match the overreaction-consulted exchange with the previous movement graphic.

![image](https://user-images.githubusercontent.com/40740483/172581936-4c1ab171-ccf6-4bfc-b761-ffc29f1f735b.png)

<p align="center"> Table 1 Market Overreaction - Results Summary </p>


![image](https://user-images.githubusercontent.com/40740483/172582114-7b407af7-aaa3-4cc1-9766-233d41cd9175.png)
<p align="center"> Table 2 Market Overreaction - Results P-values </p>

As the result shew, almost all the coefficients in the test 1 were statistically significant. Though they shew a slight negative correlation between difference of portfolios’ returns against the constant X-variable (in the python program was equal to “1”), it is insufficient enough, since the market risk premium had not been considered. Thus, the second test has been made.

During the second test, 5 out of 9 betas were statistically significant, while only one alpha reminded statistically significant.

Though the statistical significancy will be debated, the results from the two presented tables have shown the movements due to the market overreaction.



# Conclusion

In this paper a self-defined algorithm is applied by setting up the tracking period within this loop and sort all stocks into 5 portfolios ranked based on percentage changes of monthly returns. The output shows a regular change within bottom and top 20% stocks in a time room from 12 to 24 months.

For future work a wider range of asset allocation, e.g., more asset classes like currency market, bond market and other alternative investments should be considered. For the investigation of the defined observation and tracking loop-function the more factors could be added, since now it’s only one factor model by taking the market risk premium as its X-variable.

**Overall, The portfolio modelling backed by python does show the market overreaction movements.**

