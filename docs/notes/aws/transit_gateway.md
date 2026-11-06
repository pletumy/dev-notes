# aws transit gateway

## Context
- mutlti account + multi VPC, trafic gonna go through internet, the concern of latency and cost varies 

-> Solution: 
1) VPC Peering (nối 2 VPC khác region, khác account)
- pros: không tính phí theo giờ (vẫn tính phí data transfer inter-region / inter-AZ)
- cons: 
    + 2 VPC is enough, but in case too many vpc (just 5 vpc for eg we gonna need 10 vpc peering), 20 vpc -> 190 VPC peering (full mesh: 20×19/2, mỗi VPC 19 kết nối) 
    + cannot reach to on premise

2) Transit Gateway
- No overlap CIDR, like vpc peering
- reghional scope: 
- pros: 
    + could reach to On Premises
    + has up to 5000 attachment
- cons: 
    + tốn phí: theo giờ cho mỗi attachment + phí xử lý data theo GB (peering thì không có)
- phù hợp nhất khi có nhiều VPC, hệ thống mạng quy mô lớn

