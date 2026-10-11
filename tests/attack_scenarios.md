# Scénarios de tests d'intrusion – Laboratoire SCADA Nour 1 (NOMAC)

> **Avertissement** : les tests décrits dans ce document sont réalisés
> **uniquement en laboratoire isolé VMware (réseaux host-only)**, à but
> académique. Aucune infrastructure de production n'est visée.

## Contexte

- **Attaquant :** Kali Linux `192.168.28.50` (zone WAN)
- **Cible :** FortiGate `192.168.28.2` et zone SCADA `192.168.30.0/24` (Nour 1)
- **Capteur :** FortiGate VM (pare-feu, IPS) → journaux centralisés dans Splunk

## Tableau des scénarios

| Scénario                           | Outil      | Cible               | Détecté | Bloqué   | Journalisé |
|------------------------------------|------------|---------------------|---------|----------|------------|
| Scan reconnaissance WAN            | Nmap       | 192.168.28.0/24     | Oui     | Partiel  | Oui        |
| Accès zone SCADA depuis WAN        | Nmap       | 192.168.30.0/24     | Oui     | Oui      | Oui        |
| Inondation ICMP                    | hping3     | 192.168.28.2        | Oui     | Oui      | Oui        |
| Inondation SYN (443)               | hping3     | 192.168.28.2        | Oui     | Oui      | Oui        |
| Force brute SSH                    | Hydra      | 192.168.28.2        | Oui     | Oui      | Oui        |
| Scan de vulnérabilités             | Nmap NSE   | 192.168.28.2        | Oui     | Journalisé | Oui      |

## Commandes utilisées

- Scan reconnaissance WAN (découverte d'hôtes) :

```bash
nmap -sn 192.168.28.0/24
```

- Tentative d'accès à la zone SCADA depuis le WAN :

```bash
nmap -sV 192.168.30.0/24
```

- Inondation ICMP (flood ping) vers le FortiGate :

```bash
sudo hping3 -1 --flood -V 192.168.28.2
```

- Inondation SYN (DoS, port 443) vers le FortiGate :

```bash
sudo hping3 -S --flood -p 443 192.168.28.2
```

- Force brute SSH (Hydra, dictionnaire rockyou) :

```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://192.168.28.2 -t 4 -V -f
```

- Scan de vulnérabilités (Nmap NSE) :

```bash
nmap --script vuln -p 22,443 192.168.28.2
```

## Bilan

- **5 scénarios sur 6** détectés et bloqués.
- **100 %** des tentatives journalisées dans Splunk.