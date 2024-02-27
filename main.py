import importlib
import pkgutil

import tasks


def execute_all_tasks():
    """
    Executes all task modules found in the tasks directory.

    This function iterates over every module found within the tasks directory, excluding
    packages. For each module, it dynamically imports the module and assumes the existence
    of a Task class which it instantiates with `use_local_uri=True`. The run method of the
    Task class instance is then invoked.

    This function can be useful in a system where tasks are defined as separate modules within
    a tasks directory, and there is a need to execute all tasks in a consistent manner.

    Note:
        Each module in the tasks directory should contain a Task class having
        a method 'run' which encapsulates the task's logic.

    Example:
        tasks
        ├── task1.py
        ├── task2.py
    """
    for importer, modname, is_pkg in pkgutil.iter_modules(tasks.__path__):
        if not is_pkg:
            try:
                module = importlib.import_module("." + modname, "tasks")
                task_instance = getattr(module, "Task")(use_local_uri=True)
                task_instance.run()
            except ImportError:
                raise ImportError(f"Could not import module '{modname}'")
            except AttributeError:
                raise AttributeError(f"Module '{modname}' does not contain a Task class")


if __name__ == '__main__':
    execute_all_tasks()
