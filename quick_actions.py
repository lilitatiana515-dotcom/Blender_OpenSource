bl_info = {
    "name": "Quick Actions Panel",
    "author": "Lilibeth Gomez & Marlon Laiton - Universitaria de Colombia",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "Vista 3D > Barra lateral (N) > Quick Actions",
    "description": "Panel de atajos rapidos con las acciones mas usadas en Blender",
    "category": "3D View",
}

import bpy


# ─── OPERADORES PERSONALIZADOS ───────────────────────────────────────────────

class QUICK_OT_eliminar_objeto(bpy.types.Operator):
    bl_idname = "quick.eliminar_objeto"
    bl_label = "Eliminar objeto"
    bl_description = "Elimina el objeto activo de la escena"

    def execute(self, context):
        if context.active_object:
            bpy.ops.object.delete()
            self.report({"INFO"}, "Objeto eliminado.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_duplicar_objeto(bpy.types.Operator):
    bl_idname = "quick.duplicar_objeto"
    bl_label = "Duplicar objeto"
    bl_description = "Duplica el objeto activo"

    def execute(self, context):
        if context.active_object:
            bpy.ops.object.duplicate_move()
            self.report({"INFO"}, "Objeto duplicado.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_resetear_posicion(bpy.types.Operator):
    bl_idname = "quick.resetear_posicion"
    bl_label = "Resetear posicion"
    bl_description = "Lleva el objeto al centro de la escena (0, 0, 0)"

    def execute(self, context):
        obj = context.active_object
        if obj:
            obj.location = (0, 0, 0)
            self.report({"INFO"}, f"{obj.name} movido al origen.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_resetear_escala(bpy.types.Operator):
    bl_idname = "quick.resetear_escala"
    bl_label = "Resetear escala"
    bl_description = "Resetea la escala del objeto a 1"

    def execute(self, context):
        obj = context.active_object
        if obj:
            obj.scale = (1, 1, 1)
            self.report({"INFO"}, f"Escala de {obj.name} reseteada.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_resetear_rotacion(bpy.types.Operator):
    bl_idname = "quick.resetear_rotacion"
    bl_label = "Resetear rotacion"
    bl_description = "Resetea la rotacion del objeto a 0"

    def execute(self, context):
        obj = context.active_object
        if obj:
            obj.rotation_euler = (0, 0, 0)
            self.report({"INFO"}, f"Rotacion de {obj.name} reseteada.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_camara_objeto(bpy.types.Operator):
    bl_idname = "quick.camara_objeto"
    bl_label = "Enfocar objeto"
    bl_description = "Centra la camara en el objeto seleccionado"

    def execute(self, context):
        if context.active_object:
            bpy.ops.view3d.view_selected()
            self.report({"INFO"}, "Camara enfocada en el objeto.")
        else:
            self.report({"WARNING"}, "No hay objeto seleccionado.")
        return {"FINISHED"}


class QUICK_OT_agregar_cubo(bpy.types.Operator):
    bl_idname = "quick.agregar_cubo"
    bl_label = "Agregar Cubo"
    bl_description = "Agrega un cubo en el origen de la escena"

    def execute(self, context):
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        self.report({"INFO"}, "Cubo agregado.")
        return {"FINISHED"}


class QUICK_OT_agregar_esfera(bpy.types.Operator):
    bl_idname = "quick.agregar_esfera"
    bl_label = "Agregar Esfera"
    bl_description = "Agrega una esfera en el origen de la escena"

    def execute(self, context):
        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
        self.report({"INFO"}, "Esfera agregada.")
        return {"FINISHED"}


class QUICK_OT_agregar_cilindro(bpy.types.Operator):
    bl_idname = "quick.agregar_cilindro"
    bl_label = "Agregar Cilindro"
    bl_description = "Agrega un cilindro en el origen de la escena"

    def execute(self, context):
        bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
        self.report({"INFO"}, "Cilindro agregado.")
        return {"FINISHED"}


class QUICK_OT_render_rapido(bpy.types.Operator):
    bl_idname = "quick.render_rapido"
    bl_label = "Render rapido"
    bl_description = "Ejecuta un render rapido de la escena actual"

    def execute(self, context):
        bpy.ops.render.render("INVOKE_DEFAULT")
        return {"FINISHED"}


# ─── PANEL ──────────────────────────────────────────────────────────────────

class QUICK_PT_panel(bpy.types.Panel):
    bl_label = "Quick Actions"
    bl_idname = "QUICK_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Quick Actions"

    def draw(self, context):
        layout = self.layout
        obj = context.active_object

        # Info objeto activo
        box = layout.box()
        box.label(text="Objeto activo:", icon="OBJECT_DATA")
        if obj:
            box.label(text=obj.name, icon="CHECKMARK")
        else:
            box.label(text="Ninguno", icon="ERROR")

        layout.separator()

        # ── Sección: Transformaciones ──────────────────────────
        box = layout.box()
        box.label(text="Transformaciones:", icon="EMPTY_ARROWS")
        col = box.column(align=True)
        col.operator("quick.resetear_posicion", icon="TRACKING_CLEAR_FORWARDS")
        col.operator("quick.resetear_rotacion", icon="FILE_REFRESH")
        col.operator("quick.resetear_escala", icon="FULLSCREEN_EXIT")

        layout.separator()

        # ── Sección: Objeto ────────────────────────────────────
        box = layout.box()
        box.label(text="Objeto:", icon="MESH_DATA")
        col = box.column(align=True)
        col.operator("quick.duplicar_objeto", icon="DUPLICATE")
        col.operator("quick.camara_objeto", icon="ZOOM_IN")
        col.operator("quick.eliminar_objeto", icon="TRASH")

        layout.separator()

        # ── Sección: Agregar mallas ────────────────────────────
        box = layout.box()
        box.label(text="Agregar malla:", icon="ADD")
        col = box.column(align=True)
        col.operator("quick.agregar_cubo", icon="MESH_CUBE")
        col.operator("quick.agregar_esfera", icon="MESH_UVSPHERE")
        col.operator("quick.agregar_cilindro", icon="MESH_CYLINDER")

        layout.separator()

        # ── Sección: Render ────────────────────────────────────
        box = layout.box()
        box.label(text="Render:", icon="RENDER_STILL")
        row = box.row()
        row.scale_y = 1.5
        row.operator("quick.render_rapido", icon="RENDER_STILL")


# ─── REGISTRO ───────────────────────────────────────────────────────────────

classes = [
    QUICK_OT_eliminar_objeto,
    QUICK_OT_duplicar_objeto,
    QUICK_OT_resetear_posicion,
    QUICK_OT_resetear_escala,
    QUICK_OT_resetear_rotacion,
    QUICK_OT_camara_objeto,
    QUICK_OT_agregar_cubo,
    QUICK_OT_agregar_esfera,
    QUICK_OT_agregar_cilindro,
    QUICK_OT_render_rapido,
    QUICK_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
