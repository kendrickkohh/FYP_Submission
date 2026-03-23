import os
import ast
import json
import pandas as pd
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from guardrail import guardrail_input, guardrail_output

load_dotenv()

template = """
You are a helpful assistant. Answer the user's questions to the best of your ability.

User question:
{question}
"""


def build_model():
    return AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_NTU_ENDPOINT_4o"),
        api_key=os.getenv("AZURE_OPENAI_NTU_API_KEY_4o"),
        api_version=os.getenv("AZURE_OPENAI_NTU_API_VERSION_4o"),
        deployment_name=os.getenv("AZURE_OPENAI_NTU_DEPLOYMENT_NAME_4o"),
    )


def parse_prompt_array(cell_value):
    """
    Parses the prompt column which contains a string representation of a list.
    Example:
    '["prompt 1", "prompt 2", "prompt 3"]'
    """
    if pd.isna(cell_value):
        return []

    if isinstance(cell_value, list):
        return cell_value

    if isinstance(cell_value, str):
        text = cell_value.strip()

        # Try JSON first
        try:
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass

        # Fallback to Python literal parsing
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                return parsed
        except Exception:
            pass

    return []


def query_rag(model, query_text: str):
    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.format(question=query_text)
    response = model.invoke(prompt)
    return response.content


def process_excel(input_file: str, output_file: str, prompt_column: str = "prompt"):
    df = pd.read_excel(input_file)

    if prompt_column not in df.columns:
        raise ValueError(f"Column '{prompt_column}' not found in Excel file.")

    model = build_model()
    results = []

    for row_idx, row in df.iterrows():
        prompt_list = parse_prompt_array(row[prompt_column])

        if not prompt_list:
            results.append({
                "row_index": row_idx,
                "prompt_index": None,
                "original_prompt": None,
                "sanitized_prompt": None,
                "input_guardrail_status": "invalid_or_empty_prompt_array",
                "raw_response": None,
                "sanitized_response": None,
                "output_guardrail_status": None,
                "final_status": "skipped"
            })
            continue

        row_blocked = False

        for prompt_idx, prompt_text in enumerate(prompt_list):
            if row_blocked:
                break

            try:
                print(f"Processing row {row_idx}, prompt {prompt_idx}...")

                sanitized_prompt = guardrail_input(prompt_text)

                if sanitized_prompt == "eject":
                    results.append({
                        "row_index": row_idx,
                        "prompt_index": prompt_idx,
                        "original_prompt": prompt_text,
                        "sanitized_prompt": None,
                        "input_guardrail_status": "blocked",
                        "raw_response": None,
                        "sanitized_response": None,
                        "output_guardrail_status": None,
                        "final_status": "skipped_next_row"
                    })
                    row_blocked = True
                    continue

                response_text = query_rag(model, sanitized_prompt)

                sanitized_response = guardrail_output(sanitized_prompt, response_text)

                if sanitized_response == "eject":
                    results.append({
                        "row_index": row_idx,
                        "prompt_index": prompt_idx,
                        "original_prompt": prompt_text,
                        "sanitized_prompt": sanitized_prompt,
                        "input_guardrail_status": "passed",
                        "raw_response": response_text,
                        "sanitized_response": None,
                        "output_guardrail_status": "blocked",
                        "final_status": "skipped_next_row"
                    })
                    row_blocked = True
                    continue

                results.append({
                    "row_index": row_idx,
                    "prompt_index": prompt_idx,
                    "original_prompt": prompt_text,
                    "sanitized_prompt": sanitized_prompt,
                    "input_guardrail_status": "passed",
                    "raw_response": response_text,
                    "sanitized_response": sanitized_response,
                    "output_guardrail_status": "passed",
                    "final_status": "completed"
                })

            except Exception as e:
                results.append({
                    "row_index": row_idx,
                    "prompt_index": prompt_idx,
                    "original_prompt": prompt_text,
                    "sanitized_prompt": None,
                    "input_guardrail_status": "error",
                    "raw_response": None,
                    "sanitized_response": None,
                    "output_guardrail_status": None,
                    "final_status": f"error: {str(e)}"
                })
                row_blocked = True

    results_df = pd.DataFrame(results)
    results_df.to_excel(output_file, index=False)
    print(f"\nDone. Results saved to: {output_file}")


if __name__ == "__main__":
    input_file = r"prompt_injection_final.xlsx"
    output_file = r"output_results.xlsx"
    process_excel(input_file, output_file, prompt_column="prompt")