# ADR-009: Observability & Security Auditing (CloudWatch & CloudTrail)

* **Status:** Accepted (Lab Verified)
* **Date:** 2026-11-19
* **Project:** CloudPulse AWS Architecture (SAA-C03 Study Project)
* **Artifacts:** [`observability/cloudwatch-dashboard-body.json`](../observability/cloudwatch-dashboard-body.json) | [`observability/sample-cloudtrail-security-event.json`](../observability/sample-cloudtrail-security-event.json)

## Context & Problem Statement

Deploying decoupled serverless pipelines and strict IAM least-privilege policies is insufficient without operational visibility and tamper-evident audit logging. Operations teams need real-time telemetry into queue backlogs, Lambda execution errors, and DynamoDB capacity consumption, while security teams require an immutable audit trail of who modified cloud resources or assumed IAM roles.

## Architecture Overview

```text
+-------------------------------------------------------------------------+
|                    CloudPulse Observability & Auditing                  |
+------------------------------------+------------------------------------+
|   OPERATIONAL METRICS & LOGS       |   GOVERNANCE & API AUDIT TRAIL     |
|      (Amazon CloudWatch)           |         (AWS CloudTrail)           |
+------------------------------------+------------------------------------+
| - Lambda: Invocations & Errors     | - Management Events (90-Day Free)  |
| - SQS: Sent, Deleted & DLQ Depth   | - Tracks PutDashboard, Lambda,     |
| - DynamoDB: Read/Write Capacity    |   SQS, and STS AssumeRole calls    |
| - Unified Dashboard JSON as Code   | - Immutable Who/When/Where JSON    |
+------------------------------------+------------------------------------+
```

## Architectural Decisions

### 1. Unified Operational Monitoring via Amazon CloudWatch Dashboard
* Provisioned **`CloudPulse-Operations-Dashboard`** in `us-east-1` consolidating telemetry across the entire Lab 8 serverless ingestion pipeline into a single pane of glass:
  * **Compute (`AWS/Lambda`):** `Invocations` and `Errors` for `CloudPulse-Telemetry-Ingestor`.
  * **Messaging (`AWS/SQS`):** `NumberOfMessagesSent`, `NumberOfMessagesDeleted` for `CloudPulse-Telemetry-Queue`, and `ApproximateNumberOfMessagesVisible` for `CloudPulse-Telemetry-DLQ`.
  * **Database (`AWS/DynamoDB`):** `ConsumedWriteCapacityUnits` and `ConsumedReadCapacityUnits` for `CloudPulse-Telemetry`.
* Exported the dashboard source definition to [`observability/cloudwatch-dashboard-body.json`](../observability/cloudwatch-dashboard-body.json) for version-controlled infrastructure documentation.

### 2. API Governance & Security Auditing via AWS CloudTrail Event History
* Leveraged AWS CloudTrail's built-in **Event History** (90-day management event retention at **$0.00** cost) to audit control-plane API calls and IAM role executions without provisioning paid multi-region trails or S3 delivery buckets.
* Verified real-time audit capture of dashboard creation (`PutDashboard` on `monitoring.us-east-1.amazonaws.com`, `eventID: bbfb91a3-9e0c-4fe8-95a0-0e37ada5029b`), confirming `readOnly: false`, `managementEvent: true`, and `TLSv1.3` session details.

## Live Verification Summary

* **CloudWatch Dashboard:** Created `CloudPulse-Operations-Dashboard` with all 3 metric widgets rendering live `us-east-1` namespaces.
* **CloudTrail Event History:** Inspected live management event record JSON (`requestID: 6cb575c4-2e9e-489d-94e0-38367cbeacb8`) confirming `eventSource`, `eventName`, `resources` (`AWS::CloudWatch::Metric`), and `tlsDetails`, sanitized and documented in [`observability/sample-cloudtrail-security-event.json`](../observability/sample-cloudtrail-security-event.json).

## Cost Hygiene & Consequences

* **Cost Footprint ($0.00):**
  * **CloudWatch:** 1 dashboard with 7 metrics stays well inside the AWS Always Free Tier limit (up to 3 dashboards and 50 metrics/month free).
  * **CloudTrail:** Viewing 90-day Event History is completely free ($0.00); no custom Trails were created.
  * **Compute & Databases:** EC2 (`zayartesting1`) remains stopped and Lab 6 RDS remains deleted, keeping total ongoing project cost at **$0.00**.
* **Positive:** Clear separation between operational performance monitoring (CloudWatch) and security/compliance auditing (CloudTrail), reinforced for SAA-C03 exam scenarios.
* **Trade-offs:** Default CloudTrail Event History retains management events for 90 days; production compliance beyond 90 days or data-plane event logging (`s3:GetObject`, `dynamodb:PutItem`) would require a dedicated CloudTrail Trail streaming to S3 with Object Lock / Glacier lifecycle rules.

## Learning Context & AI Assistance Disclosure

Built as the final lab of my 9-lab hands-on study repository as a first-year Computer Science undergraduate preparing for the **AWS Certified Solutions Architect – Associate (SAA-C03)** exam. I transparently use **Gemini AI** as a study mentor for architecture review, JSON schema structuring, and documentation formatting while personally configuring every AWS service, dashboard, and audit verification in my account.
