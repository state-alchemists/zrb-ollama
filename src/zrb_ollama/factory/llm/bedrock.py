from typing import Any, Dict, Iterator, List, Mapping, Optional
from langchain_community.llms import Bedrock
from langchain_core.language_models import BaseLanguageModel
from langchain_core.outputs import GenerationChunk
from langchain_core.callbacks import CallbackManagerForLLMRun

from ...bedrock.helper import create_bedrock_client
from ...config import (
    AWS_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    AWS_SECRET_ACCESS_KEY,
    AWS_BEDROCK_MODEL_ID,
)
from ...task.any_prompt_task import AnyPromptTask
from ..schema import LLMFactory


class BedrockHack(Bedrock):
    def _prepare_input_and_invoke_stream(
        self,
        prompt: Optional[str] = None,
        system: Optional[str] = None,
        messages: Optional[List[Dict]] = None,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> Iterator[GenerationChunk]:
        provider = self._get_provider()
        # In our experiment, mistral doesn't accept stop_sequence
        if provider == "mistral":
            stop = None
        return super()._prepare_input_and_invoke_stream(
            prompt=prompt,
            system=system,
            messages=messages,
            stop=stop,
            run_manager=run_manager,
            **kwargs
        )


def bedrock_llm_factory(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_region_name=AWS_DEFAULT_REGION,
    model_id=AWS_BEDROCK_MODEL_ID,
    model_kwargs: Optional[Dict] = None,
    credentials_profile_name: Optional[str] = None,
    config: Any = None,
    provider: Optional[str] = None,
    provider_stop_sequence_key_name_map: Mapping[str, str] = {
        "anthropic": "stop_sequences",
        "amazon": "stopSequences",
        "ai21": "stop_sequences",
        "cohere": "stop_sequences",
        "mistral": "stop_sequences",
    },
    guardrails: Optional[Mapping[str, Any]] = {
        "id": None,
        "version": None,
        "trace": False,
    }
) -> LLMFactory:
    def create_bedrock_llm(task: AnyPromptTask) -> BaseLanguageModel:
        bedrock_client = create_bedrock_client(
            aws_access_key_id=task.render_str(aws_access_key_id),
            aws_secret_access_key=task.render_str(aws_secret_access_key),
            aws_region_name=task.render_str(aws_region_name),
        )
        return BedrockHack(
            client=bedrock_client,
            region_name=aws_region_name,
            model_id=task.render_str(model_id),
            model_kwargs=model_kwargs,
            credentials_profile_name=credentials_profile_name,
            config=config,
            provider=provider,
            provider_stop_sequence_key_name_map=provider_stop_sequence_key_name_map,
            guardrails=guardrails,
            streaming=True,
            callback_manager=task.get_callback_manager(),
        )

    return create_bedrock_llm
