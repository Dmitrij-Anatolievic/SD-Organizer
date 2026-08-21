#!/usr/bin/env python3
"""
Test SUPER SMART PATH LOGIC - Gestione Intelligente Anno E Mese
"""
import os
import sys

print("=" * 80)
print("TEST SUPER SMART PATH LOGIC - GESTIONE ANNO + MESE")
print("=" * 80)

def super_smart_path_logic(pictures_path, year_str, month_str, day_folder):
    """
    Replica ESATTA della logica super intelligente implementata.
    Controlla se anno e/o mese sono già nel path.
    """
    base_path = os.path.normpath(pictures_path)
    path_parts = base_path.split(os.sep)
    
    # Check what's already in the path
    year_in_path = year_str in path_parts
    
    # For month, check if last part is the month
    month_in_path = False
    if year_in_path and len(path_parts) >= 2:
        last_part = path_parts[-1] if path_parts else ""
        if last_part.lower() == month_str.lower():
            month_in_path = True
    
    # Build the path intelligently
    if year_in_path:
        if month_in_path:
            # Both year AND month in path - add only day
            day_path = os.path.join(base_path, day_folder)
            print(f"  ℹ️  Anno+Mese già nel path → Aggiungi solo: {day_folder}")
        else:
            # Only year in path - add month + day
            day_path = os.path.join(base_path, month_str, day_folder)
            print(f"  ℹ️  Anno già nel path → Aggiungi: {month_str}\\{day_folder}")
    else:
        # Normal case - add year + month + day
        day_path = os.path.join(base_path, year_str, month_str, day_folder)
        print(f"  ✅ Path normale → Aggiungi: {year_str}\\{month_str}\\{day_folder}")
    
    return day_path


year = "2025"
month = "Ottobre"
day = "21_Prova"

print("\n" + "=" * 80)
print("SCENARIO 1: Path base SENZA anno")
print("=" * 80)
path1 = r"C:\Users\Dmitr\Desktop\Nikon"
result1 = super_smart_path_logic(path1, year, month, day)

print(f"Input:  {path1}")
print(f"Output: {result1}")
print(f"Atteso: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova")

# Verifica
expected1 = os.path.normpath(r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre\21_Prova")
result1_norm = os.path.normpath(result1)
match1 = result1_norm == expected1
print(f"✅ CORRETTO" if match1 else f"❌ SBAGLIATO")

print("\n" + "=" * 80)
print("SCENARIO 2: Path CON anno (2025)")
print("=" * 80)
path2 = r"C:\Users\Dmitr\Desktop\Nikon\2025"
result2 = super_smart_path_logic(path2, year, month, day)

print(f"Input:  {path2}")
print(f"Output: {result2}")
print(f"Atteso: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova")

# Verifica
expected2 = os.path.normpath(r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre\21_Prova")
result2_norm = os.path.normpath(result2)
match2 = result2_norm == expected2

# Verifica che NON abbia doppio anno
has_double_year = result2.count("2025") > 1 and f"2025{os.sep}2025" in result2
print(f"Doppio anno? {'❌ BUG!' if has_double_year else '✅ NO'}")
print(f"✅ CORRETTO" if match2 and not has_double_year else f"❌ SBAGLIATO")

print("\n" + "=" * 80)
print("SCENARIO 3: Path CON anno E mese (2025\\Ottobre)")
print("=" * 80)
path3 = r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre"
result3 = super_smart_path_logic(path3, year, month, day)

print(f"Input:  {path3}")
print(f"Output: {result3}")
print(f"Atteso: C:\\Users\\Dmitr\\Desktop\\Nikon\\2025\\Ottobre\\21_Prova")

# Verifica
expected3 = os.path.normpath(r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre\21_Prova")
result3_norm = os.path.normpath(result3)
match3 = result3_norm == expected3

# Verifica che NON abbia doppio mese
has_double_month = result3.count("Ottobre") > 1 and f"Ottobre{os.sep}Ottobre" in result3
print(f"Doppio mese? {'❌ BUG!' if has_double_month else '✅ NO'}")
print(f"✅ CORRETTO" if match3 and not has_double_month else f"❌ SBAGLIATO")

print("\n" + "=" * 80)
print("RIEPILOGO FINALE")
print("=" * 80)

all_tests = [
    ("Path base (Nikon)", match1),
    ("Path + anno (Nikon\\2025)", match2 and not has_double_year),
    ("Path + anno + mese (Nikon\\2025\\Ottobre)", match3 and not has_double_month)
]

all_passed = all(result for _, result in all_tests)

for test_name, passed in all_tests:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {test_name}")

print("\n" + "=" * 80)
if all_passed:
    print("✅✅✅ PERFETTO! TUTTI I TEST PASSATI! ✅✅✅")
    print("\nCOMPORTAMENTO CORRETTO:")
    print("  1. Nikon → Aggiungi 2025\\Ottobre\\21_Prova")
    print("  2. Nikon\\2025 → Aggiungi Ottobre\\21_Prova")
    print("  3. Nikon\\2025\\Ottobre → Aggiungi 21_Prova")
else:
    print("❌ ALCUNI TEST FALLITI")
print("=" * 80)
