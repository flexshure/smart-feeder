import re
from typing import Optional, TypedDict, Union

from pyntone.client import AppClient, FileClient, RecordClient
from pyntone.client.bulk_request_client import BulkRequestClient
from pyntone.http.http_client import HttpClent
from pyntone.kintone_request_config_builder import KintoneRequestConfigBuilder
from pyntone.types.auth import DiscriminatedAuth


class FeatureFlags(TypedDict):
    enableAbortSearchError: bool


class KintoneRestAPIClient:
    def __init__(
        self,
        base_url: str,
        auth: DiscriminatedAuth,
        guest_space_id: Union[int, str, None] = None,
        # TODO
        # basic_auth=None,
        # client_cert_auth=None,
        # proxy=None,
        # feature_flags=None,
        # user_agent: Optional[str] = None,
    ) -> None:
        self.__base_url = re.sub('/+$', '', base_url)

        request_config_builder = KintoneRequestConfigBuilder(
            auth=auth, base_url=self.__base_url
        )
        httpClient = HttpClent(config_builder=request_config_builder)

        self.bulkRequest = BulkRequestClient(httpClient, guest_space_id)
        self.record = RecordClient(httpClient, self.bulkRequest, guest_space_id)
        self.app = AppClient(httpClient, guest_space_id)
        self.file = FileClient(httpClient, guest_space_id)
