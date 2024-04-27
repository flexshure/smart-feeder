from typing import Optional, Union, Literal
from pyntone.http.http_client import HttpClent, KintoneRequestParams
from pyntone.url import build_path
from pyntone.types import AppID, Revision, RecordID
from pyntone.client.types import Lang, AppCustomizeScope


class AppClient:
    def __init__(
        self, client: HttpClent, guest_space_id: Union[int, str, None]
    ) -> None:
        self.client = client
        self.guest_space_id = guest_space_id

    def get_form_fields(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('app/form/fields', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def add_form_fields(
        self, app: AppID, properties, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/form/fields', True)
        params = KintoneRequestParams(app=app, properties=properties, revision=revision)
        return self.client.get(path, params)

    def update_form_fields(
        self, app: AppID, properties, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/form/fields', True)
        params = KintoneRequestParams(app=app, properties=properties, revision=revision)
        return self.client.put(path, params)

    def delete_form_fields(
        self, app: AppID, fields: list[str], revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/form/fields', True)
        params = KintoneRequestParams(app=app, fields=fields, revision=revision)
        return self.client.delete(path, params)

    def get_form_layout(self, app: AppID, preview: bool = False):
        path = self.__build_path_with_guest_space_id('app/form/layout', preview)
        params = KintoneRequestParams(app=app)
        return self.client.get(path, params)

    def update_form_layout(
        self, app: AppID, layout, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/form/layout', True)
        params = KintoneRequestParams(app=app, layout=layout, revision=revision)
        return self.client.put(path, params)

    def get_views(self, app: AppID, lang: Optional[Lang] = None, preview: bool = False):
        path = self.__build_path_with_guest_space_id('app/views', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_views(self, app: AppID, views, revision: Optional[Revision] = None):
        path = self.__build_path_with_guest_space_id('app/views', True)
        params = KintoneRequestParams(app=app, views=views, revision=revision)
        return self.client.put(path, params)

    def get_app(self, id: AppID):
        path = self.__build_path_with_guest_space_id('app')
        params = KintoneRequestParams(id=id)
        return self.client.get(path, params)

    def get_apps(
        self,
        ids: Optional[list[AppID]] = None,
        codes: Optional[list[str]] = None,
        name: Optional[str] = None,
        space_ids: Optional[list[Union[int, str]]] = None,
        limit: Union[int, str, None] = None,
        offset: Union[int, str, None] = None,
    ):
        path = self.__build_path_with_guest_space_id('apps')
        params = KintoneRequestParams(
            ids=ids,
            codes=codes,
            name=name,
            space_ids=space_ids,
            limit=limit,
            offset=offset,
        )
        return self.client.get(path, params)

    def add_app(self):
        raise NotImplementedError()

    def get_app_settings(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('app/settings', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_app_settings(
        self,
        app: AppID,
        name: Optional[str] = None,
        description: Optional[str] = None,
        icon: Optional[dict] = None,
        theme: Optional[
            Literal[
                'WHITE',
                'CLIPBOARD',
                'BINDER',
                'PENCIL',
                'CLIPS',
                'RED',
                'BLUE',
                'GREEN',
                'YELLOW',
                'BLACK',
            ]
        ] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('app/settings', True)
        params = KintoneRequestParams(
            app=app,
            name=name,
            description=description,
            icon=icon,
            theme=theme,
            revision=revision,
        )
        return self.client.put(path, params)

    def get_process_management(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('app/status', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_process_management(
        self,
        app: AppID,
        enable: Optional[bool] = None,
        states: Optional[dict] = None,
        actions: Optional[dict] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('app/status', True)
        params = KintoneRequestParams(
            app=app, enable=enable, states=states, actions=actions, revision=revision
        )
        return self.client.put(path, params)

    def get_deploy_status(self, apps: list[AppID]):
        path = self.__build_path_with_guest_space_id('app/deploy', True)
        params = KintoneRequestParams(apps=apps)
        return self.client.get(path, params)

    def deploy_app(self, apps: list[dict], revert: Optional[bool] = None):
        path = self.__build_path_with_guest_space_id('app/deploy', True)
        params = KintoneRequestParams(apps=apps, revert=revert)
        return self.client.post(path, params)

    def get_field_acl(self, app: AppID, preview: bool = False):
        path = self.__build_path_with_guest_space_id('field/acl', preview)
        params = KintoneRequestParams(app=app)
        return self.client.get(path, params)

    def update_field_acl(
        self, app: AppID, rights: list, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('field/acl', True)
        params = KintoneRequestParams(app=app, rights=rights, revision=revision)
        return self.client.put(path, params)

    def get_app_acl(self, app: AppID, preview: bool = False):
        path = self.__build_path_with_guest_space_id('app/acl', preview)
        params = KintoneRequestParams(app=app)
        return self.client.get(path, params)

    def update_app_acl(
        self, app: AppID, rights: list, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/acl', True)
        params = KintoneRequestParams(app=app, rights=rights, revision=revision)
        return self.client.put(path, params)

    def evaluate_records_acl(self, app: AppID, ids: list[RecordID]):
        path = self.__build_path_with_guest_space_id('records/acl/evaluate')
        params = KintoneRequestParams(app=app, ids=ids)
        return self.client.get(path, params)

    def get_record_acl(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('record/acl', preview=preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_record_acl(
        self, app: AppID, rights: list, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('record/acl', True)
        params = KintoneRequestParams(app=app, rights=rights, revision=revision)
        return self.client.put(path, params)

    def get_app_customize(self, app: AppID, preview: bool = False):
        path = self.__build_path_with_guest_space_id('app/customize', preview)
        params = KintoneRequestParams(app=app)
        return self.client.get(path, params)

    def update_app_customize(
        self,
        app: AppID,
        scope: Optional[AppCustomizeScope] = None,
        desktop: Optional[dict] = None,
        mobile: Optional[dict] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('app/customize', True)
        params = KintoneRequestParams(
            app=app, scope=scope, desktop=desktop, mobile=mobile, revision=revision
        )
        return self.client.put(path, params)

    def get_general_notifications(self, app: AppID, preview: bool = False):
        path = self.__build_path_with_guest_space_id(
            'app/notifications/general', preview
        )
        params = KintoneRequestParams(app=app)
        return self.client.get(path, params)

    def update_general_notifications(
        self,
        app: AppID,
        notifications: Optional[list] = None,
        notify_to_commenter: Optional[bool] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('app/notifications/general', True)
        params = KintoneRequestParams(
            app=app,
            notifications=notifications,
            notifyToCommenter=notify_to_commenter,
            revision=revision,
        )
        return self.client.put(path, params)

    def get_per_record_notifications(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id(
            'app/notifications/perRecord', preview
        )
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_per_record_notifications(
        self,
        app: AppID,
        notifications: Optional[list] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id(
            'app/notifications/perRecord', True
        )
        params = KintoneRequestParams(
            app=app, notifications=notifications, revision=revision
        )
        return self.client.put(path, params)

    def get_reminder_notifications(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id(
            'app/notifications/reminder', preview
        )
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_reminder_notifications(
        self,
        app: AppID,
        notifications: Optional[list] = None,
        timezone: Optional[str] = None,
        revision: Optional[Revision] = None,
    ):
        path = self.__build_path_with_guest_space_id('app/notifications/reminder', True)
        params = KintoneRequestParams(
            app=app, notifications=notifications, timezone=timezone, revision=revision
        )
        return self.client.put(path, params)

    def get_reports(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('app/reports', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_reports(
        self, app: AppID, reports: dict, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/reports', True)
        params = KintoneRequestParams(app=app, reports=reports, revision=revision)
        return self.client.put(path, params)

    def get_app_actions(
        self, app: AppID, lang: Optional[Lang] = None, preview: bool = False
    ):
        path = self.__build_path_with_guest_space_id('app/actions', preview)
        params = KintoneRequestParams(app=app, lang=lang)
        return self.client.get(path, params)

    def update_app_actions(
        self, app: AppID, actions: dict, revision: Optional[Revision] = None
    ):
        path = self.__build_path_with_guest_space_id('app/actions', True)
        params = KintoneRequestParams(app=app, actions=actions, revision=revision)
        return self.client.put(path, params)

    def __build_path_with_guest_space_id(
        self, endpoint_name: str, preview: bool = False
    ) -> str:
        return build_path(
            endpoint_name=endpoint_name,
            guest_space_id=self.guest_space_id,
            preview=preview,
        )
