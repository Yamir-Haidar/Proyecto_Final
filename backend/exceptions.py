class UnreliableGraph(Exception):
    def __init__(self):
        self.message = "El archivo de texto que esta tratando de importar no es confiable\nAsegurese que el archivo " \
                       "fue exportado previamente por la app"

    def get_message(self) -> str:
        return self.message


class Exc(Exception):
    def __init__(self, message: str, var: list):
        super().__init__(message)
        self.errores = var
