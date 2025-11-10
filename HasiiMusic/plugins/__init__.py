import glob
from os.path import dirname, isfile, join

def __list_all_modules():
    work_dir = dirname(__file__)
    py_files = glob.glob(join(work_dir, "**", "*.py"), recursive=True)

    all_modules = [
        f.replace(work_dir + "/", "").replace("/", ".")[:-3]
        for f in py_files
        if isfile(f) and not f.endswith("__init__.py")
    ]
    return all_modules

ALL_MODULES = sorted(__list_all_modules())
__all__ = ALL_MODULES + ["ALL_MODULES"]
