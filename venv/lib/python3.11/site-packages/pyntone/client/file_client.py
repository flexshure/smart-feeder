from pathlib import Path
from typing import Any, Optional, TypedDict, Union

from pyntone.http.http_client import HttpClent
from pyntone.kintone_request_config_builder import (
    KintoneRequestFormData,
    KintoneRequestParams,
)
from pyntone.url import build_path

FilePath = Union[str, Path]


class FileData(TypedDict):
    name: str
    data: Any


class FileClient:
    def __init__(
        self, client: HttpClent, guest_space_id: Union[int, str, None]
    ) -> None:
        self.client = client
        self.guest_space_id = guest_space_id

    def upload_file(
        self, file: Union[FileData, FilePath], content_type: Optional[str] = None
    ):
        path = self.__build_path_with_guest_space_id('file')
        if type(file) is dict:
            params = KintoneRequestFormData(
                name=file['name'], data=file['data'], content_type=content_type
            )
        else:
            if type(file) is str:
                file_path = Path(file)
            elif type(file) is Path:
                file_path = file
            else:
                raise ValueError()
            if not file_path.is_file:
                raise ValueError()
            with open(file_path, 'rb') as f:
                params = KintoneRequestFormData(
                    name=file_path.name,
                    data=f.read(),
                    content_type=content_type,
                )
        return self.client.post_data(path, params)

    def download_file(self, file_key: str):
        params = KintoneRequestParams(fileKey=file_key)
        path = self.__build_path_with_guest_space_id('file')
        return self.client.get_data(path, params)

    def __build_path_with_guest_space_id(self, endpoint_name: str) -> str:
        return build_path(
            endpoint_name=endpoint_name, guest_space_id=self.guest_space_id
        )
