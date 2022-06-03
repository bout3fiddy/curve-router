# Curve Router

A work in progress dex router for curve.exchange. The current implementation is a simple depth-first search.


### TODO:

1. re-do `Swap` object so it has all info for `Swaps.vy`.
2. Prefer eth swaps instead of weth.
3. write tests for all chains. include as many corner cases.
4. gas estimates for each swap (some sort of probability distribution or some sort of fit with swap amounts and pool states as inputs should do the trick).
5. api-zation of the router suite: make it so that it can be queried by anyone using an endpoint that accepts pairs, amounts, network name.
