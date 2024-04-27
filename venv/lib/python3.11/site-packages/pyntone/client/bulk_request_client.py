from typing import Literal, TypedDict, Union

from pyntone.http.http_client import HttpClent, KintoneRequestParams
from pyntone.url import build_path

EndpointName = Literal[
    'record',
    'records',
    'record/status',
    'records/status',
    'record/assignees',
]

HttpMethod = Literal['POST', 'PUT', 'DELETE']


class ApiRequestParameter(TypedDict):
    method: HttpMethod
    api: str
    payload: dict


class EndopintRequestParameter(TypedDict):
    method: HttpMethod
    endpoint_name: EndpointName
    payload: dict


class BulkRequestClient:
    def __init__(
        self,
        client: HttpClent,
        guest_space_id: Union[int, str, None] = None,
    ) -> None:
        self.client = client
        self.guest_space_id = guest_space_id
        self.REQUESTS_LENGTH_LIMIT = 20

    def send(
        self,
        requests: Union[
            list[ApiRequestParameter],
            list[EndopintRequestParameter],
            list[Union[ApiRequestParameter, EndopintRequestParameter]],
        ],
    ):
        request_list = []
        for request in requests:
            endpoint_name = request.get('endpoint_name')
            if endpoint_name is not None:
                request_list.append(
                    {
                        'method': request['method'],
                        'api': self.__build_path_with_guest_space_id(endpoint_name),
                        'payload': request['payload'],
                    }
                )
            else:
                request_list.append(request)

        path = self.__build_path_with_guest_space_id('bulkRequest')
        params = KintoneRequestParams(requests=request_list)
        return self.client.post(path, params)

    def __build_path_with_guest_space_id(self, endpoint_name: str) -> str:
        return build_path(
            endpoint_name=endpoint_name, guest_space_id=self.guest_space_id
        )
