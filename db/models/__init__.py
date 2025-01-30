import pkgutil
import importlib
from pathlib import Path

MODEL_PREFIX = 'db.models.'

def get_model_list():
    package_dir = Path(__file__).resolve().parent

    return pkgutil.walk_packages(
        path = [str(package_dir)], 
        prefix = MODEL_PREFIX, 
    )

def load_all_models():
    """Loads all models from the db/models folder"""
    modules = get_model_list()
    
    for module in modules:
        importlib.import_module(module.name)


load_all_models()