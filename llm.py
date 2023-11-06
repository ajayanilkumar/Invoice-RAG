import together
from typing import Any, Dict, List, Mapping, Optional
from pydantic import Extra, Field, root_validator
from langchain.callbacks.manager import CallbackManagerForLLMRun
from langchain.llms.base import LLM
from langchain.utils import get_from_dict_or_env
import os
import logging

os.environ["TOGETHER_API_KEY"] = "ab4b032cd281abfa843ab00815c7c4120594a7bac92fdd97894f5a0c03a80e6b"
together.api_key = os.environ["TOGETHER_API_KEY"]


class TogetherLLM(LLM):
    """Together large language models."""

    model: str = "togethercomputer/llama-2-70b-chat"
    together_api_key: str = os.environ["TOGETHER_API_KEY"]
    temperature: float = 0.7
    max_tokens: int = 512

    class Config:
        extra = Extra.forbid

    @root_validator(allow_reuse=True)
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that the API key is set."""
        api_key = get_from_dict_or_env(
            values, "together_api_key", "TOGETHER_API_KEY"
        )
        values["together_api_key"] = api_key
        return values

    @property
    def _llm_type(self) -> str:
        """Return type of LLM."""
        return "together"

    def _call(self, prompt: str, **kwargs: Any) -> str:
        """Call to Together endpoint."""
        together.api_key = self.together_api_key
        output = together.Complete.create(prompt,
                                          model=self.model,
                                          max_tokens=self.max_tokens,
                                          temperature=self.temperature)
        text = output['output']['choices'][0]['text']
        return text
    
def load_llm(model,temp,max_tokens):
    llm = TogetherLLM(
        model=model,
        temperature=temp,
        max_tokens=max_tokens
    )
    return llm