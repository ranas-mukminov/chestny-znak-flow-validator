from pathlib import Path

PACKAGE_ROOT = Path(__file__).parent
EXAMPLES_DIR = PACKAGE_ROOT.parent / "examples"
DEFAULT_MAPPING_PROFILE = EXAMPLES_DIR / "configs" / "validation_profile_example.yaml"
