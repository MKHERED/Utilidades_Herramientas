import importlib
import os
import threading
import time
import traceback
import customtkinter as ctk
from queue import Queue
from types import ModuleType

class CTkAppRunner:
    def __init__(self, module, stop_event):
        self.module = module
        self.stop_event = stop_event
        self.command_queue = Queue()
        self.app_instance = None

    def run_app(self):
        """Ejecuta la aplicación CustomTkinter"""
        try:
            ComparadorApp = getattr(self.module, "ComparadorApp")
            self.app_instance = ComparadorApp()
            
            # Bucle principal modificado para CustomTkinter
            while not self.stop_event.is_set():
                self.app_instance.update()
                time.sleep(0.05)
                
                # Procesar comandos en cola
                try:
                    while True:
                        cmd = self.command_queue.get_nowait()
                        cmd()
                except:
                    pass
            
            # Cierre limpio
            if hasattr(self.app_instance, 'destroy'):
                self.app_instance.destroy()
            elif hasattr(self.app_instance, 'quit'):
                self.app_instance.quit()
        except Exception as e:
            print("Error en la aplicación CustomTkinter:")
            traceback.print_exc()
            if self.app_instance and hasattr(self.app_instance, 'destroy'):
                self.app_instance.destroy()

class HotReloader:
    def __init__(self, module_name: str, file_path: str):
        self.module_name = module_name
        self.file_path = file_path
        self.last_mtime = None
        self.app_thread = None
        self.stop_event = threading.Event()
        self.current_module = None
        self.app_runner = None
        
    def load_module(self) -> ModuleType:
        """Carga o recarga el módulo especificado"""
        try:
            if self.module_name in globals():
                module = importlib.reload(globals()[self.module_name])
            else:
                module = importlib.import_module(self.module_name)
                globals()[self.module_name] = module
            
            self.current_module = module
            return module
        except Exception as e:
            print(f"Error al cargar el módulo {self.module_name}:")
            traceback.print_exc()
            raise

    def start(self):
        """Inicia el bucle principal de monitoreo"""
        print(f"Monitoreando {self.file_path} para cambios...")
        try:
            while True:
                try:
                    mtime = os.path.getmtime(self.file_path)
                    
                    if self.last_mtime is None or mtime != self.last_mtime:
                        print("\nDetectados cambios en el archivo. Recargando...")
                        self.last_mtime = mtime
                        
                        # Detener la ejecución actual si existe
                        if self.app_thread and self.app_thread.is_alive():
                            self.stop_event.set()
                            self.app_thread.join(timeout=2.0)
                            if self.app_thread.is_alive():
                                print("Advertencia: El hilo anterior no terminó correctamente")
                            self.stop_event.clear()
                        
                        # Recargar el módulo
                        self.load_module()
                        
                        # Iniciar nueva instancia
                        self.app_runner = CTkAppRunner(self.current_module, self.stop_event)
                        self.app_thread = threading.Thread(
                            target=self.app_runner.run_app,
                            daemon=True
                        )
                        self.app_thread.start()
                        print("Aplicación recargada correctamente")
                    
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("\nDeteniendo el monitor...")
                    raise
                except Exception as e:
                    print(f"Error durante el monitoreo: {e}")
                    traceback.print_exc()
                    time.sleep(2)
        finally:
            # Limpieza final
            if self.app_thread and self.app_thread.is_alive():
                self.stop_event.set()
                self.app_thread.join()

if __name__ == "__main__":
    # Configuración inicial de CustomTkinter
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    reloader = HotReloader(
        module_name="interface",  # Cambia esto si tu archivo tiene otro nombre
        file_path="interface.py"  # Asegúrate que coincide con tu nombre de archivo
    )
    reloader.start()