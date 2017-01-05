# proof-solver

Graph search to generate symbolic mathematical proofs

```
Proof Generator initialized...
Given:  sin(x)/cos(x) + cos(x)/sin(x)  =  y/(sin(x)*cos(x))
Prove:  y  =  1
Nodes expanded: 21 ==> 1 = y
******************************************************
PROOF: 
	 sin(x)/cos(x) + cos(x)/sin(x)  =  y/(sin(x)*cos(x))
	 2/sin(2*x)  =  2*y/sin(2*x)
	 2*sin(x)/sin(2*x)  =  2*y*sin(x)/sin(2*x)
	 1/cos(x)  =  y/cos(x)
	 1  =  y
******************************************************
```
