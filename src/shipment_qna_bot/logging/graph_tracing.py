from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult

from shipment_qna_bot.logging.logger import logger


class GraphTracingCallbackHandler(BaseCallbackHandler):
    """
    Callback handler to log LangGraph/LangChain events.
    """

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> Any:
        logger.info(
            "Graph Node/Chain Started",
            extra={"extra_data": {"inputs": str(inputs)[:500]}},
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> Any:
        logger.info(
            "Graph Node/Chain Ended",
            extra={"extra_data": {"outputs": str(outputs)[:500]}},
        )

    def on_chain_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        logger.error(f"Graph Node/Chain Error: {error}", exc_info=True)

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        logger.info(
            f"Tool Started: {serialized.get('name')}",
            extra={"extra_data": {"input": input_str}},
        )

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        logger.info("Tool Ended", extra={"extra_data": {"output": output[:500]}})

    def on_tool_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        logger.error(f"Tool Error: {error}", exc_info=True)

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        logger.info(
            "LLM Started", extra={"extra_data": {"prompts": [p[:200] for p in prompts]}}
        )

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        logger.info(
            "LLM Ended", extra={"extra_data": {"response": str(response)[:500]}}
        )

    def on_llm_error(
        self, error: Union[Exception, KeyboardInterrupt], **kwargs: Any
    ) -> Any:
        logger.error(f"LLM Error: {error}", exc_info=True)
