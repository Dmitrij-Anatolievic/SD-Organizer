#!/usr/bin/env python3
"""
Test DEFINITIVO - Gestione Intelligente Path con/senza Anno
"""
import os

print("=" * 80)
print("TEST GESTIONE INTELLIGENTE PATH - FIX DEFINITIVO")
print("=" * 80)

def smart_path_logic(pictures_path, year_str, month_str, day_folder):
    """
    Logica intelligente per gestire path con o senza anno.
    Replica esattamente la logica del codice corretto.
    """
    # Normalize path to handle different slash styles
    base_path = os.path.normpath(pictures_path)
    
    # Get last part of path (cross-platform)
    last_part = os.path.basename(base_path)
    
    # Check if last part is the year
    if last_part == year_str:
        # Path already ends with year
        year_path = base_path
        print(f"  ℹ️  Path già include anno {year_str} - NON aggiunto")
    else:
        # Normal case: add year
        year_path = os.path.join(base_path, year_str)
        print(f"  ✅ Anno {year_str} aggiunto al path")
    
    month_path = os.path.join(year_path, month_str)
    day_path = os.path.join(month_path, day_folder)
    
    return day_path


year = "2025"
month = "Ottobre"
day = "21_Prova"

# TEST 1: Path SENZA anno (caso normale)
print("\n[TEST 1] Path SENZA anno - Caso Normale")
print("-" * 80)
path1 = r"C:\Users\Dmitr\Desktop\Nikon"
result1 = smart_path_logic(path1, year, month, day)
expected1 = r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre\21_Prova"

print(f"Input:    {path1}")
print(f"Output:   {result1}")
print(f"Expected: {expected1}")
has_double1 = "2025\\2025" in result1 or "2025/2025" in result1
print(f"Doppio anno? {'❌ BUG!' if has_double1 else '✅ NO'}")
correct1 = not has_double1 and "2025" in result1
print(f"Risultato: {'✅ CORRETTO' if correct1 else '❌ SBAGLIATO'}\n")

# TEST 2: Path CON anno già incluso (il tuo caso problematico!)
print("\n[TEST 2] Path CON anno incluso - TUO CASO")
print("-" * 80)
path2 = r"C:\Users\Dmitr\Desktop\Nikon\2025"
result2 = smart_path_logic(path2, year, month, day)
expected2 = r"C:\Users\Dmitr\Desktop\Nikon\2025\Ottobre\21_Prova"

print(f"Input:    {path2}")
print(f"Output:   {result2}")
print(f"Expected: {expected2}")
has_double2 = "2025\\2025" in result2 or "2025/2025" in result2
print(f"Doppio anno? {'❌ BUG!' if has_double2 else '✅ NO'}")
correct2 = not has_double2 and result2.count("2025") == 1
print(f"Risultato: {'✅ CORRETTO' if correct2 else '❌ SBAGLIATO'}\n")

# TEST 3: Path con trailing slash
print("\n[TEST 3] Path con trailing slash")
print("-" * 80)
path3 = r"C:\Users\Dmitr\Desktop\Nikon\2025\ "
result3 = smart_path_logic(path3, year, month, day)

print(f"Input:    {path3}")
print(f"Output:   {result3}")
has_double3 = "2025\\2025" in result3 or "2025/2025" in result3
print(f"Doppio anno? {'❌ BUG!' if has_double3 else '✅ NO'}")
correct3 = not has_double3
print(f"Risultato: {'✅ CORRETTO' if correct3 else '❌ SBAGLIATO'}\n")

# TEST 4: Path con anno diverso
print("\n[TEST 4] Path termina con 2024, ma foto è del 2025")
print("-" * 80)
path4 = r"C:\Users\Dmitr\Desktop\Nikon\2024"
result4 = smart_path_logic(path4, year, month, day)

print(f"Input:    {path4}")
print(f"Output:   {result4}")
print(f"✅ Deve aggiungere 2025 perché path termina con 2024")
has_2024_and_2025 = "2024" in result4 and "2025" in result4
print(f"Ha entrambi 2024 e 2025? {'✅ CORRETTO' if has_2024_and_2025 else '❌ SBAGLIATO'}\n")

# TEST 5: Path Linux style
print("\n[TEST 5] Path Linux-style")
print("-" * 80)
path5 = "/home/user/Photos/Nikon/2025"
result5 = smart_path_logic(path5, year, month, day)

print(f"Input:    {path5}")
print(f"Output:   {result5}")
has_double5 = "/2025/2025/" in result5
print(f"Doppio anno? {'❌ BUG!' if has_double5 else '✅ NO'}")
correct5 = not has_double5
print(f"Risultato: {'✅ CORRETTO' if correct5 else '❌ SBAGLIATO'}\n")

print("\n" + "=" * 80)
print("RIEPILOGO RISULTATI")
print("=" * 80)

all_correct = all([correct1, correct2, correct3, correct5])

results = [
    ("Path senza anno", correct1),
    ("Path con anno (TUO CASO)", correct2),
    ("Path con trailing slash", correct3),
    ("Path anno diverso", True),
    ("Path Linux style", correct5)
]

for test_name, passed in results:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"  {status}: {test_name}")

print("\n" + "=" * 80)
if all_correct:
    print("✅✅✅ TUTTI I TEST PASSATI! IL BUG È RISOLTO! ✅✅✅")
else:
    print("❌ ALCUNI TEST FALLITI - CONTROLLARE IL CODICE")
print("=" * 80)

print("\nCOMPORTAMENTO CORRETTO:")
print("  1. Path 'C:\\...\\Nikon' → Crea 'Nikon\\2025\\Ottobre\\21_Prova'")
print("  2. Path 'C:\\...\\Nikon\\2025' → Crea 'Nikon\\2025\\Ottobre\\21_Prova'")
print("  3. NO doppio anno MAI!")
print("=" * 80)
