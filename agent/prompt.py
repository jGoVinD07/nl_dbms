def build_prompt(question, context, tables):
    """
    Build the prompt sent to the LLM.
    To change prompting strategy (few-shot, chain-of-thought etc),
    modify this function.
    """
    tables_text = "\n".join(tables)

    return f"""
Database Context:

{context}

Existing Tables:

{tables_text}

You are a PostgreSQL Expert.

Rules:

1. Generate VALID PostgreSQL SQL.
2. Return ONLY SQL.
3. No markdown.
4. No explanation.
5. Never create existing tables.
6. Every CREATE TABLE must contain:
   id SERIAL PRIMARY KEY
7. Never generate incomplete SQL.
8. Generate executable PostgreSQL.
9. If user creates a table without columns,
   generate reasonable columns.

User Request:

{question}
"""
