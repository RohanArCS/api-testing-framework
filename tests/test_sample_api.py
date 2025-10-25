"""Pytest test suite for the API testing framework.

The tests defined here are data‑driven: they iterate over a list of test cases
loaded from a YAML file under the `data/` directory.  Each test case specifies
the HTTP method, endpoint name, parameters, expected status code and (optionally)
expected response structure.  Data‑driven testing reduces duplication and
facilitates reusability【294264666156480†L350-L370】.
"""

from pathlib import Path
from typing import Dict, Any

import pytest
import yaml

from src.api_client import APIClient


def load_test_data(file_path: str) -> Any:
    """Load test definitions from a YAML file.

    Parameters
    ----------
    file_path: str
        Relative path to the YAML file containing test definitions.

    Returns
    -------
    Any
        Parsed YAML content (typically a dict containing a list of tests).
    """
    path = Path(__file__).resolve().parents[1] / file_path
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@pytest.fixture(scope="session")
def client() -> APIClient:
    """Create a single APIClient instance for the test session."""
    return APIClient()


TEST_DATA: Dict[str, Any] = load_test_data("data/test_data.yaml")


@pytest.mark.parametrize("test_case", TEST_DATA.get("tests", []))
def test_api_endpoints(client: APIClient, test_case: Dict[str, Any]) -> None:
    """Generic test that executes API calls based on test data.

    Each test case dictionary should define at least the following keys:

    - `name`: human‑readable description of the test.
    - `method`: HTTP method (get, post, put, delete).
    - `endpoint`: logical name defined in config.yaml.
    - `expected_status`: expected HTTP status code.

    Optional keys include:

    - `params`: dictionary of path parameters used to format the endpoint path.
    - `payload`: request body for POST/PUT requests.
    - `expected_keys`: list of JSON keys that must be present in the response.
    - `expected_min_length`: minimum length of a list response.
    """
    method = test_case["method"].lower()
    endpoint_name = test_case["endpoint"]
    path_params = test_case.get("params", {}) or {}
    payload = test_case.get("payload")
    expected_status = test_case["expected_status"]

    # Dispatch request based on method
    if method == "get":
        response = client.get(endpoint_name, **path_params)
    elif method == "post":
        response = client.post(endpoint_name, payload=payload, **path_params)
    elif method == "put":
        response = client.put(endpoint_name, payload=payload, **path_params)
    elif method == "delete":
        response = client.delete(endpoint_name, **path_params)
    else:
        pytest.skip(f"Unsupported HTTP method: {method}")

    assert response.status_code == expected_status, (
        f"{test_case['name']} expected status {expected_status} but got {response.status_code}"
    )

    # Validate JSON keys if provided
    if "expected_keys" in test_case and response.headers.get("Content-Type", "").startswith("application/json"):
        try:
            data = response.json()
        except Exception:
            pytest.fail(f"{test_case['name']} failed to parse JSON response")
        for key in test_case["expected_keys"]:
            assert key in data, f"{test_case['name']} missing key '{key}' in response"

    # Validate list length if provided
    if "expected_min_length" in test_case and response.headers.get("Content-Type", "").startswith("application/json"):
        try:
            data = response.json()
        except Exception:
            pytest.fail(f"{test_case['name']} failed to parse JSON response")
        assert isinstance(data, list), f"{test_case['name']} expected list response"
        assert len(data) >= test_case["expected_min_length"], (
            f"{test_case['name']} expected at least {test_case['expected_min_length']} items"
        )