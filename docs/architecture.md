# Architecture de cybersécurité – Centrale solaire CSP Nour 1 (NOMAC)

<img src="../images/topologie_vmware.png" width="800" alt="Topologie du laboratoire (FortiGate VM, zones WAN / DMZ / SCADA)">

Ce document décrit l'architecture du laboratoire de simulation (VMware Workstation
Pro) conçue pour la protection des systèmes SCADA et du réseau industriel de la
centrale Nour 1.

## Topologie des zones

| Zone      | Réseau VMware            | Réseau            | Rôle                     |
|-----------|--------------------------|-------------------|--------------------------|
| Zone WAN  | VMnet1 Host-only         | 192.168.28.0/24   | Zone WAN                 |
| Zone DMZ  | VMnet3 Host-only         | 192.168.20.0/24   | Zone DMZ                 |
| Zone SCADA| VMnet4 Host-only         | 192.168.30.0/24   | Zone SCADA               |

## Interfaces FortiGate VM (v7.2.13)

| Interface | Zone          | Adresse IP        | Rôle  |
|-----------|---------------|-------------------|-------|
| port1     | Zone WAN      | 192.168.28.2/24   | WAN   |
| port2     | Zone DMZ      | 192.168.20.1/24   | DMZ   |
| port3     | Zone SCADA    | 192.168.30.1/24   | LAN   |

## Machines virtuelles

| Machine                              | Adresse IP        | Zone   | Rôle / services                                 |
|--------------------------------------|-------------------|--------|--------------------------------------------------|
| Kali Linux 2025                      | 192.168.28.50     | WAN    | Poste d'attaque (tests d'intrusion)              |
| Windows 10 + Splunk Enterprise 10.2.2| 192.168.28.x      | WAN    | Supervision SIEM, collecte des journaux          |
| Ubuntu 22.04 SCADA                   | 192.168.30.10 (ens33 VMnet4, ens37 NAT) | SCADA | ScadaBR 1.0CE + Tomcat 6.0.53 + simulateur Modbus pymodbus |

## Politiques firewall

| Politique                | Source→Destination | Action | Journalisation |
|--------------------------|--------------------|--------|----------------|
| Allow-SCADA-to-DMZ       | port3 → port2      | ALLOW  | Activée        |
| Allow-WAN-to-DMZ         | port1 → port2      | ALLOW  | Activée        |
| Block-WAN-to-SCADA       | port1 → port3      | DENY   | Activée        |

## Défense en profondeur

L'architecture repose sur **5 couches de protection** :

1. **Contrôle périmétrique FortiGate (deny-all)** : filtrage strict par défaut,
   seules les flux explicitement autorisés transitent entre les zones.
2. **Isolation VLAN/DMZ** : cloisonnement physique et logique entre WAN, DMZ et
   SCADA (réseaux host-only VMware dédiés).
3. **Chiffrement VPN IPsec** (IKEv2, AES-256-GCM) : protection des accès distants
   et des échanges entre zones.
4. **IPS industriel** : profil de détection et de blocage dédié aux protocoles
   industriels et aux attaques réseau (flood, force brute, anomalies Modbus).
5. **Supervision SIEM Splunk** : centralisation, corrélation et analyse des
   journaux FortiGate en temps réel.