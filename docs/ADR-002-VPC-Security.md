Lab 2 Notes: VPC Routing, DNS, and Security Audit

Date: November 2026
Topic: AWS SAA-C03 Study Notes & Lab 2 Documentation

1. What I Built and Audited in Lab 2:
- Created a bash script (network_audit.sh) to audit VPC networking components on my Amazon Linux 2023 EC2 instance.
- Verified the default route and gateway in the VPC.
- Tested Amazon-provided DNS resolution using nslookup.
- Checked active listening ports (Port 22 for SSH, Port 80 for HTTP).
- Audited the Apache web server access logs to confirm inbound traffic allowed by Security Groups.

2. SAA-C03 Exam Notes - VPC Routing & DNS:
- Route Table: To allow internet access, a Public Subnet must have a route pointing 0.0.0.0/0 to an Internet Gateway (IGW).
- VPC DNS: AWS reserves the "VPC network base IP + 2" for the Route 53 Resolver (Amazon-provided DNS). In my lab, the VPC network is 172.31.0.0, so the DNS server is 172.31.0.2.

3. SAA-C03 Exam Notes - Security Groups vs Network ACLs (NACLs):
- Security Groups (SGs) are Stateful: If you allow inbound Port 80, the return traffic is automatically allowed. They operate at the Instance level.
- Network ACLs (NACLs) are Stateless: You must explicitly allow both inbound and outbound traffic. They operate at the Subnet level.
- In this lab, my Apache logs showed successful inbound requests because the SG allowed inbound HTTP (Port 80) from 0.0.0.0/0.
