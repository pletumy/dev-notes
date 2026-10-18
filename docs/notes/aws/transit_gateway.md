# aws transait gateway

## Context
- mutlti account + multi VPC, trafic gonna go through internet, the concern of latency and cost varies 

-> Solution: 
1) VPC Peering (nối 2 VPC khác region, khác account)
- pros: free
- cons: 
    + 2 VPC is enough, but in case too many vpc (just 5 vpc for eg we gonna need 10 vpc peering), 20 vpc -> 19 VPC peering =) 
    + cannot reach to on premise

2) Transit Gateway
- No overlap CIDR, like vpc peering
- reghional scope: 
- pros: 
    + could reach to On Premises
    + has up to 5000 attachment
- cons: 
    + best approach in case too many vpc, large scale network system 
    + 

