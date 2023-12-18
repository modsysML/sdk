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

import importlib
import ast


from django.utils.module_loading import import_string
from modsys.avid.base import AbstractAVIDProvider

from modsys.const import (
    AVID_CLIENT_CLASS,
    GOOGLE_PERSPECTIVE_CLIENT_CLASS,
    OPENAI_CLIENT_CLASS,
    REST_CLIENT_CLASS,
    SCAMADVISOR_CLIENT_CLASS,
    SIGHTENGINE_CLIENT_CLASS,
)
from modsys.google.base import AbstractGooglePerspectiveProvider
from modsys.openai.base import AbstractOpenAIProvider
from modsys.scam_advisor.base import AbstractScamAdvisorProvider
from modsys.service.json.base import AbstractRestClient
from modsys.sightengine.base import AbstractSightengineProvider


def get_json_client(api_key) -> AbstractRestClient:
    client = import_string(REST_CLIENT_CLASS)
    return client(api_key)


def get_scam_advisor_client(api_key) -> AbstractScamAdvisorProvider:
    client = import_string(SCAMADVISOR_CLIENT_CLASS)
    return client(api_key)


def get_openai_client(provider_path: str) -> AbstractOpenAIProvider:
    client = import_string(OPENAI_CLIENT_CLASS)
    if provider_path.startswith("openai:"):
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = path_parts[1]
        if model_type == "chat":
            raise NotImplementedError
        elif model_type == "completion":
            return client("text-davinci-003")
        else:
            raise ValueError(f"Unknown OpenAI model type: {model_type}")
    else:
        return importlib.import_module(provider_path).default()


def get_google_client(
    provider_path: str, *args, **kwargs
) -> AbstractGooglePerspectiveProvider:
    client = import_string(GOOGLE_PERSPECTIVE_CLIENT_CLASS)
    secret = kwargs["secret"] if "secret" in kwargs else None
    if provider_path.startswith("google_perspective:"):
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = path_parts[1]
        if model_type == "analyze":
            return client(model_type, secret)
        elif model_type == "suggest":
            return client(model_type, secret)
        else:
            raise ValueError(f"Unknown OpenAI model type: {model_type}")
    else:
        return importlib.import_module(provider_path).default()


def get_sightengine_client(
    provider_path, secret: str, api_user: str
) -> AbstractSightengineProvider:
    client = import_string(SIGHTENGINE_CLIENT_CLASS)
    if provider_path.startswith("sightengine:"):
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = ast.literal_eval(path_parts[1])

        if len(model_type) > 0:
            return client(model_type, secret=secret, api_user=api_user)
        else:
            raise ValueError(f"No model type set for Sightengine: {model_name}")
        return path_parts
    else:
        return importlib.import_module(provider_path).default()


def get_avid_client() -> AbstractAVIDProvider:
    client = import_string(AVID_CLIENT_CLASS)
    return client()


def get_provider_client(provider_path: str, *args, **kwargs):
    secret = kwargs["secret"] if "secret" in kwargs else None
    api_user = kwargs["api_user"] if "api_user" in kwargs else None

    if provider_path.startswith("openai:"):
        client = import_string(OPENAI_CLIENT_CLASS)
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = path_parts[1]
        if model_type == "chat":
            raise NotImplementedError
        elif model_type == "completion":
            return client("text-davinci-003")
        else:
            raise ValueError(f"Unknown OpenAI model type: {model_type}")
    elif provider_path.startswith("google_perspective:"):
        client = import_string(GOOGLE_PERSPECTIVE_CLIENT_CLASS)
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = path_parts[1]
        if model_type == "analyze":
            return client(model_type, secret)
        elif model_type == "suggest":
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown OpenAI model type: {model_type}")
    elif provider_path.startswith("sightengine:"):
        client = import_string(SIGHTENGINE_CLIENT_CLASS)
        path_parts = provider_path.split(":")
        model_name = path_parts[0]
        model_type = ast.literal_eval(path_parts[1])

        if len(model_type) > 0:
            return client(model_type, secret=secret, api_user=api_user)
        else:
            raise ValueError(f"No model type set for Sightengine: {model_name}")
        return path_parts
    else:
        return importlib.import_module(provider_path).default()
