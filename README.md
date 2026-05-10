# Arbitrage-Analysis-with-Bellman-Ford-Algorithm
Arbitrage refers to the practice of exploiting differences in the prices of an identical asset and earning a risk-free profit in the process. Traditional economic theory suggests that asset prices incorporate all relevant information at any point in time which would make it impossible for arbitrage opportunities to arise. Empirical work on foreign exchange markets, however, has found that arbitrage opportunities do in fact occur frequently, although the number of such opportunities has been declining over the years and their profitability and duration tends to be very low, especially after accounting for execution costs. This study focuses on triangular arbitrage and aims to expand the scope of the concept by allowing for more/less currencies to be incorporated when detecting for arbitrage opportunities, through the Bellman-Ford algorithm. The frequency, duration, profitability of arbitrage opportunities in the foreign exchange market will be analysed.

## Methodology
The Bellman-Ford algorithm is a method for finding the shortest path from a single-source node to all other nodes in a weighted directed graph. Unlike other well-known shortest path algorithms like Dijkstra’s algorithm, bellman-ford has the unique ability to handle negative weight cycles. The algorithm works by assigning an initial distance from one node to all other nodes in a graph and then initiates an iterated relaxation process V – 1 times (where V represents the total number of vertices) thus reducing and updating the edge weights between nodes until no further improvements can be found. After the V -1 iterations are complete, it takes one final pass through the nodes to see it they can still be updated. 
As explained earlier, triangular arbitrage involves the simultaneous exchange of three currencies for the purpose of profiting from discrepancies in the rate product, such that it is greater than 1. This can be represented as:

rₐᵇ ·  rbc  ·  rca  >  1
The above equation gives the required condition for triangular arbitrage. Assuming three currencies a, b and c, triangular arbitrage exists when the product of the exchange rate of a in terms of b (rab ),  exchange rate of b  in terms of c (rbc) and exchange rate of c in terms of a (rca) is greater than 1. A successful execution of the strategy requires conversion from a to b, b to c and c back to a. To convert the above idea into graph problem to which bellman-ford can be applied and extend it to include n number of currencies, the currencies can be taken as nodes and exchange rates as weighted edges. Graph algorithms are better at handling additive rather than multiplicative relations, so the above equation is represented as the sum of the log of exchange rates as shown below – 

log (rₐᵇ) + log(rbc )+ log( rca)  >  0

To make use of the bellman ford algorithm’s ability to handle negative edge weights, this equation is then made negative as shown below – 

-log (rₐᵇ) - log(rbc  )- log( rca)  <  0

Thus, detection of a negative-weight cycle means detection of an arbitrage opportunity. The equation below generalizes this idea for any number of currencies.

W(C)  =  ∑ w(vᵢ, vᵢ₊₁)  =  − ∑ log( rᵢ,ᵢ₊₁ )  =  − log ∏ rᵢ,ᵢ₊₁

Here, W(C) represents the cycle sum. It is strictly negative only when there exists an opportunity for arbitrage. The Bellman-Ford algorithm, through its shortest-path computation detects for the presence of such opportunities. The Bellman-Ford algorithm used in this study only reports the most profitable loop detected out of all the possible loops for each time stamp of the collected data.

## Dataset and Description
This study uses 5 days of second-by-second data from 00:00 UTC to 23:59 UTC. The data has been obtained from the Dukascopy database .  The period under consideration is 30th March to 3rd April 2026. The pairwise exchange rates for the following 5 currencies are used – US dollar (USD), Euro (EUR), Chinese yuan (CNH), British pound (GBP) and Swiss franc (CHF). These currencies, except for the CHF, have been chosen as they are the most traded currencies in the world. The Japanese yen (JPY) has a higher trade volume than CHF but is not chosen for this study as it is traded in units up to the third decimal place while other currencies are traded in units up to the fifth decimal place. The JPY is thus excluded to avoid any complications in arbitrage calculation that may arise due to the differences in decimal points. Forward filling has been used to fill in missing values.
Closing bid prices have been used to denote the exchange rate from the base currency to the quote currency and the reciprocal of closing ask prices have been taken to denote the exchange rate in the other direction, from the quote currency to the base currency. In graphical form, the bid price would represent the edge from the base currency to the quote currency and the reciprocal of ask price would represent the edge from the quote to the base currency. Thus, if the following transaction is to be carried out– EUR to USD, USD to CNH, CNH to EUR it would use the following pairs – EUR/USD, USD/CNH, EUR/CNH and its rate product would be:

(EUR/USDBID) * (USD/CNHBID) * 1/(EUR/CNHASK) = r

An arbitrage opportunity would exist for values of r > 1. For this study, values of r > 1 up to the 5th decimal point, ie 1.00001 or higher have been considered valid to be recorded as an arbitrage opportunity if detected, as currency trading typically happens in values extending till the 5th decimal point. It should be noted however that this does account for transaction and other execution-related costs that may be incurred when attempting to seize these opportunities.

## Findings
- Over the 5 day sample more than 13,000 opportunities were detected. The average profitability, however was very low at only 0.0016% and over 62% of the identified opportunities vanished within less than a second

-Currencies like the USD and CNH were the most important for enabling arbitrage opportunities. Over 98% of the identified opportunities involved a CNH to USD conversion. Currencies having USD CNH conversions also showed the strongest cross-correlations. On the other hand, the GBF and CHF played very minor roles in enabling arbitrage, rarely featuring in an opportunity.

-The largest number of opportunities was observed between hours 6:00 UTC and 16:00 UTC which coincides with the London sessions which is the most active market period in Europe. This suggests the importance of liquidty for creating arbitrage opportunities. 
