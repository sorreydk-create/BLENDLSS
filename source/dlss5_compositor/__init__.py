bl_info = {
    "name": "BlenDLSS5 - DLSS 5 Compositor Node",
    "author": "LGCY Creative Studios",
    "version": (2, 6, 1),
    "blender": (4, 2, 0),
    "location": "Compositor > Add > Filter > DLSS 5",
    "description": "NVIDIA DLSS 5 neural rendering as a compositor node, live in the viewport and on renders",
    "category": "Compositing",
}

import bpy
from bpy.app.handlers import persistent
from . import prefs, node, ui, render, viewport, engine  # Добавили импорт engine сразу

_modules = (prefs, node, ui, render, viewport)

# Функция, которая сработает автоматически СРАЗУ ПОСЛЕ открытия/создания нового файла
@persistent
def reload_dlss_on_file_load(dummy):
    print("[BlenDLSS5] Обнаружена смена файла. Перезапуск графического контекста...")
    try:
        # 1. Принудительно глушим зависший поток/контекст DLSS
        engine.shutdown() 
    except Exception as e:
        print(f"[BlenDLSS5] Ошибка при остановке: {e}")
        
    try:
        # 2. Перерегистрируем модуль вьюпорта, чтобы он заново зацепил новое окно
        viewport.unregister()
        viewport.register()
        print("[BlenDLSS5] Нейросетевой движок успешно перезапущен в новом файле!")
    except Exception as e:
        print(f"[BlenDLSS5] Ошибка при перезапуске вьюпорта: {e}")

def register():
    for m in _modules:
        m.register()
    
    # Регистрируем наш автоматический перезапуск сцены
    if reload_dlss_on_file_load not in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.append(reload_dlss_on_file_load)


def unregister():
    # Удаляем обработчик при отключении плагина
    if reload_dlss_on_file_load in bpy.app.handlers.load_post:
        bpy.app.handlers.load_post.remove(reload_dlss_on_file_load)
        
    engine.shutdown()
    for m in reversed(_modules):
        m.unregister()
