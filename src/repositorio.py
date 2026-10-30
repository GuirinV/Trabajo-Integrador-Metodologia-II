import json
import os

from modelos import Alumno, Documento, Solicitud

ARCHIVO_DATOS = "datos/datos.json"


class RepositorioSolicitudes:

    def __init__(self, archivo=ARCHIVO_DATOS):
        self.archivo = archivo

    def guardar(self, alumnos, solicitudes):
        datos = {"alumnos": [], "solicitudes": []}
        for a in alumnos:
            datos["alumnos"].append(
                {
                    "legajo": a.legajo,
                    "nombre": a.nombre,
                    "carrera": a.carrera,
                    "email": a.email,
                }
            )
        for s in solicitudes:
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
        f = open(self.archivo, "w")
        f.write(json.dumps(datos, indent=2))
        f.close()

    def cargar(self):
        alumnos = []
        solicitudes = []
        if not os.path.exists(self.archivo):
            return alumnos, solicitudes
        f = open(self.archivo, "r")
        contenido = f.read()
        f.close()
        datos = json.loads(contenido)
        for a in datos["alumnos"]:
            alumnos.append(Alumno(a["legajo"], a["nombre"], a["carrera"], a["email"]))
        for s in datos["solicitudes"]:
            solicitud = Solicitud(s["id"], s["legajo"], s["tipo"], s["estado"], s["fecha"])
            for d in s["documentos"]:
                solicitud.documentos.append(Documento(d["nombre"], d["tipo"], d["obligatorio"]))
            solicitudes.append(solicitud)
        return alumnos, solicitudes
