from llm_guard import scan_output, scan_prompt
from llm_guard.input_scanners import PromptInjection
from llm_guard.output_scanners import Relevance, Sensitive, Toxicity

# Determine input and output scanners
input_scanners = [PromptInjection()]
output_scanners = [Relevance(), Sensitive(), Toxicity()]

# Function using LLM-Guard to sanitize inputs
def guardrail_input(prompt):
    sanitized_prompt, results_valid, results_score = scan_prompt(input_scanners, prompt)
    if any(results_valid.values()) is False:
        print(f"Prompt {prompt} is not valid, scores: {results_score}")
        return "eject"

    print(f"Prompt: {sanitized_prompt}")
    return sanitized_prompt

# Function using LLM-Guard to sanitize outputs
def guardrail_output(sanitized_prompt, response_text):
    sanitized_response_text, results_valid, results_score = scan_output(
        output_scanners, sanitized_prompt, response_text
    )
    if not all(results_valid.values()) is True:
        print(f"Rejected output: \"{response_text}\" is not valid, scores: {results_score}\n")
        return "eject"

    print(f"Output: {sanitized_response_text}\n")
    return sanitized_response_text
