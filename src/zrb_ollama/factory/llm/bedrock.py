import boto3
from langchain_community.llms import Bedrock
from langchain_core.language_models import BaseLanguageModel

from zrb_ollama.config import AWS_ACCESS_KEY, AWS_SECRET_ACCESS_KEY
from zrb_ollama.factory.schema import LLMFactory
from zrb_ollama.task.any_prompt_task import AnyPromptTask


def bedrock_llm_factory(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region="us-east-1",
    model_id="anthropic.claude-v2",
) -> LLMFactory:
    def create_bedrock_llm(task: AnyPromptTask) -> BaseLanguageModel:
        bedrock_runtime = boto3.client(
            aws_access_key_id=task.render_str(aws_access_key_id),
            aws_secret_access_key=task.render_str(aws_secret_access_key),
            service_name="bedrock-runtime",
            region_name=task.render_str(region),
        )
        return Bedrock(
            client=bedrock_runtime,
            model_id=task.render_str(model_id),
            streaming=True,
            callback_manager=task.get_callback_manager(),
        )

    return create_bedrock_llm
