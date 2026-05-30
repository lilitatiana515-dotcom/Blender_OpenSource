bl_info = {
    "name": "Session Timer",
    "author": "Lilibeth Gomez & Marlon Laiton - Universitaria de Colombia",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "Vista 3D > Barra lateral (N) > Session Timer",
    "description": "Muestra cuanto tiempo llevas trabajando en la sesion actual de Blender",
    "category": "3D View",
}

import bpy
import time


# ─── VARIABLES GLOBALES ──────────────────────────────────────────────────────

_start_time = None
_is_running = False
_elapsed_acumulado = 0.0


# ─── OPERADORES ──────────────────────────────────────────────────────────────

class TIMER_OT_iniciar(bpy.types.Operator):
    bl_idname = "session_timer.iniciar"
    bl_label = "Iniciar"
    bl_description = "Inicia el temporizador de sesion"

    def execute(self, context):
        global _start_time, _is_running
        if not _is_running:
            _start_time = time.monotonic()
            _is_running = True
            context.scene.timer_props.is_running = True
            self.report({"INFO"}, "Temporizador iniciado.")
        return {"FINISHED"}


class TIMER_OT_pausar(bpy.types.Operator):
    bl_idname = "session_timer.pausar"
    bl_label = "Pausar"
    bl_description = "Pausa el temporizador de sesion"

    def execute(self, context):
        global _is_running, _elapsed_acumulado, _start_time
        if _is_running:
            _elapsed_acumulado += time.monotonic() - _start_time
            _is_running = False
            context.scene.timer_props.is_running = False
            self.report({"INFO"}, "Temporizador pausado.")
        return {"FINISHED"}


class TIMER_OT_reiniciar(bpy.types.Operator):
    bl_idname = "session_timer.reiniciar"
    bl_label = "Reiniciar"
    bl_description = "Reinicia el temporizador a cero"

    def execute(self, context):
        global _start_time, _is_running, _elapsed_acumulado
        _elapsed_acumulado = 0.0
        _start_time = time.monotonic()
        _is_running = True
        context.scene.timer_props.is_running = True
        self.report({"INFO"}, "Temporizador reiniciado.")
        return {"FINISHED"}


# ─── PROPIEDADES ─────────────────────────────────────────────────────────────

class SessionTimerProperties(bpy.types.PropertyGroup):
    is_running: bpy.props.BoolProperty(default=False)


# ─── PANEL ───────────────────────────────────────────────────────────────────

class TIMER_PT_panel(bpy.types.Panel):
    bl_label = "Session Timer"
    bl_idname = "TIMER_PT_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Session Timer"

    def draw(self, context):
        layout = self.layout
        props = context.scene.timer_props

        # Calcular tiempo transcurrido correctamente
        if _is_running and _start_time is not None:
            elapsed = _elapsed_acumulado + (time.monotonic() - _start_time)
        else:
            elapsed = _elapsed_acumulado

        # Asegurar que nunca sea negativo
        elapsed = max(0.0, elapsed)

        horas = int(elapsed // 3600)
        minutos = int((elapsed % 3600) // 60)
        segundos = int(elapsed % 60)

        # Mostrar tiempo
        box = layout.box()
        box.label(text="Tiempo de sesion:", icon="TIME")
        row = box.row()
        row.scale_y = 2.0
        row.alignment = "CENTER"
        row.label(text=f"{horas:02d} : {minutos:02d} : {segundos:02d}")

        layout.separator()

        # Estado
        box2 = layout.box()
        if props.is_running:
            box2.label(text="Estado: Activo", icon="PLAY")
        else:
            box2.label(text="Estado: Pausado", icon="PAUSE")

        layout.separator()

        # Botones
        col = layout.column(align=True)
        col.scale_y = 1.5
        if not props.is_running:
            col.operator("session_timer.iniciar", icon="PLAY")
        else:
            col.operator("session_timer.pausar", icon="PAUSE")
        col.operator("session_timer.reiniciar", icon="FILE_REFRESH")

        layout.separator()

        # Resumen
        box3 = layout.box()
        box3.label(text="Resumen:", icon="INFO")
        box3.label(text=f"Horas:    {horas}h")
        box3.label(text=f"Minutos:  {minutos}m")
        box3.label(text=f"Segundos: {segundos}s")


# ─── HANDLER PARA ACTUALIZAR EL PANEL ────────────────────────────────────────

def _update_timer(scene):
    if _is_running:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type == "VIEW_3D":
                    area.tag_redraw()


# ─── REGISTRO ────────────────────────────────────────────────────────────────

classes = [
    SessionTimerProperties,
    TIMER_OT_iniciar,
    TIMER_OT_pausar,
    TIMER_OT_reiniciar,
    TIMER_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.timer_props = bpy.props.PointerProperty(
        type=SessionTimerProperties
    )
    bpy.app.handlers.depsgraph_update_post.append(_update_timer)

def unregister():
    if _update_timer in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_update_timer)
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.timer_props

if __name__ == "__main__":
    register()
