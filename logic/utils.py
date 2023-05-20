import re


def is_right(string, call):
    """
    Función que valida si un string sigue el patrón especificado.
    :param call: Lugar desde donde se llama para determinar el patron
    :param string: String a validar.
    :return: True si el string sigue el patrón, False en caso contrario.
    """
    # Compilar el patrón en una expresión regular
    patron = r'^[a-zA-Z0-9]+\s(\([a-zA-Z0-9]+-[a-zA-Z0-9]+\))*$' if call == 1 else r'^[a-zA-Z0-9]+$'
    regex = re.compile(patron)

    # Verificar si el string sigue el patrón
    if regex.fullmatch(string):
        return True
    else:
        return False
