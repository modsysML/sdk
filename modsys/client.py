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

import itertools
import json
from modsys.plugins.evaluations import evaluate
from termcolor import colored, cprint

from modsys.exceptions import ExecutionError
from modsys.resource import General


class Modsys(General):
    @classmethod
    def report(
        cls,
        provider_name,
        provider_model,
        dataset_name,
        dataset_link,
        summary,
        path_to_create_report,
    ):
        try:
            response = cls.avid_curs.create_report(
                provider_name,
                provider_model,
                dataset_name,
                dataset_link,
                summary,
                path_to_create_report,
            )
        except Exception as err:
            raise ExecutionError(err)

        return response

    @classmethod
    def use(cls, provider, token="Beta_token123", *args, **kwargs):
        provider = provider.lower()
        # TODO: Move apollo connection to its own
        # method like openai once integrated
        if provider == "apollo":
            cls.model = "Apollo"
            if token:
                cls._auth_token = token
                print(f"Connected to {provider} provider, using Safety model")
            else:
                print(
                    "Please set a auth token or use the sandbox: Apollo.sandbox_test()"
                )
        elif provider.startswith(
            "openai:"
        ):  # NOTE update the return method to detectText
            cls.model = "OpenAI"
            cls._provider_path = provider
            return cls._openai_manager.load_openai_provider(cls._provider_path)
        elif provider.startswith("google_perspective:"):
            cls.model = "Google"
            cls._google_perspective_provider_path = provider
            cls._google_perspective_auth_token = (
                kwargs["google_perspective_api_key"]
                if "google_perspective_api_key" in kwargs
                else None
            )
        elif provider.startswith("sightengine:"):
            cls.model = "Sightengine"
            cls._sightengine_provider_path = (
                provider  # provider = "sightengine:[<model/s>]"
            )
            cls._sightengine_auth_token = (
                kwargs["sightengine_api_key"]
                if "sightengine_api_key" in kwargs
                else None
            )
            cls._sightengine_api_user = (
                kwargs["sightengine_api_user"]
                if "sightengine_api_user" in kwargs
                else None
            )
        elif provider == "scam_advisor":
            cls.model = "Scam Advisor"
            cls._scam_advisor_token = (
                kwargs["scam_advisor_api_key"]
                if "scam_advisor_api_key" in kwargs
                else None
            )
        else:
            return f"Provider {provider} not found"

    @classmethod
    def detectText(cls, *args, **kwargs):
        """
        Detects text using the appropriate provider based on the `model` attribute of the class. If using google_perspective can also suggest scores as well.

        :param text: The text to be detected (optional).
        :type text: str
        :param operator: The operator to be used (optional).
        :type operator: str
        :param threshold: The threshold value to be used (optional).
        :type threshold: float
        :param scores: A dict of attributes with their respective scores that you'd like to suggest (optional).
        :type threshold: dict

        :return: The result of the text detection operation.
        :rtype: str

        """
        text = kwargs.get("text")
        operator = kwargs.get("operator")
        threshold = kwargs.get("threshold")
        if cls.model == "Apollo":  # TODO: changes with sandbox update
            # print(cls.model)
            conn = cls._service_manager.connect(cls._auth_token)
            return conn.make_https_request({"rule": f"{text} {operator} {threshold}"})
        elif cls.model == "Google":
            conn = cls._googleai_manager.load_google_provider(
                cls._google_perspective_provider_path,
                secret=cls._google_perspective_auth_token,
            )
            return conn.call_api(
                kwargs["prompt"] if "prompt" in kwargs else None,
                kwargs["content_id"] if "content_id" in kwargs else None,
                kwargs["community_id"] if "community_id" in kwargs else None,
                kwargs["score"] if "score" in kwargs else None,
                kwargs["category"] if "category" in kwargs else None,
            )
        elif cls.model == "Scam Advisor":
            conn = cls._scam_advisor_manager.connect(cls._scam_advisor_token)
            return conn.call_api(kwargs["domain"] if "domain" in kwargs else None)
        else:
            return "No provider connected"

    @classmethod
    def detectImage(cls, url, *args, **kwargs):
        if cls.model == "Sightengine":
            conn = cls._sightengine_manager.load_sightengine_provider(
                cls._sightengine_provider_path,
                cls._sightengine_auth_token,
                cls._sightengine_api_user,
            )
            return conn.call_api(url)
        else:
            raise NotImplementedError

    @classmethod
    def evaluate(cls, vars: list, community_id):
        """
        After setting up the connection criteria for google_perspecitve
        run the evaluation.

        vars (json): [
            {
                "item": "You suck at this game.",
                "__expected": {
                    "TOXICITY": {
                        "value": "0.83"
                    } (label)
                },
                "__trend": "higher"
            }
        ] - responsible for setting up test run

        provider (str): "google_perspective:analyze"
        """
        if cls.model == "Google":
            conn = cls._api_manager.load_provider(
                cls._google_perspective_provider_path,
                secret=cls._google_perspective_auth_token,
            )
        else:
            raise NotImplementedError

        options = {"prompts": ["evaluate: {{item}}"], "vars": vars, "providers": [conn]}

        # Evaluation
        summary = evaluate(options, conn, community_id=community_id)
        print_yellow = lambda x: cprint(x, "yellow")
        print_yellow(f"Evaluation complete: {json.dumps(summary['stats'], indent=4)}")

        # Output
        return summary["results"]
