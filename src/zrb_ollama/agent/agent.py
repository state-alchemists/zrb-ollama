import json
import os
import re
import time
import traceback
from collections.abc import Callable, Mapping
from datetime import date
from typing import Annotated, Any, Optional

import json_repair
import litellm
from zrb.helper.callable import run_async
from zrb.helper.typecheck import typechecked

from ..config import (
    DEFAULT_JSON_FIXER_SYSTEM_MESSAGE_TEMPLATE,
    DEFAULT_JSON_FIXER_SYSTEM_PROMPT,
    DEFAULT_SYSTEM_MESSAGE_TEMPLATE,
    DEFAULT_SYSTEM_PROMPT,
    LLM_MODEL,
    SHOULD_SHOW_SYSTEM_PROMPT
)
from ._helper import extract_metadata, get_metadata_description, get_metadata_signature


@typechecked
class Agent:

    def __init__(
        self,
        model: Optional[str] = None,
        system_message_template: Optional[str] = None,
        system_prompt: Optional[str] = None,
        json_fixer_system_message_template: Optional[str] = None,
        json_fixer_system_prompt: Optional[str] = None,
        previous_messages: Optional[list[Any]] = [],
        tools: list[Callable] = [],
        max_iteration: int = 10,
        should_show_system_prompt: bool = SHOULD_SHOW_SYSTEM_PROMPT,
        should_show_history: bool = False,
        conversation_log_path: Optional[str] = None,
        print_fn: Optional[Callable[[str], Any]] = None,
        **kwargs: Mapping[str, Any],
    ):
        def finish_conversation(
            final_answer: Annotated[
                str, "Final answer containing all necessary information and citations"
            ]  # noqa
        ) -> str:
            """Ends up conversation with user by providing the final_answer. The final_answer should contains all detailed information and citations."""  # noqa
            self._finished = True
            return final_answer
        if model is None:
            model = LLM_MODEL
        if system_message_template is None:
            system_message_template = DEFAULT_SYSTEM_MESSAGE_TEMPLATE
        if system_prompt is None:
            system_prompt = DEFAULT_SYSTEM_PROMPT
        if json_fixer_system_message_template is None:
            json_fixer_system_message_template = DEFAULT_JSON_FIXER_SYSTEM_MESSAGE_TEMPLATE  # noqa
        if json_fixer_system_prompt is None:
            json_fixer_system_prompt = DEFAULT_JSON_FIXER_SYSTEM_PROMPT
        if previous_messages is None:
            previous_messages = []
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
        formatted_function_description = {
            fn_name: "   \n".join(get_metadata_description(metadata).split("\n"))
            for fn_name, metadata in self._function_schemas.items()
        }
        self._function_md_signature_str = "\n".join(
            [
                f"- {signature}\n  {formatted_function_description[fn_name]}"
                for fn_name, signature in self._function_signatures.items()
            ]
        )
        self._function_names = [key for key in self._function_schemas]
        self._function_map = {fn.__name__: fn for fn in self._tools}
        function_names_str = ", ".join([f"`{key}`" for key in self._function_names])
        self._response_format = {
            "thought": "<your plan and reasoning to choose an action>",
            "function": f"<function name, SHOULD STRICTLY be one of these: {function_names_str}>",  # noqa
            "arguments": {
                "<argument-1>": "<value-1>",
                "<argument-2>": "<value-2>",
            },
        }
        self._system_message = self._build_system_message(
            system_message_template, system_prompt
        )
        self._json_fixer_system_message = self._build_system_message(
            json_fixer_system_message_template, json_fixer_system_prompt
        )
        self._previous_messages = previous_messages
        self._finished = False

    def _build_system_message(self, template: str, prompt: str) -> Mapping[str, Any]:
        return {
            "role": "system",
            "content": template.format(
                system_prompt=prompt,
                response_format=json.dumps(self._response_format),
                function_names=", ".join(self._function_names),
                function_signatures=self._function_md_signature_str,
                function_schemas=json.dumps(self._function_schemas, indent=2),
            ),
        }

    def get_system_message(self) -> Any:
        return self._system_message

    def get_previous_messages(self) -> list[Any]:
        return self._previous_messages

    def get_messages(self) -> list[Any]:
        return [
            self._system_message,
            {"role": "user", "content": "Hi"},
            {
                "role": "assistant",
                "content": json.dumps(
                    {
                        "thought": "User has greet me, I should say hi.",
                        "function": "finish_conversation",
                        "arguments": {
                            "final_answer": "Hi, I'm a useful assistant, I'm ready to help."  # noqa
                        },
                    }
                ),
            },
        ] + self._previous_messages

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
            response_content = response.choices[0].message.content
            self._print(f"🤖 LLM Response ({elapsed:.2f} seconds): {response_content}")
            response_map = None
            try:
                response_map = await self._extract_agent_message_with_llm(
                    user_message, response_content
                )
                self._append_agent_message(json.dumps(response_map))
            except Exception as exc:
                self._print(f"🛑 Error: {exc}")
                traceback.print_exc()
                if response_map is not None:
                    self._append_agent_message(response_map)
                else:
                    self._append_agent_message(response_content)
                self._append_format_error(user_message, exc)
                continue
            self._print(f"🥝 Extracted Response: {response_map}")
            function_name = response_map.get("function", "")
            function_kwargs = response_map.get("arguments", {})
            result = None
            try:
                self._validate_function_call(function_name, function_kwargs)
                start = time.time()
                result = await self._execute_function(function_name, function_kwargs)
                end = time.time()
                elapsed = end - start
                if self._finished:
                    self._print(f"✅ Final Result ({elapsed:.2f} seconds)")
                else:
                    self._print(f"✅ Result ({elapsed:.2f} seconds): {result}")
                self._append_function_call_ok(
                    user_message, function_name, function_kwargs, result
                )
            except Exception as exc:
                self._print(f"🛑 Error: {exc}")
                traceback.print_exc()
                self._append_function_call_error(
                    user_message, function_name, function_kwargs, exc
                )
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
        self._write_conversation_log(f"User: {user_message}")

    def _append_agent_message(self, assistant_message: str):
        self._append_message({"role": "assistant", "content": assistant_message})
        self._write_conversation_log(f"Assistant: {assistant_message}")

    def _append_format_error(self, user_message: str, exc: Exception):
        self._append_message(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "type": "format_error",
                        "details": "Assistant response is unparseable.",
                        "error": self._extract_exception(exc),
                        "original_user_message": user_message,
                    }
                ),
            }
        )
        self._write_conversation_log("[ERROR] Invalid message")

    def _append_function_call_error(
        self, user_message: str, function: str, arguments: list[str], exc: Exception
    ):
        self._append_message(
            {
                "role": "user",
                "content": json.dumps(
                    {
                        "type": "function_call_error",
                        "details": "Assistant function call is incorrect.",
                        "function": function,
                        "arguments": arguments,
                        "error": self._extract_exception(exc),
                        "original_user_message": user_message,
                    }
                ),
            }
        )
        self._write_conversation_log("[ERROR] Function call error")

    def _append_function_call_ok(
        self, user_message: str, function_name: str, arguments: list[str], result: Any
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
                        "original_user_message": user_message,
                    }
                ),
            }
        )
        self._write_conversation_log(f"[SUCCESS] {result}")

    def _append_message(self, message: Any):
        self._previous_messages.append(message)

    def _write_conversation_log(self, message: str):
        if self._conversation_log_path is None:
            return
        conversation_log_path = os.path.expanduser(self._conversation_log_path)
        if not os.path.isdir(conversation_log_path):
            os.makedirs(conversation_log_path)
        current_date = date.today()
        formatted_date = current_date.strftime('%Y-%m-%d')
        file_name = os.path.join(conversation_log_path, f"{formatted_date}.txt")
        with open(file_name, "a") as file:
            file.write(f"{message}\n")

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

    async def _extract_agent_message_with_llm(
        self, user_message, response_content
    ) -> Mapping[str, Any]:
        try:
            response_map = self._extract_agent_message(response_content)
            return response_map
        except Exception:
            start = time.time()
            self._print("🛑 Trying to create a valid JSON by using LLM...")
            response = await litellm.acompletion(
                model=self._model,
                messages=[
                    self._json_fixer_system_message,
                    {
                        "role": "user",
                        "content": "\n".join(
                            [
                                "Original query from human:",
                                user_message,
                                "Fix the following LLM message:",
                                response_content,
                            ]
                        ),
                    },
                ],
            )
            end = time.time()
            elapsed = end - start
            revised_content = response.choices[0].message.content
            self._print(f"Revised content ({elapsed:.2f}): {revised_content}")
            return self._extract_agent_message(revised_content)

    def _extract_agent_message(self, response_content) -> Mapping[str, Any]:
        try:
            response_map = self._json_loads(response_content)
            self._validate_agent_message(response_map)
            return response_map
        except Exception:
            self._print("🛑 Trying to determine JSON by using code delimiters...")
            json_pattern = re.compile(r"```(json)?\n({.*?})\n```", re.DOTALL)
            # Search for the pattern in the content
            match = json_pattern.search(response_content)
            if match:
                json_str = match.group(2)
                # Parse the JSON string to ensure it is valid
                try:
                    response_map = self._json_loads(json_str)
                    self._validate_agent_message(response_map)
                    return response_map
                except Exception as e:
                    self._print(f"🛑 Failed: {e}")
            else:
                self._print("🛑 Failed: Not found")
            # The seemingly working way
            self._print("🛑 Trying to determine JSON by using matching braces...")
            json_start, json_end = self._get_json_start_and_end(response_content)
            if json_start != -1 and json_end != -1:
                json_str = response_content[json_start:json_end]
                # Parse the JSON string to ensure it is valid
                try:
                    response_map = self._json_loads(json_str)
                    self._validate_agent_message(response_map)
                    return response_map
                except Exception as e:
                    self._print(f"🛑 Failed: {e}")
            else:
                self._print("🛑 Failed: Not found")
            raise self._map_to_exception(
                {
                    "error": "MALFORMED RESPONSE",
                    "error_message": "Your response is not a valid JSON",
                    "expected_format": self._response_format,
                    "required_action": "Reformat your entire response to match the expected_format",  # noqa
                }
            )

    def _get_json_start_and_end(self, response_content: str) -> tuple[int, int]:
        brace_stack = []
        json_start, json_end = -1, -1
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
        return json_start, json_end

    def _json_loads(self, json_str: str) -> Any:
        return json_repair.loads(json_str)

    def _validate_agent_message(self, json_message: Mapping[str, Any]):
        error_details = []
        if "thought" not in json_message:
            error_details.append("The `thought` field is missing")
        if "thought" in json_message and not isinstance(json_message["thought"], str):
            error_details.append("The `thought` field is not a string")
        if "function" not in json_message:
            error_details.append("The `function` field is missing")
        if "function" in json_message and not isinstance(json_message["function"], str):
            error_details.append("The `function` field is not a string")
        if "arguments" not in json_message:
            error_details.append("The `arguments` field is missing")
        if "arguments" in json_message and not isinstance(
            json_message["arguments"], dict
        ):
            error_details.append("The `arguments` field is not an object")
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
