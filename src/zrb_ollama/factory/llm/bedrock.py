from langchain_community.llms import Bedrock
from langchain_core.language_models import BaseLanguageModel

from ...bedrock.helper import create_bedrock_client
from ...config import (
    AWS_ACCESS_KEY,
    AWS_REGION_NAME,
    AWS_SECRET_ACCESS_KEY,
    BEDROCK_MODEL,
)
from ...task.any_prompt_task import AnyPromptTask
from ..schema import LLMFactory


def bedrock_llm_factory(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    aws_region_name=AWS_REGION_NAME,
    model_id=BEDROCK_MODEL,
) -> LLMFactory:
    def create_bedrock_llm(task: AnyPromptTask) -> BaseLanguageModel:
        bedrock_client = create_bedrock_client(
            aws_access_key_id=task.render_str(aws_access_key_id),
            aws_secret_access_key=task.render_str(aws_secret_access_key),
            aws_region_name=task.render_str(aws_region_name),
        )
        return Bedrock(
            client=bedrock_client,
            model_id=task.render_str(model_id),
            streaming=True,
            callback_manager=task.get_callback_manager(),
        )

    return create_bedrock_llm
