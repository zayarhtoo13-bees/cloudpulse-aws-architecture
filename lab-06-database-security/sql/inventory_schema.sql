-- Lab 6: CloudPulse RDS MySQL Inventory Verification Script
-- Executed from EC2 (zayartesting1) over Private VPC Security Group Chaining

CREATE DATABASE IF NOT EXISTS cloudpulse_inventory;
USE cloudpulse_inventory;

CREATE TABLE IF NOT EXISTS servers (
    instance_id VARCHAR(50) PRIMARY KEY,
    role VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL
);

INSERT INTO servers (instance_id, role, status)
VALUES ('i-web-01', 'Web-Server', 'Active');

SELECT * FROM servers;
