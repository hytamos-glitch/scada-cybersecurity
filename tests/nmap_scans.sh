#!/bin/bash
# À exécuter UNIQUEMENT dans le laboratoire isolé (VMware host-only)
nmap -sn 192.168.28.0/24
nmap -sV -p 22,443,80 192.168.28.2
nmap -sV 192.168.30.0/24
nmap --script vuln 192.168.28.2