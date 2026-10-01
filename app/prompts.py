SUMMARY_PROMPT = """You are a meeting intelligence assistant.
Summarize this transcript chunk faithfully. Preserve decisions, commitments, disagreements,
dates, owners and risks. Do not invent facts. Keep speaker names when relevant.

TRANSCRIPT CHUNK:
{chunk}"""

MERGE_PROMPT = """Combine the chunk summaries into one concise executive meeting summary.
Remove repetition. Preserve outcomes, decisions, unresolved issues, owners and deadlines.
Do not invent information.

CHUNK SUMMARIES:
{summaries}"""

DECISIONS_PROMPT = """Extract key decisions actually supported by the transcript.
Use the speaker who stated or owned each decision. Do not invent decisions.

TRANSCRIPT:
{transcript}"""

ACTIONS_PROMPT = """Extract concrete action items actually supported by the transcript.
Identify owner and deadline only when stated; otherwise use null.

TRANSCRIPT:
{transcript}"""

RISKS_PROMPT = """Extract concrete risks and unresolved concerns. Assign severity only from
low, medium, high, critical based on the described impact. Do not invent risks.

TRANSCRIPT:
{transcript}"""

TOPICS_PROMPT = """Group the meeting into coherent topic clusters. Include relevant speakers
when they can be identified. Do not invent topics.

TRANSCRIPT:
{transcript}"""
