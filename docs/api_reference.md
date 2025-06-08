# API Reference

## readme_improver.improver.load_config

Load configuration values from a YAML file.

| Name | Type | Description |
| --- | --- | --- |
| `path` | `str` | Path to the configuration file |

Returns: `dict` parsed configuration or empty dict.

## readme_improver.improver.build_prompt

Construct the prompt for the rewrite request.

| Name | Type | Description |
| --- | --- | --- |
| `readme_text` | `str` | Current README contents |
| `config` | `dict` | Configuration values controlling extra sections and branding |

Returns: `str` formatted prompt.

## readme_improver.improver.generate_summary

Generate a TL;DR summary of the README.

| Name | Type | Description |
| --- | --- | --- |
| `readme_text` | `str` | README content to summarize |
| `model` | `str` | OpenAI model name |
| `prompt_prefix` | `Optional[str]` | Custom prompt prefix |

Returns: `str` summary.

## readme_improver.improver.suggest_improvements

Provide improvement suggestions for the README.

| Name | Type | Description |
| --- | --- | --- |
| `readme_text` | `str` | README content to analyze |
| `model` | `str` | OpenAI model name |
| `prompt_prefix` | `Optional[str]` | Optional prompt prefix |

Returns: `str` suggestions.

## readme_improver.improver.rewrite_readme

Rewrite the README using OpenAI.

| Name | Type | Description |
| --- | --- | --- |
| `readme_text` | `str` | Source README text |
| `model` | `str` | OpenAI model name |
| `prompt_prefix` | `Optional[str]` | Custom prompt prefix |
| `config` | `Optional[dict]` | Configuration for custom sections |

Returns: `str` rewritten README content.

## readme_improver.logger.get_logger

Return a configured logger writing to file and console.

Returns: `logging.Logger` instance.

## readme_improver.openai_helper._get_client

Create the OpenAI client lazily.

Returns: `OpenAI` client instance.

## readme_improver.openai_helper._estimate_cost

Estimate API cost for a given model and token count.

| Name | Type | Description |
| --- | --- | --- |
| `model` | `str` | Model name used for the request |
| `total_tokens` | `int` | Total tokens consumed |

Returns: `float` cost in USD.

## readme_improver.openai_helper.ask_openai

Send a prompt to OpenAI ChatCompletion with caching and detailed logging.

| Name | Type | Description |
| --- | --- | --- |
| `prompt` | `str` | Prompt text |
| `model` | `str` | Model name |
| `temperature` | `float` | Sampling temperature |
| `max_tokens` | `int` | Maximum tokens in the reply |

Returns: `str` response from the API.

## readme_improver.readme_loader.load_readme

Load the contents of a README file.

| Name | Type | Description |
| --- | --- | --- |
| `path` | `str` | Path to the README file |

Returns: `str` file content (empty string if missing).

## readme_improver.post_comment.get_pr_number

Extract the pull request number from the GitHub event payload.

Returns: `str` PR number.

## readme_improver.post_comment.main

Post README improvement suggestions as a PR comment.

## main.main

Run the CLI.
