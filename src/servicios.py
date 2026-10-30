from datetime import datetime

from modelos import Alumno, Documento, Solicitud
from repositorio import RepositorioSolicitudes
from requisitos import RequisitosDocumentales
from constantes import (
    ESTADO_PENDIENTE,
    ESTADO_EN_REVISION,
    ESTADO_APROBADA,
    ESTADO_RECHAZADA,
    RESULTADO_NO_ENCONTRADA,
    RESULTADO_YA_RESUELTA,
    RESULTADO_FALTAN_DOCUMENTOS,
    RESULTADO_EXITO,
)


class ServicioSolicitudes:

    def __init__(self, repositorio=None):
        self.alumnos = []
        self.solicitudes = []
        if repositorio is None:
            repositorio = RepositorioSolicitudes()
        self.repositorio = repositorio
        self.alumnos, self.solicitudes = self.repositorio.cargar()

    def buscar_solicitud(self, id_solicitud):
        for s in self.solicitudes:
            if s.id == id_solicitud:
                return s
        return None

    def guardar(self):
        self.repositorio.guardar(self.alumnos, self.solicitudes)

    # ---------------------------------------------------------------
    # ALTA DE ALUMNO
    # ---------------------------------------------------------------
    def alta_alumno(self, legajo, nombre, carrera, email):
        a = Alumno(legajo, nombre, carrera, email)
        self.alumnos.append(a)
        self.guardar()
        print("Alumno dado de alta: " + nombre + " (legajo " + str(legajo) + ")")
        return a

    # ---------------------------------------------------------------
    # CREAR SOLICITUD
    # ---------------------------------------------------------------
    def crear_solicitud(self, legajo, tipo):
        alumno_encontrado = None
        for a in self.alumnos:
            if a.legajo == legajo:
                alumno_encontrado = a
        if alumno_encontrado is None:
            print("Error: el legajo " + str(legajo) + " no existe")
            return None

        if tipo != "EQUIVALENCIA" and tipo != "CERTIFICADO" and tipo != "RECLAMO":
            print("Error: tipo de solicitud invalido")
            return None

        nuevo_id = len(self.solicitudes) + 1
        solicitud = Solicitud(
            nuevo_id,
            legajo,
            tipo,
            ESTADO_PENDIENTE,
            datetime.now().strftime("%d/%m/%Y"),
        )
        self.solicitudes.append(solicitud)
        self.guardar()
        print(
            "Solicitud "
            + str(nuevo_id)
            + " creada para "
            + alumno_encontrado.nombre
            + " el "
            + solicitud.fecha_creacion
        )
        return solicitud

    # ---------------------------------------------------------------
    # ADJUNTAR DOCUMENTO
    # ---------------------------------------------------------------
    def adjuntar_documento(self, id_solicitud, nombre, tipo, obligatorio):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return None
        if solicitud.estado == ESTADO_APROBADA or solicitud.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta, no se pueden adjuntar documentos")
            return None
        doc = Documento(nombre, tipo, obligatorio)
        solicitud.documentos.append(doc)
        self.guardar()
        print("Documento '" + nombre + "' adjuntado a la solicitud " + str(id_solicitud))
        return doc

    # ---------------------------------------------------------------
    # CAMBIAR ESTADO
    # ---------------------------------------------------------------
    def cambiar_estado(self, id_solicitud, nuevo_estado):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return False

        puede = False
        if solicitud.estado == ESTADO_PENDIENTE and nuevo_estado == ESTADO_EN_REVISION:
            puede = True
        elif solicitud.estado == ESTADO_EN_REVISION and (
            nuevo_estado == ESTADO_APROBADA or nuevo_estado == ESTADO_RECHAZADA
        ):
            puede = True
        elif solicitud.estado == ESTADO_PENDIENTE and (
            nuevo_estado == ESTADO_APROBADA or nuevo_estado == ESTADO_RECHAZADA
        ):
            puede = True

        if not puede:
            print(
                "Transicion invalida: "
                + solicitud.estado
                + " -> "
                + nuevo_estado
            )
            return False

        solicitud.estado = nuevo_estado
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " ahora esta en estado " + nuevo_estado)
        return True

    # ---------------------------------------------------------------
    # APROBAR  (valida documentos obligatorios)
    # ---------------------------------------------------------------
    def aprobar(self, id_solicitud):
        solicitud_encontrada = self.buscar_solicitud(id_solicitud)
        if solicitud_encontrada is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return RESULTADO_NO_ENCONTRADA
        if solicitud_encontrada.estado == ESTADO_APROBADA or solicitud_encontrada.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta")
            return RESULTADO_YA_RESUELTA

        requisitos = RequisitosDocumentales(solicitud_encontrada.tipo)
        faltantes = requisitos.faltantes(solicitud_encontrada.documentos)

        if len(faltantes) > 0:
            print("No se puede aprobar. Faltan documentos: " + str(faltantes))
            solicitud_encontrada.estado = ESTADO_EN_REVISION
            self.guardar()
            return RESULTADO_FALTAN_DOCUMENTOS

        solicitud_encontrada.estado = ESTADO_APROBADA
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " APROBADA con exito")
        return RESULTADO_EXITO

    # ---------------------------------------------------------------
    # RECHAZAR
    # ---------------------------------------------------------------
    def rechazar(self, id_solicitud, motivo):
        solicitud_encontrada = self.buscar_solicitud(id_solicitud)
        if solicitud_encontrada is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return RESULTADO_NO_ENCONTRADA
        if solicitud_encontrada.estado == ESTADO_APROBADA or solicitud_encontrada.estado == ESTADO_RECHAZADA:
            print("Error: la solicitud ya fue resuelta")
            return RESULTADO_YA_RESUELTA

        solicitud_encontrada.estado = ESTADO_RECHAZADA
        solicitud_encontrada.motivo = motivo
        self.guardar()
        print("Solicitud " + str(id_solicitud) + " RECHAZADA. Motivo: " + motivo)
        return RESULTADO_EXITO

    # ---------------------------------------------------------------
    # LISTAR SOLICITDES DE UN ALUMNO
    # ---------------------------------------------------------------
    def listar_solicitudes_de_alumno(self, legajo):
        resultado = []
        for s in self.solicitudes:
            if s.legajo_alumno == legajo:
                resultado.append(s)
        if len(resultado) == 0:
            print("El legajo " + str(legajo) + " no tiene solicitudes")
        else:
            print("Solicitudes del legajo " + str(legajo) + ":")
            for s in resultado:
                print(
                    "  #"
                    + str(s.id)
                    + " "
                    + s.tipo
                    + " "
                    + s.estado
                    + " ("
                    + str(len(s.documentos))
                    + " documentos)"
                )
        return resultado

    # ---------------------------------------------------------------
    # VER DETALLE
    # ---------------------------------------------------------------
    def ver_detalle(self, id_solicitud):
        solicitud = self.buscar_solicitud(id_solicitud)
        if solicitud is None:
            print("Error: la solicitud " + str(id_solicitud) + " no existe")
            return None
        print("Detalle de la solicitud #" + str(solicitud.id))
        print("  Tipo: " + solicitud.tipo)
        print("  Estado: " + solicitud.estado)
        print("  Fecha: " + solicitud.fecha_creacion)
        print("  Legajo del alumno: " + str(solicitud.legajo_alumno))
        print("  Documentos:")
        for d in solicitud.documentos:
            if d.obligatorio:
                obs = "obligatorio"
            else:
                obs = "opcional"
            print("    - " + d.nombre + " (" + d.tipo + ", " + obs + ")")
        if hasattr(solicitud, "motivo"):
            print("  Motivo de rechazo: " + solicitud.motivo)
        return solicitud
