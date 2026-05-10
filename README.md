# Arbitrage-Analysis-with-Bellman-Ford-Algorithm
Arbitrage refers to the practice of exploiting differences in the prices of an identical asset and earning a risk-free profit in the process. Traditional economic theory suggests that asset prices incorporate all relevant information at any point in time which would make it impossible for arbitrage opportunities to arise. Empirical work on foreign exchange markets, however, has found that arbitrage opportunities do in fact occur frequently, although the number of such opportunities has been declining over the years and their profitability and duration tends to be very low, especially after accounting for execution costs. This study focuses on triangular arbitrage and aims to expand the scope of the concept by allowing for more/less currencies to be incorporated when detecting for arbitrage opportunities, through the Bellman-Ford algorithm. The frequency, duration, profitability of arbitrage opportunities will be analysed.

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

