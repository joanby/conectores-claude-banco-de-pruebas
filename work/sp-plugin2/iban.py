"""Validación de IBAN español."""

import re

_FORMATO = re.compile(r"ES[0-9]{22}")


def validar_iban_es(texto: str) -> bool:
    """Indica si `texto` es un IBAN español válido.

    Acepta espacios y minúsculas. Comprueba el formato (ES + 22 dígitos)
    y el dígito de control IBAN (módulo 97, ISO 13616).
    """
    iban = "".join(texto.split()).upper()
    if not _FORMATO.fullmatch(iban):
        return False
    reordenado = iban[4:] + iban[:4]
    numerico = "".join(str(int(c, 36)) for c in reordenado)
    return int(numerico) % 97 == 1
