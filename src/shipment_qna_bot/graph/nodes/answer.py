from typing import Any, Dict

from shipment_qna_bot.logging.graph_tracing import log_node_execution
from shipment_qna_bot.logging.logger import logger, set_log_context
from shipment_qna_bot.tools.azure_openai_chat import AzureOpenAIChatTool

_CHAT_TOOL = None


def _get_chat_tool() -> AzureOpenAIChatTool:
    global _CHAT_TOOL
    if _CHAT_TOOL is None:
        _CHAT_TOOL = AzureOpenAIChatTool()
    return _CHAT_TOOL


def answer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes a natural language answer from retrieved documents using LLM.
    """
    set_log_context(
        conversation_id=state.get("conversation_id", "-"),
        consignee_codes=state.get("consignee_codes", []),
        intent=state.get("intent", "-"),
    )

    with log_node_execution(
        "Answer",
        {
            "intent": state.get("intent", "-"),
            "hits_count": len(state.get("hits") or []),
        },
    ):
        hits = state.get("hits") or []
        analytics = state.get("idx_analytics") or {}
        question = state.get("question_raw") or ""

        # Context construction
        context_str = ""

        # 1. Add Analytics Context
        if analytics:
            count = analytics.get("count")
            facets = analytics.get("facets")
            context_str += f"--- Analytics Data ---\nTotal Matches: {count}\n"
            if facets:
                context_str += f"Facets: {facets}\n"

        # 2. Add Documents Context
        if hits:
            for i, hit in enumerate(hits[:5]):
                context_str += (
                    f"\n--- Document {i+1} ---\n"
                    f"Content: {hit.get('content')}\n"
                    f"Container: {hit.get('container_number')}\n"
                )

        # If no info at all
        if not hits and not analytics:
            state["answer_text"] = (
                "I couldn't find any information matching your request within your authorized scope."
            )
            return state

        # Prompt Construction
        system_prompt = (
            "You are a helpful Shipment Q&A Assistant. "
            "Use the provided retrieved context (analytics and/or documents) to answer the user's question. "
            "If providing analytics, summarize the key figures. "
            "If the answer is not in the context, say you don't know. "
            "Be concise and professional."
        )

        user_prompt = (
            f"Context:\n{context_str}\n\n" f"Question: {question}\n\n" "Answer:"
        )

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        try:
            chat_tool = _get_chat_tool()
            response_text = chat_tool.chat_completion(messages)
            state["answer_text"] = response_text

            logger.info(
                f"Generated answer: {response_text[:100]}...",
                extra={"step": "NODE:Answer"},
            )
        except Exception as e:
            logger.error(f"LLM generation failed: {e}", exc_info=True)
            state["answer_text"] = (
                "I found relevant documents but encountered an error generating the summary. "
                "Please check the evidence logs."
            )
            state.setdefault("errors", []).append(f"LLM Error: {e}")

        return state
