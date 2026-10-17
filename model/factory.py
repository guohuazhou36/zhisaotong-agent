import os
from abc import ABC, abstractmethod
from typing import Optional

from dotenv import load_dotenv
from langchain_community.chat_models.tongyi import BaseChatModel, ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.embeddings import Embeddings

from utils.config_handler import rag_conf

load_dotenv()


def _require_dashscope_key() -> str:
    key = (os.getenv("DASHSCOPE_API_KEY") or "").strip()
    if not key:
        raise ValueError(
            "缺少 DASHSCOPE_API_KEY：请在 Streamlit Secrets 或本地 .env 中配置。"
        )
    return key


class BaseModelFactory(ABC):
    @abstractmethod
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        pass


class ChatModelFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return ChatTongyi(
            model=rag_conf["chat_model_name"],
            dashscope_api_key=_require_dashscope_key(),
        )


class EmbeddingsFactory(BaseModelFactory):
    def generator(self) -> Optional[Embeddings | BaseChatModel]:
        return DashScopeEmbeddings(
            model=rag_conf["embedding_model_name"],
            dashscope_api_key=_require_dashscope_key(),
        )


chat_model = ChatModelFactory().generator()
embed_model = EmbeddingsFactory().generator()
