#!/usr/bin/env python3
"""
Script di verifica signature PhotoOrganizer
Verifica ESATTAMENTE quali parametri accetta PhotoOrganizer
"""
import sys
import inspect

print("=" * 80)
print("VERIFICA SIGNATURE PHOTOORGANIZER")
print("=" * 80)
print()

# Import modulo
print("Importando photo_organizer_logic...")
try:
    from photo_organizer_logic import SDOrganizerBase, PhotoOrganizer
    print("✓ Import riuscito")
except Exception as e:
    print(f"✗ ERRORE import: {e}")
    sys.exit(1)

print()
print("-" * 80)
print("ANALISI SDOrganizerBase.__init__")
print("-" * 80)

# Ottieni signature
sig_base = inspect.signature(SDOrganizerBase.__init__)
print(f"Signature completa: {sig_base}")
print()

# Analizza parametri
print("Parametri:")
for i, (name, param) in enumerate(sig_base.parameters.items(), 1):
    if name == 'self':
        continue
    
    default_str = " = None" if param.default != inspect.Parameter.empty else ""
    required_str = " [REQUIRED]" if param.default == inspect.Parameter.empty else " [OPTIONAL]"
    
    print(f"  {i}. {name}{default_str}{required_str}")

print()
print("-" * 80)
print("ANALISI PhotoOrganizer")
print("-" * 80)

# Verifica se PhotoOrganizer ha __init__ proprio
if hasattr(PhotoOrganizer, '__init__'):
    # Ottieni il metodo
    init_method = getattr(PhotoOrganizer, '__init__')
    
    # Verifica se è definito in PhotoOrganizer o ereditato
    if '__init__' in PhotoOrganizer.__dict__:
        print("PhotoOrganizer ha __init__ PROPRIO")
        sig_photo = inspect.signature(PhotoOrganizer.__init__)
        print(f"Signature: {sig_photo}")
    else:
        print("PhotoOrganizer EREDITA __init__ da SDOrganizerBase")
        print("Usa la stessa signature di SDOrganizerBase")
else:
    print("PhotoOrganizer non ha __init__")

print()
print("-" * 80)
print("TEST CREAZIONE ISTANZE")
print("-" * 80)

# Test 1: Con brand_name
print("\nTest 1: Creazione con brand_name='Nikon'")
try:
    org1 = PhotoOrganizer(
        brand_name="Nikon",
        pictures_path="/tmp/test",
        logs_path="/tmp/logs"
    )
    print("✓ SUCCESSO!")
    print(f"  org1.brand_name = {org1.brand_name}")
except Exception as e:
    print(f"✗ ERRORE: {e}")
    print(f"  Tipo: {type(e).__name__}")

# Test 2: Con brand (sbagliato)
print("\nTest 2: Creazione con brand='Nikon' (parametro sbagliato)")
try:
    org2 = PhotoOrganizer(
        brand="Nikon",  # Parametro sbagliato
        pictures_path="/tmp/test",
        logs_path="/tmp/logs"
    )
    print("✓ SUCCESSO (inaspettato!)")
    print(f"  org2.brand_name = {getattr(org2, 'brand_name', 'NON DEFINITO')}")
except TypeError as e:
    print(f"✗ TypeError (ATTESO): {e}")
except Exception as e:
    print(f"✗ Altro errore: {e}")
    print(f"  Tipo: {type(e).__name__}")

# Test 3: Senza parametri richiesti
print("\nTest 3: Creazione SENZA parametri (per vedere errore)")
try:
    org3 = PhotoOrganizer()
    print("✓ SUCCESSO (inaspettato!)")
except TypeError as e:
    print(f"✗ TypeError (ATTESO): {e}")
    print("  Mostra quali parametri sono richiesti:")
    print(f"  {e}")

print()
print("=" * 80)
print("VERIFICA COMPLETATA")
print("=" * 80)
print()
print("RIEPILOGO:")
print("  - Se Test 1 è ✓ e Test 2 è ✗ → Tutto OK, usa brand_name")
print("  - Se entrambi ✓ → C'è un problema nella signature")
print("  - Se entrambi ✗ → C'è un problema serio")
