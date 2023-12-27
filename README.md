# xrpl-tps-test
Simple test for transactions per second on XRPL

Code outline
------------
. From the wallet with 511XRP balance create 250 tickets
. Get the resulting ticket numbers
. Create and sign payment transactions for 1 drop (0.000001 XRP) from Source to Dest using these tickets
. Submit the transactions all at once
