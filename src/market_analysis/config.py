"""Load versioned configuration artifacts without applying production schemas."""

from json import load as load_json
from pathlib import Path
from typing import cast

import yaml

type ConfigValue = object
type ConfigMapping = dict[str, ConfigValue]


def load_yaml_mapping(path: Path) -> ConfigMapping:
    """Load a YAML document whose root must be a mapping."""
    with path.open(encoding="utf-8") as stream:
        document = yaml.safe_load(stream)

    if not isinstance(document, dict) or not all(
        isinstance(key, str) for key in document
    ):
        raise ValueError(f"expected a string-keyed mapping in {path}")
    return cast("ConfigMapping", document)


def load_json_mapping(path: Path) -> ConfigMapping:
    """Load a JSON document whose root must be a mapping."""
    with path.open(encoding="utf-8") as stream:
        document = load_json(stream)

    if not isinstance(document, dict) or not all(
        isinstance(key, str) for key in document
    ):
        raise ValueError(f"expected a string-keyed mapping in {path}")
    return cast("ConfigMapping", document)
