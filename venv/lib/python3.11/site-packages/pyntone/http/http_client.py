from typing import Any

import requests

from pyntone.kintone_request_config_builder import (
    HttpMethod,
    KintoneRequestConfigBuilder,
    KintoneRequestFormData,
    KintoneRequestParams,
)


class KintoneError(Exception):
    def __init__(self, message, text, json, status_code) -> None:
        self.text = text
        self.json = json
        self.status_code = status_code
        super().__init__(message)


class HttpClent:
    def __init__(self, config_builder: KintoneRequestConfigBuilder) -> None:
        self.config_builder = config_builder

    def get(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.GET, path, params)
        return self._send_request(config).json()

    def get_data(self, path: str, params: KintoneRequestParams) -> bytes:
        config = self.config_builder.build(HttpMethod.GET, path, params)
        return self._send_request(config).content

    def post(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.POST, path, params)
        return self._send_request(config).json()

    def post_data(self, path: str, form_data: KintoneRequestFormData) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.POST, path, form_data)
        return self._send_request(config).json()

    def put(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.PUT, path, params)
        return self._send_request(config).json()

    def delete(self, path: str, params: KintoneRequestParams) -> dict[str, Any]:
        config = self.config_builder.build(HttpMethod.DELETE, path, params)
        return self._send_request(config).json()

    def _send_request(self, config: dict[str, Any]):
        r = requests.request(**config)
        self._is_success(r)
        return r

    def _is_success(self, response: requests.Response) -> None:
        if not (200 <= response.status_code < 300):
            json = response.json()
            raise KintoneError(
                json['message'], response.text, json, response.status_code
            )
