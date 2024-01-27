from abc import abstractmethod

from langchain.agents import Agent, AgentExecutor
from langchain.callbacks.manager import CallbackManager
from langchain_core.language_models import BaseLanguageModel
from langchain_core.prompts import BasePromptTemplate
from langchain_core.tools import BaseTool
from zrb import AnyTask
from zrb.helper.typing import List


class AnyPromptTask(AnyTask):
    @abstractmethod
    def get_callback_manager(self) -> CallbackManager:
        pass

    @abstractmethod
    def get_llm(self) -> BaseLanguageModel:
        pass

    @abstractmethod
    def get_prompt(self) -> BasePromptTemplate:
        pass

    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        pass

    @abstractmethod
    def get_agent(self) -> Agent:
        pass

    @abstractmethod
    def get_agent_executor(self) -> AgentExecutor:
        pass

    @abstractmethod
    def get_history_file_name(self) -> str:
        pass
