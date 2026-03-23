# FYP Submission — Security on LLM-Powered Chatbots

This repository contains the code, datasets, experiments, and results for my Final Year Project on **Security on LLM-Powered Chatbots**. The project investigates prompt injection, adversarial prompting, RAG-based data leakage, and evaluates practical defense mechanisms such as guardrails and validation pipelines.

---

## Project Overview

With the increasing accessibility of Large Language Models (LLMs), many developers deploy applications without fully considering security risks. This project proposes a structured red teaming pipeline to evaluate and improve the security of LLM-based systems.

The project covers:

- Adversarial prompt generation using PyRIT
- Controlled experimental validation
- Azure automated red teaming
- Real-world red teaming of student-built chatbots
- RAG-based data leakage testing
- Defense evaluation using guardrails

---

## 📁 Repository Structure

├── initial_datasets/
├── experimental_phase/
├── azure automated red team/
├── red_teaming/
├── requirements.txt
├── readme.md

---

## Initial Datasets

📂 `initial_datasets/`

Contains early prompt injection datasets and baseline results used for:

- identifying attack patterns
- forming adversarial objectives
- seeding the adversarial dataset

### Files

- `ollama_results_*.xlsx`

These represent early experiment outputs from local models and serve as **foundation datasets** for later adversarial prompt construction.

---

## Experimental Phase

📂 `experimental_phase/`

This phase validates the adversarial dataset in controlled environments.

---

### Core Scripts

#### `red_team_experiment.py`

- Executes adversarial prompts against LLMs
- Supports multi-turn prompt execution
- Logs model outputs into Excel

**Main experimental execution pipeline**

---

#### `experiment_validation.py`

- Uses an LLM judge to evaluate outputs
- Compares outputs against `true_description`
- Produces pass/fail results

**Semantic validation layer**

---

#### `percentage.py`

- Computes success rate of adversarial prompts
- Checks if any attack succeeded per row

**Quick evaluation summary**

---

### Azure Results

📂 `experimental_phase/azure_red_team/`

- `red_teamed_azure.xlsx`
- `red_teamed_azure_validated.xlsx`

Results from Azure GPT-4o experiments

---

### Ollama Results

📂 `experimental_phase/ollama_red_team/`

- `red_teamed_ollama.xlsx`
- `red_teamed_ollama_validated.xlsx`

Results from locally hosted models

---

### Defense Evaluation

📂 `experimental_phase/experiment_evaluate/`

#### `guardrail.py`

- Implements input/output guardrails using `llm-guard`
- Includes:
  - PromptInjection detection
  - Sensitive data filtering
  - Toxicity filtering

**Guardrail layer**

---

#### `prompt_dataset.py`

- Runs prompts through guardrails + LLM
- Tracks:
  - blocked inputs
  - blocked outputs
  - successful responses

**Defense evaluation pipeline**

---

#### Other Files

- `guardrail_percentages.xlsx` → summarized results
- `output_results.xlsx` → detailed outputs

---

## Azure Automated Red Teaming

📂 `azure automated red team/`

---

### `adversarial_simulation.ipynb`

- Uses Azure AI RedTeam framework
- Runs automated adversarial simulations
- Generates attack reports

**Automated red teaming via Azure**

---

### `pyrit_redTeam.ipynb`

- Uses PyRIT `RedTeamingOrchestrator`
- Generates adversarial prompts using:
  - objective
  - true_description
- Supports multi-turn attacks

**Core adversarial generation pipeline**

---

### `red_team_output.json`

- Contains structured results:
  - success rates
  - attack categories
  - detailed logs

**Machine-readable output**

---

## Real-World Red Teaming

📂 `red_teaming/`

---

### RAG Experiments

📂 `red_teaming/RAG/`

Files include:

- `rag_prompt.xlsx`
- `rag_prompt_pii.xlsx`
- `rag_result*.xlsx`

Used to test:

- PII leakage
- RAG-based vulnerabilities
- retrieval manipulation

---

### Final Results

📂 `red_teaming/Results/`

- `prompt_injection_final.xlsx`
- `results_raw.xlsx`
- `results_successful.xlsx`

Contains:

- final adversarial dataset
- raw outputs from real systems
- successful exploit cases

---

## Pipeline Overview

The project follows this pipeline:

1. **Dataset Sourcing**
2. **Adversarial Prompt Generation (PyRIT)**
3. **Experimental Validation**
4. **Automated Red Teaming (Azure)**
5. **Real-World Red Teaming**
6. **Defense Evaluation (Guardrails)**

---

## Setup Instructions

### Install dependencies

```bash
pip install -r requirements.txt
```
