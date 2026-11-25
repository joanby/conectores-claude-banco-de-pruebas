"""Validación de IBAN español."""

import re

_FORMATO = re.compile(r"ES[0-9]{22}")


def validar_iban_es(texto: str) -> bool:
    """Devuelve True si `texto` es un IBAN español válido.

    Acepta espacios y guiones como separadores y mayúsculas o minúsculas.
    Comprueba el formato (ES + 22 dígitos) y el dígito de control mod 97 (ISO 13616).
    No comprueba los dígitos de control nacionales del CCC.

    >>> validar_iban_es("ES91 2100 0418 4502 0005 1332")
    True
    >>> validar_iban_es("ES91 2100 0418 4502 0005 1333")
    False
    """
    iban = re.sub(r"[ -]", "", texto).upper()
    if not _FORMATO.fullmatch(iban):
        return False
    reordenado = iban[4:] + iban[:4]
    numerico = "".join(str(int(c, 36)) for c in reordenado)
    return int(numerico) % 97 == 1
