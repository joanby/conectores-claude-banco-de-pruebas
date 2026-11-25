"""Validación de IBAN español."""

import re

_FORMATO_ES = re.compile(r"ES\d{22}")


def validar_iban_es(texto: str) -> bool:
    """Indica si `texto` es un IBAN español válido.

    Acepta espacios y minúsculas ("es91 2100 0418 4502 0005 1332").
    Comprueba el formato (ES + 22 dígitos) y el dígito de control ISO 7064 mod 97.
    No comprueba que el banco o la cuenta existan.
    """
    iban = "".join(texto.split()).upper()
    if not _FORMATO_ES.fullmatch(iban):
        return False
    reordenado = iban[4:] + iban[:4]
    numerico = "".join(str(int(c, 36)) for c in reordenado)
    return int(numerico) % 97 == 1
