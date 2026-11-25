"""Tests ocultos para validar_iban_es: los agentes no los ven. Uso: uv run python tests_ocultos_iban.py <carpeta>."""
import importlib.util, sys

def iban_es(ccc):
    """Construye un IBAN español con dígitos de control IBAN correctos a partir de un CCC de 20 cifras."""
    n = int(ccc + "142800")
    return f"ES{98 - n % 97:02d}{ccc}"

def dc(digits, w=(1, 2, 4, 8, 5, 10, 9, 7, 3, 6)):
    r = 11 - sum(int(d) * p for d, p in zip(digits, w)) % 11
    return {10: 1, 11: 0}.get(r, r)

ok_ccc = "21000418450200051332"
d1 = dc("00" + ok_ccc[:8]); d2 = dc(ok_ccc[10:])
assert ok_ccc[8:10] == f"{d1}{d2}"
mal_dc = ok_ccc[:8] + "99" + ok_ccc[10:]

CASOS = [
    ("ES9121000418450200051332", True, "válido"),
    ("ES91 2100 0418 4502 0005 1332", True, "con espacios"),
    ("es9121000418450200051332", True, "minúsculas"),
    ("ES9121000418450200051333", False, "checksum IBAN mal"),
    ("ES912100041845020005133", False, "longitud corta"),
    ("DE89370400440532013000", False, "IBAN alemán válido"),
    ("", False, "vacío"),
    ("ES91210004184502000513AB", False, "letras en la cuenta"),
    (iban_es(mal_dc), False, "IBAN cuadra pero el DC del CCC no"),
    ("  ES9121000418450200051332  ", True, "espacios alrededor"),
]

carpeta = sys.argv[1]
spec = importlib.util.spec_from_file_location("iban", f"{carpeta}/iban.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ok = 0
for txt, esperado, nombre in CASOS:
    try:
        r = bool(m.validar_iban_es(txt))
    except Exception as e:
        r = f"EXC {type(e).__name__}"
    bien = r == esperado; ok += bien
    print(("OK  " if bien else "MAL ") + nombre, r)
print(f"{ok}/{len(CASOS)}")
