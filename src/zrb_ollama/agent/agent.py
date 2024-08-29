import json
import re
import time
import traceback
from collections.abc import Callable, Mapping
from typing import Annotated, Any, Optional

import litellm
from zrb.helper.callable import run_async
from zrb.helper.typecheck import typechecked

from ..config import DEFAULT_SYSTEM_PROMPT, DEFAULT_SYSTEM_MESSAGE_TEMPLATE
from ._helper import extract_metadata, get_metadata_description, get_metadata_signature


@typechecked
class Agent:

    def __init__(
        self,
        model: str,
        system_message_template: str = DEFAULT_SYSTEM_MESSAGE_TEMPLATE,
        system_prompt: str = DEFAULT_SYSTEM_PROMPT,
        previous_messages: Optional[list[Any]] = None,
        tools: list[Callable] = [],
        max_iteration: int = 10,
        should_show_system_prompt: bool = False,
        should_show_history: bool = False,
        conversation_log_path: Optional[str] = None,
        print_fn: Optional[Callable[[str], Any]] = None,
        **kwargs: Mapping[str, Any],
    ):
        def finish_conversation(
            final_answer: Annotated[str, "Final answer containing all necessary information and citations"]  # noqa
        ) -> str:
            """Ends up conversation with user by providing the final_answer. The final_answer should contains all detailed information and citations."""  # noqa
            self._finished = True
            return final_answer

        self._model = model
        self._tools = [finish_conversation] + tools
        self._max_iteration = max_iteration
        self._kwargs = kwargs
        self._should_show_system_prompt = should_show_system_prompt
        self._should_show_history = should_show_history
        self._conversation_log_path = conversation_log_path
        self._return = ""
        self._print = print if print_fn is None else print_fn
        self._function_schemas = {
            fn.__name__: extract_metadata(fn) for fn in self._tools
        }
        self._function_signatures = {
            fn_name: get_metadata_signature(metadata)
            for fn_name, metadata in self._function_schemas.items()
        }
        self._function_names = [key for key in self._function_schemas]
        self._function_map = {fn.__name__: fn for fn in self._tools}
        function_names_str = ", ".join([f"`{key}`" for key in self._function_names])
        self._response_format = {
            "thought": "<your plan and reasoning to choose an action>",
            "action": {
                "function": f"<function name, SHOULD STRICTLY be one of these: {function_names_str}>",  # noqa
                "arguments": {
                    "<argument-1>": "<value-1>",
                    "<argument-2>": "<value-2>",
                },
            },
        }
        self._system_message = {
            "role": "system",
            "content": system_message_template.format(
                system_prompt=system_prompt,
                response_format=json.dumps(self._response_format, indent=2),
                function_names=", ".join(self._function_names),
                function_signatures="\n".join(
                    [
                        "\n".join(
                            [
                                f"- {signature}",
                                "  "
                                + get_metadata_description(
                                    self._function_schemas[fn_name]
                                ),
                            ]
                        ).strip()
                        for fn_name, signature in self._function_signatures.items()
                    ]
                ),
                function_schemas=json.dumps(self._function_schemas, indent=2),
            ),
        }
        self._previous_messages = (
            previous_messages if previous_messages is not None else []
        )  # noqa
        self._finished = False

    def get_system_message(self) -> Any:
        return self._system_message

    def get_previous_messages(self) -> list[Any]:
        return self._previous_messages

    def get_messages(self) -> list[Any]:
        return [self._system_message] + self._previous_messages

    async def add_user_message(self, user_message: str) -> list[Any]:
        self._append_user_message(user_message)
        self._print_system_prompt()
        self._print_previous_messages()
        for _ in range(self._max_iteration):
            start = time.time()
            self._print("🧠 Processing...")
            response = await litellm.acompletion(
                model=self._model, messages=self.get_messages(), **self._kwargs
            )
            end = time.time()
            elapsed = end - start
            response_message = response.choices[0].message
            self._print(f"🤖 Response ({elapsed:.2f} seconds): {response_message}")
            try:
                response_map = self._extract_agent_message(response_message.content)
                self._validate_agent_message(response_map)
                self._append_agent_message(json.dumps(response_map))
            except Exception as exc:
                self._print(f"🛑 Error: {exc}")
                traceback.print_exc()
                self._append_agent_message(response_message.content)
                self._append_feedback_error(exc)
                continue
            self._print(f"🥝 Response map: {response_map}")
            action = response_map.get("action", {})
            function_name = action.get("function", "")
            function_kwargs = action.get("arguments", {})
            result = None
            try:
                self._validate_function_call(function_name, function_kwargs)
                start = time.time()
                result = await self._execute_function(function_name, function_kwargs)
                end = time.time()
                elapsed = end - start
                self._print(f"✅ Result ({elapsed:.2f} seconds): {result}")
                self._append_function_call_ok(function_name, function_kwargs, result)
            except Exception as exc:
                self._print(f"🛑 Error: {exc}")
                traceback.print_exc()
                self._append_function_call_error(function_name, function_kwargs, exc)
            if self._finished:
                return result
        self._finished = False
        return None

    def _print_system_prompt(self):
        if self._should_show_system_prompt:
            self._print("📜 System prompt")
            self._print(self.get_system_message()["content"])

    def _print_previous_messages(self):
        previous_messages = self.get_previous_messages()
        if self._should_show_history and len(previous_messages) > 0:
            self._print("📜 History")
            for previous_message in previous_messages:
                self._print(previous_message)

    def _append_user_message(self, user_message: str):
        self._append_message({"role": "user", "content": user_message})

    def _append_agent_message(self, assistant_message: str):
        self._append_message({"role": "assistant", "content": assistant_message})

    def _append_feedback_error(self, exc: Exception):
        self._append_message(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "type": "feedback_error",
                        "error": self._extract_exception(exc),
                    }
                ),
            }
        )

    def _append_function_call_error(
        self, function: str, arguments: list[str], exc: Exception
    ):
        self._append_message(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "type": "function_call_error",
                        "function": function,
                        "arguments": arguments,
                        "error": self._extract_exception(exc),
                    }
                ),
            }
        )

    def _append_function_call_ok(
        self, function_name: str, arguments: list[str], result: Any
    ):
        self._append_message(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "type": "function_call_ok",
                        "function": function_name,
                        "arguments": arguments,
                        "result": result,
                    }
                ),
            }
        )

    def _append_message(self, message: Any):
        self._previous_messages.append(message)

    def _extract_exception(self, exc: Exception) -> Any:
        exc_str = f"{exc}"
        try:
            return json.loads(exc_str)
        except Exception:
            return exc_str

    def _map_to_exception(self, data: Mapping[str, Any]) -> Exception:
        return Exception(json.dumps(data))

    def _validate_function_call(
        self, function_name: str, kwargs: Mapping[str, Any]
    ) -> Any:
        if function_name not in self._function_schemas:
            raise self._map_to_exception(
                {
                    "error": "INVALID FUNCTION",
                    "details": f"The function `{function_name}` is not a recognized",
                    "valid_functions": self._function_names,
                    "required_action": "Choose a valid function",
                }
            )
        missing_arguments = []
        invalid_arguments = []
        # ensure all required arguments is provided
        for key, value in self._function_schemas[function_name]["arguments"].items():
            if value["required"] and key not in kwargs:
                missing_arguments.append(key)
        # ensure all provided arguments are on the spec
        for key in kwargs:
            if key not in self._function_schemas[function_name]["arguments"]:
                invalid_arguments.append(key)
        # contruct error if any
        if len(missing_arguments) > 0 or len(invalid_arguments) > 0:
            error_details = {}
            if len(missing_arguments) > 0:
                error_details["missing_arguments"] = missing_arguments
            if len(invalid_arguments) > 0:
                error_details["invalid_arguments"] = invalid_arguments
            raise self._map_to_exception(
                {
                    "error": "INVALID ARGUMENTS",
                    "details": error_details,
                    "correct_function_schema": self._function_schemas[function_name],
                    "required_action": "Revise your response to include all required arguments and remove any invalid ones",  # noqa
                }
            )

    async def _execute_function(
        self, function_name: str, kwargs: Mapping[str, Any]
    ) -> Any:
        try:
            function_map = self._function_map
            return await run_async(function_map[function_name], **kwargs)
        except Exception as exc:
            raise self._map_to_exception(
                {
                    "error": "EXECUTION FAILED",
                    "details": f"{exc}",
                    "correct_function_schema": self._function_schemas[function_name],
                    "required_action": "Revise your arguments",
                }
            )

    def _extract_agent_message(self, response_content) -> Mapping[str, Any]:
        try:
            return json.loads(response_content)
        except Exception:
            json_pattern = re.compile(r"```(json)?\n({.*?})\n```", re.DOTALL)
            # Search for the pattern in the content
            match = json_pattern.search(response_content)
            if match:
                json_str = match.group(2)
                # Parse the JSON string to ensure it is valid
                return json.loads(json_str)
            # The dumbest way
            brace_stack = []
            json_start = -1
            json_end = -1
            for i, char in enumerate(response_content):
                if char == "{":
                    if not brace_stack:
                        json_start = i
                    brace_stack.append("{")
                elif char == "}":
                    if brace_stack:
                        brace_stack.pop()
                        if not brace_stack:
                            json_end = i + 1
                            break
            if json_start != -1 and json_end != -1:
                json_str = response_content[json_start:json_end]
                # Parse the JSON string to ensure it is valid
                try:
                    return json.loads(json_str)
                except Exception:
                    pass
            raise self._map_to_exception(
                {
                    "error": "MALFORMED PAYLOAD",
                    "error_message": "Your response does not match the required JSON format",  # noqa
                    "expected_format": self._response_format,
                    "required_action": "Reformat your entire response to match the expected_format",  # noqa
                }
            )

    def _validate_agent_message(self, json_message: Mapping[str, Any]):
        error_details = []
        if "thought" not in json_message:
            error_details.append("The `thought` field is missing")
        if "thought" in json_message and not isinstance(json_message["thought"], str):
            error_details.append("The `thought` field is not a string")
        if "action" not in json_message:
            error_details.append("The `action` field is missing")
        if "action" in json_message and not isinstance(json_message["action"], dict):
            error_details.append("The `action` field is not an object")
        if "action" in json_message and isinstance(json_message["action"], dict):
            if "function" not in json_message["action"]:
                error_details.append(
                    "The `function` field is missing from the `action` object"
                )  # noqa
            if "function" in json_message["action"] and not isinstance(
                json_message["action"]["function"], str
            ):  # noqa
                error_details.append("The action's `function` field is not a string")
            if "arguments" not in json_message["action"]:
                error_details.append(
                    "The `arguments` field is missing from the `action` object"
                )  # noqa
            if "arguments" in json_message["action"] and not isinstance(
                json_message["action"]["arguments"], dict
            ):  # noqa
                error_details.append("The action's `arguments` field is not an object")
        if len(error_details) > 0:
            raise self._map_to_exception(
                {
                    "error": "MALFORMED PAYLOAD",
                    "error_message": "The response payload is missing required information or contains invalid data",  # noqa
                    "details": error_details,
                    "expected_format": self._response_format,
                    "required_action": "Reformat your entire response to match the expected_format",  # noqa
                }
            )
