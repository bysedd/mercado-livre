import importlib
import pkgutil
import tasks


def execute_all_tasks():
    for importer, modname, is_pkg in pkgutil.iter_modules(tasks.__path__):
        if not is_pkg:
            module = importlib.import_module("." + modname, "tasks")
            task_instance = getattr(module, "Task")(use_local_uri=True)
            task_instance.run()


if __name__ == '__main__':
    execute_all_tasks()
