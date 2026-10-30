import json
import os
from datetime import datetime

from modelos import Alumno, Documento, Solicitud

ARCHIVO_DATOS = "datos/datos.json"


class ServicioSolicitudes:

    def __init__(self):
        self.alumnos = []
        self.solicitudes = []
        self.cargar_datos()

    def buscar_solicitud(self, id_solicitud):
        for s in self.solicitudes:
            if s.id == id_solicitud:
                return s
        return None

    # ---------------------------------------------------------------
    # ALTA DE ALUMNO
    # ---------------------------------------------------------------
    def alta_alumno(self, legajo, nombre, carrera, email):
        a = Alumno(legajo, nombre, carrera, email)
        self.alumnos.append(a)
        self.guardar_datos()
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
            "PENDIENTE",
            datetime.now().strftime("%d/%m/%Y"),
        )
        self.solicitudes.append(solicitud)
        self.guardar_datos()
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
        if solicitud.estado == "APROBADA" or solicitud.estado == "RECHAZADA":
            print("Error: la solicitud ya fue resuelta, no se pueden adjuntar documentos")
            return None
        doc = Documento(nombre, tipo, obligatorio)
        solicitud.documentos.append(doc)
        self.guardar_datos()
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
        if solicitud.estado == "PENDIENTE" and nuevo_estado == "EN_REVISION":
            puede = True
        elif solicitud.estado == "EN_REVISION" and (
            nuevo_estado == "APROBADA" or nuevo_estado == "RECHAZADA"
        ):
            puede = True
        elif solicitud.estado == "PENDIENTE" and (
            nuevo_estado == "APROBADA" or nuevo_estado == "RECHAZADA"
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
        self.guardar_datos()
        print("Solicitud " + str(id_solicitud) + " ahora esta en estado " + nuevo_estado)
        return True

    # ---------------------------------------------------------------
    # APROBAR  (valida documentos obligatorios)
    # ---------------------------------------------------------------
    def aprobar(self, id_solicitud):
        solicitud_encontrada = self.buscar_solicitud(id_solicitud)
        if solicitud_encontrada is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return -1
        if solicitud_encontrada.estado == "APROBADA" or solicitud_encontrada.estado == "RECHAZADA":
            print("Error: la solicitud ya fue resuelta")
            return -2

        requeridos = []
        if solicitud_encontrada.tipo == "EQUIVALENCIA":
            requeridos = ["plan de estudio", "syllabus"]
        elif solicitud_encontrada.tipo == "CERTIFICADO":
            requeridos = ["probante de pago"]
        else:
            requeridos = []

        nombres_adjuntos = []
        for d in solicitud_encontrada.documentos:
            nombres_adjuntos.append(d.nombre.lower())

        faltantes = []
        for r in requeridos:
            if not (r in nombres_adjuntos):
                faltantes.append(r)

        if len(faltantes) > 0:
            print("No se puede aprobar. Faltan documentos: " + str(faltantes))
            solicitud_encontrada.estado = "EN_REVISION"
            self.guardar_datos()
            return 0

        solicitud_encontrada.estado = "APROBADA"
        self.guardar_datos()
        print("Solicitud " + str(id_solicitud) + " APROBADA con exito")
        return 1

    # ---------------------------------------------------------------
    # RECHAZAR
    # ---------------------------------------------------------------
    def rechazar(self, id_solicitud, motivo):
        solicitud_encontrada = self.buscar_solicitud(id_solicitud)
        if solicitud_encontrada is None:
            print("Error: solicitud " + str(id_solicitud) + " no encontrada")
            return -1
        if solicitud_encontrada.estado == "APROBADA" or solicitud_encontrada.estado == "RECHAZADA":
            print("Error: la solicitud ya fue resuelta")
            return -2

        solicitud_encontrada.estado = "RECHAZADA"
        solicitud_encontrada.motivo = motivo
        self.guardar_datos()
        print("Solicitud " + str(id_solicitud) + " RECHAZADA. Motivo: " + motivo)
        return 1

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

    # ---------------------------------------------------------------
    # PERSISTENCIA (guarda y carga JSON)
    # ---------------------------------------------------------------
    def guardar_datos(self):
        datos = {"alumnos": [], "solicitudes": []}
        for a in self.alumnos:
            datos["alumnos"].append(
                {
                    "legajo": a.legajo,
                    "nombre": a.nombre,
                    "carrera": a.carrera,
                    "email": a.email,
                }
            )
        for s in self.solicitudes:
            docs = []
            for d in s.documentos:
                docs.append({"nombre": d.nombre, "tipo": d.tipo, "obligatorio": d.obligatorio})
            datos["solicitudes"].append(
                {
                    "id": s.id,
                    "legajo": s.legajo_alumno,
                    "tipo": s.tipo,
                    "estado": s.estado,
                    "fecha": s.fecha_creacion,
                    "documentos": docs,
                }
            )
        if not os.path.exists("datos"):
            os.makedirs("datos")
        f = open(ARCHIVO_DATOS, "w")
        f.write(json.dumps(datos, indent=2))
        f.close()

    def cargar_datos(self):
        if not os.path.exists(ARCHIVO_DATOS):
            return
        f = open(ARCHIVO_DATOS, "r")
        contenido = f.read()
        f.close()
        datos = json.loads(contenido)
        for a in datos["alumnos"]:
            self.alumnos.append(Alumno(a["legajo"], a["nombre"], a["carrera"], a["email"]))
        for s in datos["solicitudes"]:
            solicitud = Solicitud(s["id"], s["legajo"], s["tipo"], s["estado"], s["fecha"])
            for d in s["documentos"]:
                solicitud.documentos.append(Documento(d["nombre"], d["tipo"], d["obligatorio"]))
            self.solicitudes.append(solicitud)
