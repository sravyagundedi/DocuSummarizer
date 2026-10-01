# Prompt Documentation

The brief specifies separate prompts for chunk summaries, global merge, decisions, actions, risks and topics.

Design rules:
- factual extraction only
- no invented details
- preserve speaker attribution
- owner/deadline may be null
- controlled risk severity
- Pydantic format instructions
- retry after parse failure

The implementation does not request hidden chain-of-thought; it requests concise, verifiable outputs instead.
