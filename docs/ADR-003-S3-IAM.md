Lab 3 Notes: S3 Lifecycle Rules and IAM Least Privilege

Date: November 2026
Topic: AWS SAA-C03 Study Notes & Lab 3 Documentation

1. What I Built and Configured in Lab 3:
- Created a new Amazon S3 bucket (cloudpulse-logs-zayarhtoo-2026) to store telemetry logs.
- Configured an S3 Lifecycle Rule (MoveToIAandGlacier) via the AWS Console to transition objects to Standard-IA after 30 days and to Glacier Flexible Retrieval after 90 days.
- Created a custom IAM Policy (CloudPulse-Telemetry-LeastPrivilege) using the AWS Visual Editor.
- Implemented the "Least Privilege" principle by restricting the s3:PutObject action to only the specific ARN of my new bucket.

2. SAA-C03 Exam Notes - S3 Storage Classes & Lifecycle Policies:
- Cost Optimization: Moving infrequently accessed data to Standard-IA and archive data to Glacier is a key strategy for reducing S3 storage costs.
- Transitions: Lifecycle rules automate moving data between storage tiers based on object age.

3. SAA-C03 Exam Notes - IAM & Principle of Least Privilege:
- Least Privilege: Never grant broad access. Always restrict to the specific action (e.g., s3:PutObject) and the specific resource ARN.
- Transparency Note: To ensure accuracy and adhere to best practices without prior hands-on workplace experience, I utilized the AWS Visual Editor and Gemini AI assistance to accurately generate the underlying JSON logic for this policy.
