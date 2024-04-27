from typing import Literal, Optional, Union

from pyntone.client.bulk_request_client import (
    BulkRequestClient,
    EndopintRequestParameter,
)
from pyntone.http.http_client import HttpClent, KintoneRequestParams
from pyntone.types import AppID, CommentID, RecordID, Revision
from pyntone.types.record import (
    Comment,
    DeleteRecordParameter,
    RecordForParameter,
    UpdateKey,
    UpdateKeyRecordForParameter,
    UpdateRecordForParameter,
    UpdateRecordStatusParameter,
)
from pyntone.url import build_path

ADD_RECORDS_LIMIT = 100
UPDATE_RECORDS_LIMIT = 100
DELETE_RECORDS_LIMIT = 100
GET_RECORDS_LIMIT = 500


class RecordClient:
    def __init__(
        self,
        client: HttpClent,
        bulk_request_client: BulkRequestClient,
        guest_space_id: Union[int, str, None],
    ) -> None:
        self.client = client
        self.bulk_request_client = bulk_request_client
        self.guest_space_id = guest_space_id
        self.did_warn_maximum_offset_value = False

    def get_record(self, app: AppID, record_id: RecordID):
        path = self.__build_path_with_guest_space_id(endpoint_name='record')
        params = KintoneRequestParams(app=app, id=record_id)
        return self.client.get(path, params)

    def add_record(self, app: AppID, record: Optional[RecordForParameter] = None):
        path = self.__build_path_with_guest_space_id(endpoint_name='record')
        params = KintoneRequestParams(app=app, record=record)
        return self.client.post(path, params)

    def update_record(
        self,
        app: AppID,
        record_id: Optional[RecordID] = None,
        update_key: Optional[UpdateKey] = None,
        record: Optional[RecordForParameter] = None,
        revision: Optional[Revision] = None,
    ):
        if record_id is None and update_key is None:
            raise ValueError()
        path = self.__build_path_with_guest_space_id(endpoint_name='record')
        params = KintoneRequestParams(
            app=app,
            id=record_id,
            updateKey=update_key,
            record=record,
            revision=revision,
        )
        return self.client.put(path, params)

    def upsert_record(
        self,
        app: AppID,
        update_key: UpdateKey,
        record: Optional[RecordForParameter] = None,
        revision: Optional[Revision] = None,
    ):
        query = '{} = "{}"'.format(update_key['field'], update_key['value'])
        records = self.get_records(app, query=query)['records']
        if len(records) > 0:
            if records[0]['$id']['type'] == '__ID__':
                result = self.update_record(
                    app, update_key=update_key, record=record, revision=revision
                )
                return {
                    'id': records[0]['$id']['value'],
                    'revision': result['revision'],
                }
            raise Exception('Missing `$id` in `getRecords` response.')
        return self.add_record(
            app,
            {
                f"{update_key['field']}": {'value': update_key['value']},
                **({} if record is None else record),
            },
        )

    def get_records(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        total_count: Optional[bool] = None,
    ):
        path = self.__build_path_with_guest_space_id(endpoint_name='records')
        params = KintoneRequestParams(
            app=app, fields=fields, query=query, totalCount=total_count
        )
        return self.client.get(path, params)

    def add_records(self, app: AppID, records: list[RecordForParameter]):
        path = self.__build_path_with_guest_space_id(endpoint_name='records')
        params = KintoneRequestParams(app=app, records=records)
        return self.client.post(path, params)

    def update_records(
        self,
        app: AppID,
        records: Union[
            list[UpdateRecordForParameter],
            list[UpdateKeyRecordForParameter],
            list[Union[UpdateRecordForParameter, UpdateKeyRecordForParameter]],
        ],
    ):
        path = self.__build_path_with_guest_space_id(endpoint_name='records')
        params = KintoneRequestParams(app=app, records=records)
        return self.client.put(path, params)

    def delete_records(
        self, app: AppID, ids: list[RecordID], revisions: Optional[list[Revision]]
    ):
        path = self.__build_path_with_guest_space_id(endpoint_name='records')
        params = KintoneRequestParams(app=app, ids=ids, revisions=revisions)
        return self.client.delete(path, params)

    def create_cursor(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
        size: Union[int, str, None] = None,
    ):
        path = self.__build_path_with_guest_space_id(endpoint_name='records/cursor')
        params = KintoneRequestParams(app=app, fields=fields, query=query, size=size)
        return self.client.post(path, params)

    def get_records_by_cursor(self, cursor_id: str):
        path = self.__build_path_with_guest_space_id(endpoint_name='records/cursor')
        params = KintoneRequestParams(id=cursor_id)
        return self.client.get(path, params)

    def delete_cursor(self, cursor_id: str):
        path = self.__build_path_with_guest_space_id(endpoint_name='records/cursor')
        params = KintoneRequestParams(id=cursor_id)
        return self.client.delete(path, params)

    def get_all_records(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        condition: Optional[str] = None,
        order_by: Optional[str] = None,
        with_cursor: bool = False,
    ):
        if with_cursor:
            condition_query = f'{condition} ' if condition is not None else ''
            order_by_query = f'order by {order_by}' if order_by is not None else ''
            query = f'{condition_query}{order_by_query}'
            query = None if query == '' else query
            return self.get_all_records_with_cursor(app, fields, query)
        if order_by is None:
            return self.get_all_records_with_id(app, fields, condition)
        return self.get_all_records_with_offset(app, fields, condition, order_by)

    def get_all_records_with_id(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        condition: Optional[str] = None,
    ):
        if fields is not None and len(fields) > 0 and not '$id' in fields:
            fields.append('$id')
        return self.__get_all_records_recursive_with_id(app, fields, condition, '0', [])

    def __get_all_records_recursive_with_id(
        self,
        app: AppID,
        fields: Optional[list[str]],
        condition: Optional[str],
        id: str,
        records: list,
    ):
        condition_query = f'({condition}) and ' if condition is not None else ''
        query = (
            f'{condition_query}$id > {id} order by $id asc limit {GET_RECORDS_LIMIT}'
        )
        result = self.get_records(app, fields, query)
        all_records = records + result['records']
        if len(result['records']) < GET_RECORDS_LIMIT:
            return all_records
        last_record = result['records'][-1]
        if last_record['$id']['type'] == '__ID__':
            last_id = last_record['$id']['value']
            return self.__get_all_records_recursive_with_id(
                app, fields, condition, last_id, all_records
            )
        raise Exception('Missing `$id` in `getRecords` response.')

    def get_all_records_with_offset(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        condition: Optional[str] = None,
        order_by: Optional[str] = None,
    ):
        return self.__get_all_records_recursive_with_offset(
            app, fields, condition, order_by, 0, []
        )

    def __get_all_records_recursive_with_offset(
        self,
        app: AppID,
        fields: Optional[list[str]],
        condition: Optional[str],
        order_by: Optional[str],
        offset: int,
        records: list,
    ):
        condition_query = f'{condition} ' if condition is not None else ''
        order_by_query = f'order by {order_by} ' if order_by is not None else ''
        query = f'{condition_query}{order_by_query}limit {GET_RECORDS_LIMIT} offset {offset}'
        result = self.get_records(app, fields, query)
        all_records = records + result['records']
        if len(result['records']) < GET_RECORDS_LIMIT:
            return all_records
        return self.__get_all_records_recursive_with_offset(
            app, fields, condition, order_by, offset + GET_RECORDS_LIMIT, all_records
        )

    def get_all_records_with_cursor(
        self,
        app: AppID,
        fields: Optional[list[str]] = None,
        query: Optional[str] = None,
    ) -> list:
        res = self.create_cursor(app, fields, query, size=500)
        cursor_id = res['id']
        try:
            return self.__get_all_records_recursive_by_cursor(cursor_id, [])
        except Exception as e:
            self.delete_cursor(cursor_id)
            raise e

    def __get_all_records_recursive_by_cursor(
        self, cursor_id: str, records: list
    ) -> list:
        result = self.get_records_by_cursor(cursor_id)
        all_records = records + result['records']
        if result['next']:
            return self.__get_all_records_recursive_by_cursor(cursor_id, all_records)
        return all_records

    def add_all_records(self, app: AppID, records: list[RecordForParameter]):
        if not all(
            not isinstance(record, list) and isinstance(record, dict)
            for record in records
        ):
            raise ValueError('the `records` parameter must be an array of object.')
        return self.__add_all_records_recursive(app, records, len(records), [])

    def __add_all_records_recursive(
        self,
        app: AppID,
        records: list[RecordForParameter],
        num_of_all_records: int,
        results: list,
    ) -> dict:
        CHUNK_LENGTH = (
            self.bulk_request_client.REQUESTS_LENGTH_LIMIT * ADD_RECORDS_LIMIT
        )
        records_chunk = records[:CHUNK_LENGTH]
        if len(records_chunk) == 0:
            return {'records': results}
        new_results = []
        try:
            new_results = self.__add_all_records_with_bulk_request(app, records_chunk)
        except Exception as e:
            # TODO
            raise e
        return self.__add_all_records_recursive(
            app, records[CHUNK_LENGTH:], num_of_all_records, results + new_results
        )

    def __add_all_records_with_bulk_request(
        self, app: AppID, records: list[RecordForParameter]
    ):
        separated_records = self.__separate_array_recursive(
            ADD_RECORDS_LIMIT, [], records
        )
        requests: list[EndopintRequestParameter] = [
            {
                'method': 'POST',
                'endpoint_name': 'records',
                'payload': {'app': app, 'records': records_},
            }
            for records_ in separated_records
        ]
        results = self.bulk_request_client.send(requests)['results']
        return_value = []
        for result in results:
            ids = result['ids']
            revisions = result['revisions']
            return_value += [
                {'id': val, 'revision': revisions[num]} for num, val in enumerate(ids)
            ]
        return return_value

    def update_all_records(
        self,
        app: AppID,
        records: Union[
            list[UpdateRecordForParameter],
            list[UpdateKeyRecordForParameter],
            list[Union[UpdateRecordForParameter, UpdateKeyRecordForParameter]],
        ],
    ):
        return self.__update_all_records_recursive(app, records, len(records), [])

    def __update_all_records_recursive(
        self,
        app: AppID,
        records: Union[
            list[UpdateRecordForParameter],
            list[UpdateKeyRecordForParameter],
            list[Union[UpdateRecordForParameter, UpdateKeyRecordForParameter]],
        ],
        num_of_all_records: int,
        results: list,
    ):
        CHUNK_LENGTH = (
            self.bulk_request_client.REQUESTS_LENGTH_LIMIT * UPDATE_RECORDS_LIMIT
        )
        records_chunk = records[:CHUNK_LENGTH]
        if len(records_chunk) == 0:
            return {'records': results}
        new_results = []
        try:
            new_results = self.__update_all_records_with_bulk_request(
                app, records_chunk
            )
        except Exception as e:
            # TODO
            raise e
        return self.__update_all_records_recursive(
            app, records[CHUNK_LENGTH:], num_of_all_records, results + new_results
        )

    def __update_all_records_with_bulk_request(
        self,
        app: AppID,
        records: Union[
            list[UpdateRecordForParameter],
            list[UpdateKeyRecordForParameter],
            list[Union[UpdateRecordForParameter, UpdateKeyRecordForParameter]],
        ],
    ):
        separated_records = self.__separate_array_recursive(
            UPDATE_RECORDS_LIMIT, [], records
        )
        requests: list[EndopintRequestParameter] = [
            {
                'method': 'PUT',
                'endpoint_name': 'records',
                'payload': {
                    'app': app,
                    'records': records_,
                },
            }
            for records_ in separated_records
        ]
        results = self.bulk_request_client.send(requests)['results']
        return_value = []
        for result in results:
            return_value += result['records']
        return return_value

    def delete_all_reocrds(self, app: AppID, records: list[DeleteRecordParameter]):
        return self.__delete_all_records_recursive(app, records, len(records))

    def __delete_all_records_recursive(
        self, app: AppID, records: list[DeleteRecordParameter], num_of_all_records: int
    ):
        CHUNK_LENGTH = (
            self.bulk_request_client.REQUESTS_LENGTH_LIMIT * DELETE_RECORDS_LIMIT
        )
        records_chunk = records[:CHUNK_LENGTH]
        if len(records_chunk) == 0:
            return {}
        try:
            self.__delete_all_records_with_bulk_request(app, records_chunk)
        except Exception as e:
            # TODO
            raise e
        return self.__delete_all_records_recursive(
            app, records[CHUNK_LENGTH:], num_of_all_records
        )

    def __delete_all_records_with_bulk_request(
        self, app: AppID, records: list[DeleteRecordParameter]
    ):
        separated_records = self.__separate_array_recursive(
            DELETE_RECORDS_LIMIT, [], records
        )
        requests: list[EndopintRequestParameter] = [
            {
                'method': 'DELETE',
                'endpoint_name': 'records',
                'payload': {
                    'app': app,
                    'ids': [record['id'] for record in records_],
                    'revisions': [record.get('revision', -1) for record in records_],
                },
            }
            for records_ in separated_records
        ]
        self.bulk_request_client.send(requests)['results']
        return None

    def __separate_array_recursive(
        self, size: int, separated: list[list], array: list
    ) -> list[list]:
        chunk = array[:size]
        if len(chunk) == 0:
            return separated
        return self.__separate_array_recursive(size, [*separated, chunk], array[size:])

    def add_record_comment(self, app: AppID, record: RecordID, comment: Comment):
        path = self.__build_path_with_guest_space_id('record/comment')
        params = KintoneRequestParams(app=app, record=record, comment=comment)
        return self.client.post(path, params)

    def delete_record_comment(self, app: AppID, record: RecordID, comment: CommentID):
        path = self.__build_path_with_guest_space_id('record/comment')
        params = KintoneRequestParams(app=app, record=record, comment=comment)
        return self.client.delete(path, params)

    def get_record_comments(
        self,
        app: AppID,
        record: RecordID,
        order: Optional[Literal['asc', 'desc']] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ):
        path = self.__build_path_with_guest_space_id('record/comments')
        params = KintoneRequestParams(
            app=app, record=record, order=order, offset=offset, limit=limit
        )
        return self.client.get(path, params)

    def update_record_assigness(
        self,
        app: AppID,
        id: RecordID,
        assignees: list[str],
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('record/assignees')
        params = KintoneRequestParams(
            app=app, id=id, assignees=assignees, revision=revision
        )
        return self.client.put(path, params)

    def update_record_status(
        self,
        app: AppID,
        id: RecordID,
        action: str,
        assignees: Optional[list[str]] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('record/status')
        params = KintoneRequestParams(
            app=app, id=id, action=action, assignees=assignees, revision=revision
        )
        return self.client.put(path, params)

    def update_records_status(
        self, app: AppID, records: list[UpdateRecordStatusParameter]
    ):
        path = self.__build_path_with_guest_space_id('records/status')
        params = KintoneRequestParams(app=app, records=records)
        return self.client.put(path, params)

    def __build_path_with_guest_space_id(self, endpoint_name: str) -> str:
        return build_path(
            endpoint_name=endpoint_name, guest_space_id=self.guest_space_id
        )
