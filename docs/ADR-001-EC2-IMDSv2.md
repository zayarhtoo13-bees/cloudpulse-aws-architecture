Lab 1 Notes: EC2 Web Server, IMDSv2, and Linux /proc Telemetry

Date: November 2026
Topic: AWS SAA-C03 Study Notes & Lab 1 Documentation

1. What I Built in Lab 1:
- Launched an Amazon Linux 2023 EC2 instance (t3.micro) in a public subnet.
- Configured the Security Group to allow Port 22 (SSH) and Port 80 (HTTP).
- Installed Apache web server (httpd).
- Used a Python script (created with help from Gemini AI) to read CPU, RAM, Disk, and EC2 metadata every 3 seconds and save it to /var/www/html/telemetry.json.
- Created a Linux systemd service (cloudpulse.service) so the Python script runs automatically in the background.

2. SAA-C03 Exam Note - Why I used IMDSv2 instead of IMDSv1:
- EC2 instances use the internal IP address 169.254.169.254 to check their own metadata (like Instance ID and Availability Zone).
- Old IMDSv1 only uses a simple GET request. If a website has a security bug (SSRF), hackers can steal temporary IAM credentials from IMDSv1.
- IMDSv2 is safer because it requires a PUT request first to get a secret session token before reading metadata. My Python script uses IMDSv2.

3. SAA-C03 Exam Note - Why I read /proc files instead of using CloudWatch:
- By default, AWS CloudWatch only checks EC2 CPU, Network, and Disk I/O. It does NOT check RAM (Memory) or free disk space.
- Sending custom RAM metrics to CloudWatch using the CloudWatch Agent costs $0.30 per metric per month.
- To keep my cost at $0.00, my Python script reads Linux files (/proc/meminfo and /proc/loadavg) directly on the server for free.

4. Mistakes I Made and How I Fixed Them (Troubleshooting):
- Mistake 1: Apache was still "inactive" after I enabled it.
  Fix: I learned that I needed to run "sudo systemctl start httpd" to start it immediately, and "ss -tulpn | grep :80" (with lowercase ss) to check if Port 80 was listening.
- Mistake 2: Browser showed "404 Not Found nginx" and "403 Forbidden".
  Fix: I typed one wrong number in the Public IP address at first. Also, Apache showed 403 Forbidden because /var/www/html/index.html did not exist yet.
- Mistake 3: Typo in file path (/usr/loacl/bin instead of /usr/local/bin) and PermissionError when checking Python syntax.
  Fix: Fixed the spelling of "local" and added "sudo" before "python3 -m py_compile" because regular ec2-user cannot write to /usr/local/bin.
