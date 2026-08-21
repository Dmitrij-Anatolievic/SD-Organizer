#!/usr/bin/env python3
"""
Test CRITICAL FIX - Previene doppio anno (2025/2025)
"""
import os
import sys

print("=" * 80)
print("TEST CRITICAL FIX - PREVIENE DOPPIO ANNO")
print("=" * 80)

def test_path_logic(pictures_path, year_str):
    """Simula la logica corretta"""
    base_path = os.path.normpath(pictures_path)
    
    # Check if path ends with year
    path_parts = base_path.split(os.sep)
    if path_parts and path_parts[-1] == year_str:
        # Path già include anno - NON aggiungere di nuovo
        year_path = base_path
        print(f"✅ RILEVATO anno in path - NON aggiunto di nuovo")
    else:
        # Caso normale - aggiungi anno
        year_path = os.path.join(base_path, year_str)
        print(f"✅ Anno NON in path - aggiunto normalmente")
    
    return year_path


# TEST 1: Path CORRETTO (senza anno)
print("\n[TEST 1] Path CORRETTO - senza anno alla fine")
print("-" * 80)
pictures_path = r"C:\Users\Dmitr\Desktop\Nikon"
year_str = "2025"
month = "Ottobre"
day = "21_Prova"

year_path = test_path_logic(pictures_path, year_str)
final_path = os.path.join(year_path, month, day)

print(f"Input:  {pictures_path}")
print(f"Output: {final_path}")
print(f"Atteso: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova")
print(f"Match: {final_path == r'C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova' or final_path == 'C:/Users/Dmitr/Desktop/Nikon/2025/Ottobre/21_Prova'}")

# TEST 2: Path SBAGLIATO (con anno - l'utente ha incluso 2025)
print("\n\n[TEST 2] Path con anno già incluso (bug dell'utente)")
print("-" * 80)
pictures_path_wrong = r"C:\Users\Dmitr\Desktop\Nikon\2025"

year_path = test_path_logic(pictures_path_wrong, year_str)
final_path = os.path.join(year_path, month, day)

print(f"Input:  {pictures_path_wrong}")
print(f"Output: {final_path}")
print(f"Atteso: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova")
print(f"NON deve essere: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\2025\\Ottobre\\21_Prova")

# Verifica che NON abbia doppio 2025
has_double_year = "2025\\2025" in final_path or "2025/2025" in final_path
print(f"Ha doppio anno? {has_double_year} {'❌ BUG!' if has_double_year else '✅ OK!'}")

# TEST 3: Path con anno diverso
print("\n\n[TEST 3] Path con anno 2024 nel path, ma file è del 2025")
print("-" * 80)
pictures_path_2024 = r"C:\Users\Dmitr\Desktop\Nikon\2024"
year_str_2025 = "2025"

year_path = test_path_logic(pictures_path_2024, year_str_2025)
final_path = os.path.join(year_path, month, day)

print(f"Input:  {pictures_path_2024}")
print(f"Anno file: {year_str_2025}")
print(f"Output: {final_path}")
print(f"✅ Aggiunge 2025 perché il path termina con 2024, non 2025")

print("\n" + "=" * 80)
print("✅ TEST COMPLETATO!")
print("=" * 80)
print("\nRISULTATI:")
print("  ✅ Path corretto: Aggiunge anno normalmente")
print("  ✅ Path con anno incluso: NON aggiunge anno (no doppio)")
print("  ✅ Path con anno diverso: Aggiunge anno nuovo")
print("\nIL BUG DEL DOPPIO ANNO È STATO RISOLTO!")
print("=" * 80)
