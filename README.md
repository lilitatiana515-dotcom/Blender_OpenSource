# 🎨 MultiExport Tools — Blender Add-on

> Add-on de código abierto para Blender que permite exportar el objeto 3D activo en múltiples formatos de manera simultánea con un solo clic.

Desarrollado por **Lilibeth Tatiana Gomez Mantilla** y **Marlon Eduardo Laiton Garcia**  
Universitaria de Colombia — Ingeniería de Software — Aplicaciones Open Source 2026

---

## ✨ Características

- Exporta en **OBJ, FBX, STL y GLTF 2.0** simultáneamente
- Panel integrado en la barra lateral del viewport 3D (tecla **N**)
- Selector de carpeta de destino personalizable
- Usa el nombre del objeto activo como nombre base de los archivos
- Crea la carpeta de destino automáticamente si no existe
- Compatible con **Blender 5.1.2**

---

## 📦 Instalación

1. Descarga el archivo `multiexport_tools.py`
2. Abre Blender y ve a **Editar → Preferencias → Complementos**
3. Haz clic en **"Instalar..."**
4. Selecciona el archivo `multiexport_tools.py`
5. Activa el complemento marcando la casilla ✅

---

## 🚀 Uso

1. Selecciona un objeto en la escena 3D
2. Presiona **N** para abrir la barra lateral
3. Ve a la pestaña **"MultiExport"**
4. Elige la carpeta de destino
5. Selecciona los formatos que deseas exportar
6. Haz clic en **"Exportar ahora"**

Los archivos se guardarán en la carpeta seleccionada con el nombre del objeto activo.

---

## 📁 Formatos soportados

| Formato | Extensión | Uso común |
|---------|-----------|-----------|
| Wavefront OBJ | `.obj` | Modelado general, intercambio universal |
| Autodesk FBX | `.fbx` | Motores de juego (Unity, Unreal) |
| STL | `.stl` | Impresión 3D |
| GLTF 2.0 | `.glb` | Web 3D, realidad aumentada |

---

## 🛠️ Requisitos

- Blender 4.0 o superior (probado en Blender 5.1.2)
- Sistema operativo: Windows, macOS o Linux

---

## 📄 Licencia

Este proyecto está distribuido bajo la licencia **GNU General Public License v2 (GPL v2)**, la misma licencia de Blender. Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras un error o tienes una sugerencia:

1. Abre un **Issue** describiendo el problema o mejora
2. Haz un **Fork** del repositorio
3. Crea una rama con tu mejora: `git checkout -b mejora/nueva-funcionalidad`
4. Envía un **Pull Request**

---

*Proyecto desarrollado como parte del Taller 003 de la asignatura Aplicaciones Open Source — Universitaria de Colombia 2026*
