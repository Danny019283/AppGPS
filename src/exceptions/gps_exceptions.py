class GPSError(Exception):
    """Base exception para errores del GPS"""
    pass

class EmptyFieldError(GPSError):
    def __init__(self, field_name):
        super().__init__(f"El campo '{field_name}' no puede estar vacío")

class AddressNotFoundError(GPSError):
    def __init__(self, address):
        super().__init__(f"No se pudo encontrar la dirección: {address}")

class PointOutsideAreaError(GPSError):
    def __init__(self, point_name, area):
        super().__init__(f"El {point_name} está fuera del área: {area}")

class AreaNotLoadedError(GPSError):
    def __init__(self):
        super().__init__("Primero debes cargar un área")

class RouteCalculationError(GPSError):
    def __init__(self, details):
        super().__init__(f"Error calculando la ruta: {details}")