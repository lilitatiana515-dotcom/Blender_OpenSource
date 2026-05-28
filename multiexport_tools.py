bl_info = {
    "name": "MultiExport Tools",
    "author": "Lilibeth Gomez & Marlon Laiton - Universitaria de Colombia",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "Vista 3D > Barra lateral (N) > MultiExport",
    "description": "Exporta el objeto activo en multiples formatos simultaneamente (OBJ, FBX, STL, GLTF)",
    "category": "Import-Export",
}

import bpy
import os


# ─── PROPIEDADES ────────────────────────────────────────────────────────────

class MultiExportProperties(bpy.types.PropertyGroup):
    export_obj: bpy.props.BoolProperty(
        name="OBJ",
        description="Exportar en formato OBJ",
        default=True
    )
    export_fbx: bpy.props.BoolProperty(
        name="FBX",
        description="Exportar en formato FBX",
        default=True
    )
    export_stl: bpy.props.BoolProperty(
        name="STL",
        description="Exportar en formato STL",
        default=False
    )
    export_gltf: bpy.props.BoolProperty(
        name="GLTF",
        description="Exportar en formato GLTF 2.0 (.glb)",
        default=False
    )
    export_path: bpy.props.StringProperty(
        name="Carpeta de destino",
        description="Carpeta donde se guardaran los archivos exportados",
        default="//exports/",
        subtype="DIR_PATH"
    )


# ─── OPERADOR ───────────────────────────────────────────────────────────────

class MULTIEXPORT_OT_export(bpy.types.Operator):
    bl_idname = "multiexport.export"
    bl_label = "Exportar ahora"
    bl_description = "Exporta el objeto activo en los formatos seleccionados"

    def execute(self, context):
        props = context.scene.multiexport_props
        obj = context.active_object

        # Validar que hay un objeto seleccionado
        if obj is None:
            self.report({"ERROR"}, "No hay ningun objeto seleccionado.")
            return {"CANCELLED"}

        # Resolver ruta absoluta
        export_dir = bpy.path.abspath(props.export_path)

        # Crear carpeta si no existe
        if not os.path.exists(export_dir):
            try:
                os.makedirs(export_dir)
            except Exception as e:
                self.report({"ERROR"}, f"No se pudo crear la carpeta: {e}")
                return {"CANCELLED"}

        # Nombre base = nombre del objeto activo
        base_name = bpy.path.clean_name(obj.name)
        exported = []
        errors = []

        # ── OBJ ──────────────────────────────────────────────────
        if props.export_obj:
            filepath = os.path.join(export_dir, base_name + ".obj")
            try:
                bpy.ops.wm.obj_export(
                    filepath=filepath,
                    export_selected_objects=True,
                    export_materials=True,
                )
                exported.append("OBJ")
            except Exception as e:
                errors.append(f"OBJ: {e}")

        # ── FBX ──────────────────────────────────────────────────
        if props.export_fbx:
            filepath = os.path.join(export_dir, base_name + ".fbx")
            try:
                bpy.ops.export_scene.fbx(
                    filepath=filepath,
                    use_selection=True,
                )
                exported.append("FBX")
            except Exception as e:
                errors.append(f"FBX: {e}")

        # ── STL ──────────────────────────────────────────────────
        if props.export_stl:
            filepath = os.path.join(export_dir, base_name + ".stl")
            try:
                bpy.ops.wm.stl_export(
                    filepath=filepath,
                    export_selected_objects=True,
                )
                exported.append("STL")
            except Exception as e:
                errors.append(f"STL: {e}")

        # ── GLTF ─────────────────────────────────────────────────
        if props.export_gltf:
            filepath = os.path.join(export_dir, base_name + ".glb")
            try:
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    use_selection=True,
                    export_format="GLB",
                )
                exported.append("GLTF")
            except Exception as e:
                errors.append(f"GLTF: {e}")

        # ── Resultado ─────────────────────────────────────────────
        if not exported and not errors:
            self.report({"WARNING"}, "No seleccionaste ningun formato.")
            return {"CANCELLED"}

        msg_parts = []
        if exported:
            msg_parts.append(f"Exportado: {', '.join(exported)}")
        if errors:
            msg_parts.append(f"Errores: {' | '.join(errors)}")

        self.report({"INFO"}, " — ".join(msg_parts))
        return {"FINISHED"}


# ─── PANEL ──────────────────────────────────────────────────────────────────

class MULTIEXPORT_PT_panel(bpy.types.Panel):
    bl_label = "MultiExport Tools"
    bl_idname = "MULTIEXPORT_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MultiExport"

    def draw(self, context):
        layout = self.layout
        props = context.scene.multiexport_props
        obj = context.active_object

        # Info del objeto activo
        box = layout.box()
        box.label(text="Objeto activo:", icon="OBJECT_DATA")
        if obj:
            box.label(text=obj.name, icon="CHECKMARK")
        else:
            box.label(text="Ninguno seleccionado", icon="ERROR")

        layout.separator()

        # Carpeta de destino
        layout.label(text="Carpeta de destino:", icon="FILE_FOLDER")
        layout.prop(props, "export_path", text="")

        layout.separator()

        # Formatos
        layout.label(text="Formatos a exportar:", icon="EXPORT")
        col = layout.column(align=True)
        col.prop(props, "export_obj")
        col.prop(props, "export_fbx")
        col.prop(props, "export_stl")
        col.prop(props, "export_gltf")

        layout.separator()

        # Botón de exportar
        row = layout.row()
        row.scale_y = 1.8
        row.enabled = obj is not None
        row.operator("multiexport.export", icon="EXPORT")

        if obj is None:
            layout.label(text="Selecciona un objeto primero", icon="INFO")


# ─── REGISTRO ───────────────────────────────────────────────────────────────

classes = [
    MultiExportProperties,
    MULTIEXPORT_OT_export,
    MULTIEXPORT_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.multiexport_props = bpy.props.PointerProperty(
        type=MultiExportProperties
    )

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.multiexport_props

if __name__ == "__main__":
    register()
