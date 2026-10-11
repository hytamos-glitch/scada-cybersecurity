#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulateur Modbus TCP – Centrale solaire CSP Nour 1 (NOMAC)
-----------------------------------------------------------
Émule les registres d'une centrale solaire à concentration (CSP)
via le protocole Modbus TCP sur le port 502.

Compatible pymodbus 3.x (pymodbus.datastore + pymodbus.server.StartTcpServer).
"""

# Imports compatibles pymodbus 3.x
from pymodbus.server import StartTcpServer  # Démarrer le serveur Modbus TCP
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore.store import (
    ModbusSequentialDataBlock,
    ModbusInputRegisterBlock,
    ModbusCoilBlock,
    ModbusDiscreteInputBlock,
)

# ---------------------------------------------------------------------------
# Données simulées de la centrale CSP
# ---------------------------------------------------------------------------

# Registres de maintien (holding registers) : températures du fluide en °C
# Reflet des lectures de sondes de température le long du circuit solaire.
HT = 5  # Échelle de température par défaut
hr_values = [25, 38, 52, 67, 80, 45, 30] * 15

# Registres d'entrée (input registers) : irradiance solaire en W/m²
# Valeurs de capteurs de rayonnement (pyranomètres).
HI = 6  # Échelle d'irradiance par défaut
ir_values = [100, 250, 450, 600, 800, 950] * 16

# Bobines (coils) : état des actionneurs (pompes, vannes, héliostats)
co_values = [1] * 100

# Entrées discrètes (discrete inputs) : capteurs logiques (fin de course, alarmes)
di_values = [1] * 100


def build_store():
    """
    Construit les blocs de données Modbus et le contexte de l'esclave.
    """
    # Blocs de données simulés
    hr = ModbusSequentialDataBlock(0, hr_values)   # Holding registers
    ir = ModbusInputRegisterBlock(0, ir_values)    # Input registers
    co = ModbusCoilBlock(0, co_values)             # Coils (actionneurs)
    di = ModbusDiscreteInputBlock(0, di_values)    # Discrete inputs (capteurs)

    # Contexte de l'esclave unique regroupant les quatre blocs
    store = ModbusSlaveContext(
        di=di,
        co=co,
        hr=hr,
        ir=ir,
    )
    return store


def main():
    print("[NOMAC-SCADA] Serveur Modbus TCP actif sur 0.0.0.0:502")

    # Contexte serveur avec un seul esclave (single=True)
    store = build_store()
    context = ModbusServerContext(slaves=store, single=True)

    # Démarrage du serveur Modbus TCP sur toutes les interfaces, port 502
    StartTcpServer(context=context, address=("0.0.0.0", 502))


if __name__ == "__main__":
    main()