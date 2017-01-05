# proof-solver

Graph search to generate symbolic mathematical proofs

```
Proof Generator initialized...
Given:  z/(sin(x)*cos(x)) + sin(x)/cos(x) + cos(x)/sin(x)  =  y/(sin(x)*cos(x))
Prove:  y - z  =  1
Nodes expanded: 16 ==> 1 = y - z	[Est. Dist. 0.0]
******************************************************
PROOF: 
	 z/(sin(x)*cos(x)) + sin(x)/cos(x) + cos(x)/sin(x)  =  y/(sin(x)*cos(x))
	 (z/(sin(x)*cos(x)) + sin(x)/cos(x) + cos(x)/sin(x))/y  =  1/(sin(x)*cos(x))
	 (z/(sin(x)*cos(x)) + sin(x)/cos(x) + cos(x)/sin(x))*sin(x)/y  =  1/cos(x)
	 (z + 1)/(y*cos(x))  =  1/cos(x)
	 (z + 1)/y  =  1
	 z + 1  =  y
	 1  =  y - z
******************************************************
```
