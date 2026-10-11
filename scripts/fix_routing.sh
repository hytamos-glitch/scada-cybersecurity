#!/bin/bash
# Correction de la table de routage Ubuntu SCADA (dual-NIC)
sudo ip route del default via 192.168.30.1 dev ens33
sudo ip route add default via 192.168.112.2 dev ens37
sudo ip route add 192.168.30.0/24 via 192.168.30.1 dev ens33
ping -c 3 192.168.30.1   # FortiGate
ping -c 3 8.8.8.8        # Internet