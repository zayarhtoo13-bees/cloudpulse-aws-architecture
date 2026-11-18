Lab 4 Notes: High Availability with Application Load Balancer & Auto Scaling

Date: November 2026
Topic: AWS SAA-C03 Study Notes & Lab 4 Documentation

1. What I Built and Configured in Lab 4:
- Created a Launch Template (CloudPulse-Web-Template) using Amazon Linux 2023 (t3.micro) and a custom Bash User Data script to automatically install and start Apache (httpd) with IMDSv2 instance ID display.
- Configured a Security Group (CloudPulse-Web-SG) allowing inbound HTTP traffic on Port 80.
- Deployed an Auto Scaling Group (CloudPulse-ASG) across multiple Availability Zones (us-east-1a, us-east-1b) with Desired: 2, Min: 2, Max: 3 capacity and ELB health checks enabled.
- Integrated an Internet-facing Application Load Balancer (CloudPulse-ALB) and Target Group (CloudPulse-TG) to distribute incoming traffic evenly across healthy instances.

2. SAA-C03 Exam Notes - High Availability & Load Balancing:
- Multi-AZ Deployment: Spreading EC2 instances across multiple Availability Zones protects applications against single data center failures.
- ALB Routing: Application Load Balancers operate at Layer 7 (HTTP/HTTPS) and distribute traffic across registered targets in a Target Group.
- Auto Scaling Self-Healing: When ELB health checks are enabled, ASG automatically terminates unhealthy instances and launches replacements to maintain desired capacity.
- Transparency Note: As a first-year Computer Science student without prior hands-on workplace experience, I utilized Gemini AI assistance to structure the IMDSv2 User Data script, troubleshoot target group attachment, and document these architectural decisions.
