class Alumno:
    def __init__(self, legajo, nombre, carrera, email):
        self.legajo = legajo
        self.nombre = nombre
        self.carrera = carrera
        self.email = email


class Documento:
    def __init__(self, nombre, tipo, obligatorio):
        self.nombre = nombre
        self.tipo = tipo
        self.obligatorio = obligatorio


class Solicitud:
    def __init__(self, id_solicitud, legajo_alumno, tipo, estado, fecha_creacion):
        self.id = id_solicitud
        self.legajo_alumno = legajo_alumno
        self.tipo = tipo
        self.estado = estado
        self.fecha_creacion = fecha_creacion
        self.documentos = []
