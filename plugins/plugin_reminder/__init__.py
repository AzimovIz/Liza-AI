from core import Core, F

core = Core()
from .base import Notice



async def start(core: Core):
    manifest = {
        "name": "Плагин заметок",
        "version": "1.0",
        "require_online": False,

        "default_options": {},
    }
    return manifest


async def start_with_options(core: Core, manifest: dict):
    print("reminder!!!!!!!!!!!!!!!!!!!!!!")
