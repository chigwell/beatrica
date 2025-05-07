[![PyPI version](https://badge.fury.io/py/beatrica.svg)](https://badge.fury.io/py/beatrica)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/beatrica)](https://pepy.tech/project/beatrica)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# Beatrica

`beatrica` is an innovative Python package that utilizes Large Language Models (LLMs) such as OpenAI's GPT and MistralAI for automating code review processes. It provides insights by analyzing differences between the current active branch and a specified base branch, processing code changes, and generating reviews to improve code quality and collaboration.

## Installation

Integrate cutting-edge code review automation into your workflow by installing `beatrica` using pip:

```bash
pip install beatrica
```

## Configuring the API Key

For Beatrica to communicate with LLM services like OpenAI or MistralAI, an API key is required. You can provide this API key in two ways:

### Using an Environment Variable

Set the API key as an environment variable before running Beatrica. This method is recommended for keeping your API key secure and not directly visible in command line history.

For Unix-like systems (Linux/macOS):

```bash
export LLM_API_KEY='your_api_key_here'
```

For Windows Command Prompt:

```cmd
set LLM_API_KEY=your_api_key_here
```

For Windows PowerShell:

```powershell
$env:LLM_API_KEY='your_api_key_here'
```

After setting the environment variable, you can run Beatrica without explicitly passing the API key in the command:

```bash
beatrica --base_branch=main --llm_type=openai
```

### Using the Command Line Argument

If you prefer or need to, you can directly pass the API key as a command line argument. However, be mindful of security implications such as exposing your API key in shell history or logs.

```bash
beatrica --base_branch=main --llm_type=openai --api_key='your_api_key_here'
```

Choose the method that best suits your workflow and security practices.


## Usage

Beatrica offers a CLI interface for specifying a base branch and comparing its differences with the current active branch, generating insightful reviews. Here are examples showcasing its usage with various configurations:

### Basic Usage

To analyze code differences with the `main` branch using the default OpenAI's GPT-4 model, use:

```bash
beatrica --base_branch=main --llm_type=openai
```

This command compares the current active branch against the `main` branch.

### Specifying LLM Type and Model

For a tailored review, specify the LLM (`openai` or `mistralai`) and model name:

```bash
beatrica --base_branch=main --llm_type=mistralai --model_name=mistral-large-latest
```

### Advanced Configuration

Customize further by specifying the API key (from an environment variable or directly), the maximum tokens for the LLM response, and the output format:

```bash
beatrica --base_branch=develop --llm_type=openai --model_name=gpt-4-0125-preview --api_key=YOUR_API_KEY --max_tokens=1000 --output=beatrica_review.txt
```

## Example Output

An example output of Beatrica reviewing changes between the current active branch and the `main` branch is:

```
Analyzing differences with base branch main using OpenAI GPT-4-0125-preview...
Tracking changes...
✅  Changes tracked.
✅  Found 2 changes.
Initializing language model...
Generating code embeddings...
✅  Embeddings generated.
Checking if Beatrica can review the changes...
✅ 1 changes found for review.
Starting the review process...
Reviewing changes ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:34
✅  Review process completed.
Aggregating reviews...
Aggregating reviews ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100% 0:00:20
✅  Reviews aggregated.
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Commit ID                                ┃ Change Description                                              ┃ Review                                             ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ e08642828750dc15786c1166898fe30fa500c17c │ Added comment for test_generate_crsid_with_empty_first function │ The commit message "add comment for                │
│                                          │                                                                 │ test_generate_crsid_with_empty_first" could be     │
│                                          │                                                                 │ more descriptive to convey the purpose and         │
│                                          │                                                                 │ importance of the added comment. A suggestion for  │
│                                          │                                                                 │ a more informative commit message is "Explain test │
│                                          │                                                                 │ purpose for CRSID generation with empty first name │
│                                          │                                                                 │ in comments". This provides clear context on the   │
│                                          │                                                                 │ change's significance. While adding a comment to   │
│                                          │                                                                 │ the test function is a step in the right direction │
│                                          │                                                                 │ for code clarity, the comment itself could be more │
│                                          │                                                                 │ descriptive. It should explain not just what is    │
│                                          │                                                                 │ being tested (generate_crsid with an empty first   │
│                                          │                                                                 │ name), but also the expected outcome or behavior   │
│                                          │                                                                 │ of the function under this condition. This would   │
│                                          │                                                                 │ help in understanding the test's intention without │
│                                          │                                                                 │ diving into the implementation details. The test   │
│                                          │                                                                 │ function "test_generate_crsid_with_empty_first()"  │
│                                          │                                                                 │ could have a more descriptive name that reflects   │
│                                          │                                                                 │ the expected behavior or outcome of the test, such │
│                                          │                                                                 │ as                                                 │
│                                          │                                                                 │ "test_crsid_generation_fails_with_empty_first_nam… │
│                                          │                                                                 │ or                                                 │
│                                          │                                                                 │ "test_crsid_generation_handles_empty_first_name_g… │
│                                          │                                                                 │ depending on the expected behavior. This makes it  │
│                                          │                                                                 │ easier to understand the test's purpose at a       │
│                                          │                                                                 │ glance. It is recommended to include input         │
│                                          │                                                                 │ validation in the generate_crsid function to       │
│                                          │                                                                 │ ensure that the arguments passed (first_name and   │
│                                          │                                                                 │ last_name) are strings. This would prevent         │
│                                          │                                                                 │ potential runtime errors and make the function     │
│                                          │                                                                 │ more robust against incorrect usage. Considering   │
│                                          │                                                                 │ the importance of ensuring uniqueness in CRSID     │
│                                          │                                                                 │ generation, the function should include a          │
│                                          │                                                                 │ mechanism to handle scenarios where uniqueness     │
│                                          │                                                                 │ cannot be guaranteed. This could be due to         │
│                                          │                                                                 │ multiple individuals sharing the same first and    │
│                                          │                                                                 │ last names. Implementing a strategy to handle such │
│                                          │                                                                 │ cases gracefully would improve the function's      │
│                                          │                                                                 │ reliability. Adding additional test cases to cover │
│                                          │                                                                 │ edge scenarios, such as both first and last names  │
│                                          │                                                                 │ being empty or containing special characters or    │
│                                          │                                                                 │ numbers, would enhance the test suite's            │
│                                          │                                                                 │ comprehensiveness. This ensures that the function  │
│                                          │                                                                 │ behaves as expected under various inputs.          │
└──────────────────────────────────────────┴─────────────────────────────────────────────────────────────────┴────────────────────────────────────────────────────┘
```

## Features

- Analyzes differences between the current active branch and a specified base branch.
- Integration with major LLMs for code review: OpenAI and MistralAI.
- Customizable for different base branches, LLMs, and output formats.
- Simplified CLI for ease of use.

## Contributing

Contributions, issues, and

 feature requests are welcome. For more information, check our [issues page](https://github.com/chigwell/beatrica/issues).

## License

`beatrica` is made available under the [GNU AFFERO GENERAL PUBLIC LICENSE](LICENSE).
