import os

os.environ["ENVIRONMENT"] = "testing"

from config import config as project_config

if not project_config.is_testing():
    err = f"Invalid testing environment: {project_config}"
