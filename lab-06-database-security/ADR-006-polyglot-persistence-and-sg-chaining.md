# ADR-006: Polyglot Database Selection and Security Group Chaining

* **Status:** Accepted (Lab Verified)
* **Date:** 2026-11-19
* **Context:** CloudPulse AWS Architecture (SAA-C03 Study Project)

## Context & Problem Statement

The CloudPulse monitoring architecture handles two fundamentally different data workloads:
1. **High-volume, semi-structured time-series telemetry** (CPU metrics, dynamic alert payloads) that requires fast key-based lookups and automatic expiration.
2. **Structured server inventory records** (instance IDs, roles, ownership, relational metadata) requiring strict ACID compliance and SQL querying.

Additionally, the relational database must be protected from public internet exposure and resilient to dynamic EC2 IP address changes when instances stop, start, or scale.

## Architectural Decisions

### Decision 1: Polyglot Persistence (DynamoDB + RDS MySQL)
* **Telemetry -> Amazon DynamoDB:** Chosen for single-digit millisecond latency, schemaless attributes (handling optional fields like `AlertMessage` without schema migrations), and native composite key ordering (`InstanceID` + `Timestamp`).
* **Inventory -> Amazon RDS (MySQL):** Chosen for relational integrity, standard SQL support, and managed patching/backups without OS-level database administration overhead.

### Decision 2: DynamoDB TTL over Scheduled Cleanup Jobs
* Enabled **TTL (`ExpireAt`)** instead of running custom cron scripts or Lambda `DeleteItem` loops.
* **Trade-off:** Deletion occurs asynchronously within ~48 hours rather than instantaneously, which is acceptable for log retention and eliminates all Write Capacity Unit (WCU) deletion charges.

### Decision 3: Security Group Chaining + Private Isolation
* Configured RDS with **Public Access: No** and restricted `CloudPulse-RDS-SG` inbound port `3306` exclusively to the EC2 security group (`launch-wizard-1`) rather than static IP/CIDR blocks.
* **Why:** Security Group Chaining decouples firewall rules from ephemeral IP addresses. In a production Auto Scaling Group (ASG), newly launched EC2 instances that inherit the application Security Group automatically gain database access without manual firewall edits.

## Consequences

* **Positive:**
  * Clear separation of hot telemetry vs. relational inventory workloads.
  * Zero public attack surface on the RDS endpoint.
  * 100% query efficiency on DynamoDB partition lookups (`0.5 RCU` for 2 items) and $0 deletion overhead via TTL.
* **Negative / Trade-offs:**
  * Maintaining two distinct database paradigms increases application client complexity (AWS SDK for DynamoDB + SQL driver for RDS).
  * In this sandbox lab, RDS runs as Single-AZ in the Default VPC for Free Tier compliance; a production rollout would require dedicated private database subnets across multiple Availability Zones (**Multi-AZ**), **Secrets Manager** for credential rotation, and **VPC Gateway Endpoints** for private DynamoDB routing.
