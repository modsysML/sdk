# Copyright: (c) 2022, Adrian Brown <adrbrownx@gmail.com>
# Copyright: (c) 2023, ModsysML Project
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


from modsys.service.json.base import AbstractRestClient


class AbstractSightengineProvider(AbstractRestClient):
    def id(self) -> str:
        raise NotImplementedError

    def to_string(self) -> str:
        raise NotImplementedError

    def i18n(self) -> str:
        raise NotImplementedError

    def persist_settings(self) -> str:
        raise NotImplementedError
