# xrpl-tps-test
Simple test for transactions per second on XRPL

Code outline
------------
1. From the wallet with 511XRP balance create 250 tickets
2. Get the resulting ticket numbers
3. Create and sign payment transactions for 1 drop (0.000001 XRP) from Source to Dest using these tickets
4. Submit the transactions all at once
