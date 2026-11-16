#!/bin/bash
echo "==================================================="
echo " Cloudpulse network & security audit "
echo "==================================================="

echo "(1) VPC routing & Default Gateway:"
ip route | grep default

echo -e "\n(2) DNS resolution Test (amazon.com):"
nslookup amazon.com | head -n 6

echo -e "\n(3) Active Listening TCP Ports:" 
sudo ss -tlnp | grep LISTEN

echo -e "\n(4) Recent Apache Website Visitor Logs (Last 5):"
sudo tail -n 5 /var/log/httpd/access_log
echo "================================================="
