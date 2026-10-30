class RequisitosDocumentales:
    """Objeto que encapsula la relacion tipo de solicitud -> documentos requeridos.

    Introduce Parameter Object: en lugar de pasar listas sueltas de strings y
    armarlas con condicionales en cada metodo, la regla de negocio se expresa
    en un unico lugar.
    """

    REQUISITOS = {
        "EQUIVALENCIA": ["plan de estudio", "syllabus"],
        "CERTIFICADO": ["probante de pago"],
        "RECLAMO": [],
    }

    def __init__(self, tipo):
        self.tipo = tipo
        self.documentos = self.REQUISITOS.get(tipo, [])

    def faltantes(self, documentos_adjuntos):
        nombres_adjuntos = [d.nombre.lower() for d in documentos_adjuntos]
        return [r for r in self.documentos if r not in nombres_adjuntos]
