"""API client abstraction for sending HTTP requests.

The `APIClient` encapsulates common HTTP methods (GET, POST, PUT, DELETE)
and utilises the `Config` class to build full URLs from logical names.  It logs
all outgoing requests and incoming responses, making it easier to trace API
interactions during debugging【294264666156480†L290-L299】.
"""

from typing import Any, Dict, Optional

import requests
from requests.exceptions import RequestException

from .utils.config import Config
from .utils.logger import setup_logger


class APIClient:
    """Reusable API client for making HTTP requests."""

    def __init__(self, config: Optional[Config] = None, log_file: str = "logs/test.log") -> None:
        self.config = config if config is not None else Config()
        # Set up logger; each client has its own logger
        self.logger = setup_logger(name="APIClient", log_file=log_file)

    def request(self, method: str, endpoint_name: str,
                params: Optional[Dict[str, Any]] = None,
                payload: Optional[Dict[str, Any]] = None,
                headers: Optional[Dict[str, str]] = None,
                **path_params: Any) -> requests.Response:
        """Send an HTTP request using the given method.

        Parameters
        ----------
        method: str
            HTTP method (e.g. "GET", "POST").
        endpoint_name: str
            Name of the endpoint defined in configuration.
        params: dict, optional
            Query string parameters.
        payload: dict, optional
            JSON body for POST/PUT requests.
        headers: dict, optional
            Custom headers to send.
        path_params: Any
            Parameters substituted into the endpoint path.

        Returns
        -------
        requests.Response
            Raw response object from the `requests` library.
        """
        url = self.config.get_endpoint(endpoint_name, **path_params)
        self.logger.info(f"Sending {method.upper()} request to {url}")
        if params:
            self.logger.debug(f"Query params: {params}")
        if payload:
            self.logger.debug(f"Payload: {payload}")

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                params=params,
                json=payload,
                headers=headers,
                timeout=10,
            )
            self.logger.info(f"Received response with status {response.status_code}")
            return response
        except RequestException as exc:
            self.logger.error(f"HTTP request failed: {exc}")
            raise

    def get(self, endpoint_name: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **path_params: Any) -> requests.Response:
        return self.request("GET", endpoint_name, params=params, headers=headers, **path_params)

    def post(self, endpoint_name: str,
             payload: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None,
             **path_params: Any) -> requests.Response:
        return self.request("POST", endpoint_name, payload=payload, headers=headers, **path_params)

    def put(self, endpoint_name: str,
            payload: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None,
            **path_params: Any) -> requests.Response:
        return self.request("PUT", endpoint_name, payload=payload, headers=headers, **path_params)

    def delete(self, endpoint_name: str,
               headers: Optional[Dict[str, str]] = None,
               **path_params: Any) -> requests.Response:
        return self.request("DELETE", endpoint_name, headers=headers, **path_params)