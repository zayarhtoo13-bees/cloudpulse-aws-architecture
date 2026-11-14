# cloudpulse-aws-architecture
My AWS SAA-C03 Cloud Architecture Portfolio, Official AWS Workshops, and Troubleshooting Labs.
CloudPulse & AWS Hands-On Portfolio (SAA-C03 Track)

Author: Zayar Htoo
Background: First-Year Computer Science Student in Myanmar
Certifications: AWS Certified AI Practitioner (Earned) | AWS Certified Solutions Architect - Associate (In Progress)
Cost Strategy: $0.00 Budget (AWS Free Tier + Tear-Down Discipline)


1. ABOUT THIS REPOSITORY
--------------------------------------------------
I am a first-year Computer Science student preparing for a Cloud / DevOps Engineering internship. Since I do not have prior industry work experience, I created this repository to document my real hands-on practice in the AWS Console and Linux terminal.

This repository contains two main parts:
- Part A (CloudPulse 9-Lab Project): A progressive architecture project starting from a single EC2 instance and evolving into a serverless event-driven pipeline.
- Part B (AWS Skill Builder & Official Workshops): Completed hands-on tasks, badges, and troubleshooting notes from workshops.aws and AWS Skill Builder.


2. HOW I USE AI AS A LEARNING TOOL (TRANSPARENCY NOTE)
--------------------------------------------------
My core focus is mastering AWS Cloud Architecture, VPC Networking, IAM Security, and Linux troubleshooting. 
To move faster on front-end HTML design and Python helper scripts, I use Google Gemini AI as a coding assistant—similar to how engineers use GitHub Copilot in the workplace. 

My personal rule for every lab:
- I never copy-paste blindly. I ask the AI to break down every Linux command, JSON policy, and Python function so I can write notes in my notebook and explain them in interviews.
- I configure all AWS resources, security groups, and services myself in the AWS Console and troubleshoot terminal errors hands-on.

--------------------------------------------------
3. PART A: CLOUDPULSE 9-LAB ARCHITECTURE ROADMAP

- Lab 01: EC2 Web Server (AL2023), Apache, systemd, and IMDSv2 Python Telemetry (Status: Completed)
- Lab 02: VPC Subnets, Security Groups vs Network ACLs, and Linux Network Audit (Status: In Progress)
- Lab 03: S3 Storage Classes, Versioning, and Glacier Lifecycle Rules (Status: Planned)
- Lab 04: Application Load Balancer (ALB) and Auto Scaling Groups (Status: Planned)
- Lab 05: CloudFront OAC (Private S3) and Route 53 DNS Routing (Status: Planned)
- Lab 06: Relational (RDS Multi-AZ) vs NoSQL (DynamoDB + TTL) Databases (Status: Planned)
- Lab 07: IAM Roles, Custom Least-Privilege JSON Policies, and Policy Simulator (Status: Planned)
- Lab 08: Event-Driven Decoupling with SNS, SQS, DLQ, and Lambda (Status: Planned)
- Lab 09: CloudWatch Dashboards, CloudTrail Auditing, and AWS Budgets (Status: Planned)

--------------------------------------------------
4. PART B: AWS SKILL BUILDER & WORKSHOPS.AWS ACHIEVEMENTS

Alongside the 9-Lab project, I actively practice problem-solving scenarios on official AWS training platforms:
- AWS Certified AI Practitioner (AIF-C01): Passed.
- AWS Cloud Quest / Skill Builder Labs: Documenting architecture solutions and earned badges (Folder: skill-builder-achievements/).
- Official AWS Workshops (workshops.aws): Hands-on VPC, Security, and Serverless labs verified in my Free Tier account.

--------------------------------------------------
5. STRICT $0.00 FINOPS DISCIPLINE

To keep my monthly AWS bill at $0.00 while practicing enterprise architectures:
- EC2 instances are stopped immediately after each study session to prevent Public IPv4 and compute charges.
- Local Linux /proc files are used for RAM and Disk telemetry in Lab 1 to avoid CloudWatch custom metric fees ($0.30/metric).
- Paid resources (such as ALB or RDS in later labs) are provisioned, verified with proof-of-work screenshots, and terminated immediately.
