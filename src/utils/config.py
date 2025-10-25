"""Configuration loader for the API testing framework.

This module reads the YAML configuration file and exposes attributes for the
selected environment and endpoints.  Centralizing configuration allows tests
to run against multiple environments without changing test code, improving
flexibility and maintainability【294264666156480†L120-L139】.
"""

import os
from pathlib import Path
from typing import Dict, Any

import yaml


class Config:
    """Load configuration from a YAML file.

    Attributes
    ----------
    base_url: str
        Base URL of the API for the selected environment.
    endpoints: Dict[str, str]
        Mapping of endpoint names to URL paths.
    env: str
        Name of the selected environment.
    """

    def __init__(self, config_path: str = "config.yaml") -> None:
        path = Path(config_path)
        if not path.is_file():
            # Attempt to find the file relative to project root
            candidate = Path(__file__).resolve().parents[2] / "config.yaml"
            path = candidate
        with open(path, "r", encoding="utf-8") as f:
            raw_config: Dict[str, Any] = yaml.safe_load(f)

        self.env: str = os.environ.get("ENVIRONMENT", raw_config.get("default_environment", "dev"))
        environments: Dict[str, Dict[str, Any]] = raw_config.get("environments", {})
        if self.env not in environments:
            raise ValueError(f"Environment '{self.env}' not defined in configuration")

        self.base_url: str = environments[self.env]["base_url"]
        self.endpoints: Dict[str, str] = raw_config.get("endpoints", {})

    def get_endpoint(self, name: str, **params: Any) -> str:
        """Resolve an endpoint by name and substitute path parameters.

        Parameters
        ----------
        name: str
            Logical name of the endpoint defined in `config.yaml`.
        params: Any
            Path parameters to substitute (e.g. id=1).

        Returns
        -------
        str
            Fully qualified URL including the base URL and substituted path.
        """
        if name not in self.endpoints:
            raise KeyError(f"Endpoint '{name}' not found in configuration")
        path = self.endpoints[name]
        try:
            path = path.format(**params)
        except KeyError as exc:
            raise KeyError(f"Missing parameter {exc} for endpoint '{name}'")
        return self.base_url.rstrip("/") + path