# Lab 6: Polyglot Persistence (DynamoDB & RDS) and Security Group Chaining

This lab demonstrates a two-tier AWS database architecture for the **CloudPulse** monitoring project, combining NoSQL (**Amazon DynamoDB**) for high-velocity telemetry logs and relational SQL (**Amazon RDS for MySQL**) for structured server inventory, secured via **VPC Security Group Chaining**.

## Architecture Overview

```text
                       [ AWS Region: us-east-1 (Default VPC) ]
                                          |
    +-------------------------------------+-------------------------------------+
    |                                                                           |
    v                                                                           v
[ Amazon DynamoDB ]                                                  [ EC2 Compute Tier ]
Table: CloudPulse-Telemetry                                          Instance: zayartesting1
- PK: InstanceID (String)                                            Private IP: 172.31.18.15
- SK: Timestamp (String)                                             SG: launch-wizard-1
- Mode: On-Demand                                                               |
- TTL: ExpireAt (0 WCU auto-delete)                                             | TCP 3306
                                                                                | (Private VPC Traffic)
                                                                                v
                                                                     [ Amazon RDS (MySQL 8.4) ]
                                                                     DB: cloudpulse-inventory-db
                                                                     Class: db.t4g.micro (Single-AZ)
                                                                     Public Access: No (Isolated)
                                                                     SG: CloudPulse-RDS-SG
                                                                     Inbound: Allow 3306 ONLY from
                                                                              launch-wizard-1 SG ID
```

## Lab Objectives & Implementation

### Part 1: Amazon DynamoDB (NoSQL Telemetry Store)
* **Table Name:** `CloudPulse-Telemetry`
* **Primary Key Schema:** Composite Key — Partition Key `InstanceID` (`String`) + Sort Key `Timestamp` (`String`) for chronological range queries per server.
* **Capacity Mode:** On-Demand (pay-per-request, suitable for unpredictable lab/telemetry workloads).
* **Schemaless Ingestion:** Inserted telemetry items for `i-web-01` with varying attributes (`Status: Healthy` on one record, `AlertMessage: High CPU spike` on another) to verify flexible schema support.
* **Query Efficiency Verification:** Executed a targeted `Query` (instead of a full-table `Scan`) on `InstanceID = i-web-01`:
  * **Items Returned:** `2`
  * **Items Scanned:** `2`
  * **Efficiency:** `100%`
  * **Capacity Consumed:** `0.5 RCU`
* **Automated Data Lifecycle (TTL):** Enabled **Time to Live (TTL)** on attribute `ExpireAt` (Unix Epoch timestamp) so expired telemetry logs are purged automatically in the background (typically within 48 hours) at **0 WCU cost**.

### Part 2: Amazon RDS for MySQL (Relational Inventory Store)
* **DB Identifier:** `cloudpulse-inventory-db`
* **Engine & Tier:** MySQL `8.4.11`, Sandbox/Free Tier (`db.t4g.micro`, Single-AZ, `20 GiB` gp2 SSD, Storage Autoscaling disabled).
* **Network Isolation:** Deployed into the Default VPC with **Public Access: No** so the instance receives no public IP address and is unreachable from the public internet.
* **Cost Guardrails:** Disabled RDS Extended Support, Enhanced Monitoring, RDS Proxy, and CloudWatch Log Exports.

### Part 3: Security Group Chaining (Zero-IP Firewalling)
Instead of hardcoding an EC2 private IP address or opening `0.0.0.0/0` on port `3306`, the RDS security group (`CloudPulse-RDS-SG`) was configured to reference the EC2 security group (`launch-wizard-1`) directly as its inbound source:

| Security Group | Direction | Type / Port | Source | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `CloudPulse-RDS-SG` | Inbound | MySQL/Aurora (`TCP 3306`) | `launch-wizard-1` (EC2 SG ID) | Allow database traffic strictly from authorized EC2 instances |

## Connectivity & SQL Verification

Connected to the EC2 instance (`zayartesting1`) via EC2 Instance Connect, installed the MariaDB client on Amazon Linux 2023, and verified private connectivity over port `3306`:

```bash
# 1. Install MySQL-compatible client on Amazon Linux 2023
sudo dnf install -y mariadb105

# 2. Connect to private RDS endpoint over VPC network
mysql -h cloudpulse-inventory-db.<endpoint-hash>.us-east-1.rds.amazonaws.com -P 3306 -u admin -p
```

### Verification Output
During initial authentication testing, MySQL returned `Access denied for user 'admin'@'172.31.18.15'`, confirming traffic traversed the internal VPC private network rather than a public route. Upon entering the correct password, schema creation and CRUD operations succeeded:

```text
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Server version: 8.4.11 Source distribution

MySQL [(none)]> CREATE DATABASE cloudpulse_inventory;
Query OK, 1 row affected (0.027 sec)

MySQL [(none)]> USE cloudpulse_inventory;
Database changed

MySQL [cloudpulse_inventory]> CREATE TABLE servers (
    -> instance_id VARCHAR(50),
    -> role VARCHAR(50),
    -> status VARCHAR(20)
    -> );
Query OK, 0 rows affected (0.054 sec)

MySQL [cloudpulse_inventory]> INSERT INTO servers VALUES ('i-web-01', 'Web-Server', 'Active');
Query OK, 1 row affected (0.011 sec)

MySQL [cloudpulse_inventory]> SELECT * FROM servers;
+-------------+------------+--------+
| instance_id | role       | status |
+-------------+------------+--------+
| i-web-01    | Web-Server | Active |
+-------------+------------+--------+
1 row in set (0.002 sec)
```

## Real-World Troubleshooting Notes

1. **VPC Alignment Requirement:** RDS initially defaulted to `Create new VPC`. Because Security Group Chaining requires resources to reside in the same VPC (and an RDS instance's VPC cannot be changed after creation), the deployment was switched to the `Default VPC` before launch.
2. **AWS Security Group Rule Replacement Constraint:** Attempting to overwrite the auto-generated `/32` IPv4 CIDR inbound rule directly with a Security Group ID throws:
   > `You may not specify a referenced group id for an existing IPv4 CIDR rule`

   **Resolution:** Delete the existing CIDR rule row completely, then click **Add rule** to create a fresh rule referencing the EC2 Security Group ID.
3. **Client Flag Compatibility:** The AWS RDS console suggests `--ssl-mode=VERIFY_IDENTITY` (MySQL 8 client syntax), whereas Amazon Linux 2023's `mariadb105` package uses `--ssl-verify-server-cert` when verifying with `global-bundle.pem`.

## Cost Hygiene & Teardown

To maintain zero unexpected AWS charges after lab verification:
* Deleted RDS instance `cloudpulse-inventory-db` with **Create final snapshot** and **Retain automated backups** unchecked.
* Stopped EC2 instance `zayartesting1`.
* Left the `CloudPulse-Telemetry` On-Demand DynamoDB table (2 tiny items, $0 storage/idle cost) and unused security groups intact.

## Learning Context & AI Assistance Disclosure

This repository is part of my hands-on study journey as a first-year Computer Science undergraduate preparing for the **AWS Certified Solutions Architect – Associate (SAA-C03)** exam. I transparently use **Gemini AI** as an interactive study mentor to design lab scenarios, review AWS console configurations, troubleshoot live errors, and structure technical documentation, while personally executing and verifying every resource and command in my AWS account.
