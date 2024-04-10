import argparse
import os
import re
from beatrica_git.recent_change_inspector import BeatricaDiffTracker
from beatrica_embedding.embedding_generator import BeatricaCodeChangeProcessor
from langchain_openai import ChatOpenAI
from langchain_mistralai.chat_models import ChatMistralAI
from .prompts import prompts
from rich.console import Console
from rich.table import Table
from rich.progress import track


LLM_CHOICES = ['openai', 'mistralai']
BASE_BRANCH = "main"
OPENAI_DEFAULT_MODEL = "gpt-4-0125-preview"
MISTRAL_DEFAULT_MODEL = "mistral-large-latest"
MAX_TOKENS = 500
OUTPUT_FILE = "beatrica_review.txt"
LLM_API_KEY = os.getenv("LLM_API_KEY")


def main():
    parser = argparse.ArgumentParser(description='Beatrica CLI for analyzing code changes.')
    parser.add_argument('--base_branch', type=str, default=BASE_BRANCH, help='The base branch to compare.')
    parser.add_argument('--llm_type', type=str, choices=LLM_CHOICES, default="openai", help='Type of LLM to use.')
    parser.add_argument('--model_name', type=str, help='Model name for the LLM.', default="")
    parser.add_argument('--api_key', type=str, help='API key for the LLM.', default=LLM_API_KEY)
    parser.add_argument('--max_tokens', type=int, default=MAX_TOKENS, help='Maximum number of tokens for the LLM response.')
    parser.add_argument('--output', type=str, default="console", help='Output type for the review.')

    args = parser.parse_args()

    review(args.base_branch, args.llm_type, args.model_name, args.api_key, args.max_tokens, args.output)

def review(
        base_branch=BASE_BRANCH,
        llm_type="openai",
        model_name="",
        api_key=None,
        max_tokens=MAX_TOKENS,
        output=""
    ):
    if llm_type == "openai" and model_name == "":
        model_name = OPENAI_DEFAULT_MODEL
    elif llm_type == "mistralai" and model_name == "":
        model_name = MISTRAL_DEFAULT_MODEL

    console = Console()
    console.print(
        f"[bold blue]Analyzing changes[/] in branch [bold green]{base_branch}[/] with [bold yellow]{llm_type} {model_name}...")
    console.print("[bold blue]Tracking changes...[/]")
    beatrica_diff_tracker = BeatricaDiffTracker(base_branch=base_branch)

    beatrica_diff_tracker.analyze_commits()

    commit_changes = beatrica_diff_tracker.commit_changes.items()
    if len(commit_changes) == 0:
        console.print("[bold red] No changes found. Exiting.[/]")
        exit(0)
    console.print("[bold green]✅  Changes tracked.[/]")
    console.print(f"[bold blue]✅  Found[/] [bold magenta]{len(commit_changes)}[/] change(s).")

    console.print("[bold blue]Initializing language model...[/]")

    if llm_type == "openai":
        language_model = ChatOpenAI(model_name=model_name, api_key=api_key, max_tokens=max_tokens)
    elif llm_type == "mistralai":
        language_model = ChatMistralAI(model=model_name, mistral_api_key=api_key, max_tokens=max_tokens)
    else:
        raise ValueError("Unsupported LLM type.")
    console.print("[bold blue]Generating code embeddings...[/]")

    code_change_processor = BeatricaCodeChangeProcessor(commit_changes, language_model=language_model)
    retrieval_chain = code_change_processor.process()

    console.print("[bold green]✅  Embeddings generated.[/]")

    console.print("[bold blue]Checking if Beatrica can review the changes...[/]")

    question = prompts['get_changes']['question'] + "\n" + prompts['get_changes']['expected_answer']
    result = retrieval_chain.invoke(question)
    answer = result['answer']

    pattern = prompts['get_changes']['expected_pattern']
    matches = re.findall(pattern, answer, re.DOTALL)
    for match in matches:
        commit_id, change_desc = match
        if commit_id.startswith("commit_hash") or change_desc.startswith("commit\_hash"):
            matches.remove(match)
    if len(matches) == 0:
        console.print(f"⚠️ Beatrica with {llm_type} {model_name} cannot make a review. "
                      f"This is likely due to the changes being too small or not code changes. "
                      f"Please try again with a different branch or more changes.")
        exit(0)


    console.print(f"[bold green]✅ {len(matches)}[/] change(s) found for review.")

    console.print("[bold blue]Starting the review process...[/]")

    reviews = []
    for match in track(matches, description="Reviewing changes"):
        question = prompts['can_review']['question'] + match[0] + ": " + match[1] + "\n" + prompts['can_review']['expected_answer']
        result = retrieval_chain.invoke(question)
        answer = result['answer']
        pattern = prompts['can_review']['expected_pattern']
        can_review = re.findall(pattern, answer, re.DOTALL)

        if len(can_review) == 0:
            continue
        can_review = can_review[0]
        try:
            if int(can_review) == 1:
                question = prompts['make_review']['question'] + match[0] + ": " + match[1] + "\n" + prompts['make_review']['expected_answer']
                result = retrieval_chain.invoke(question)
                answer = result['answer']
                pattern = prompts['make_review']['expected_pattern']
                review_points = re.findall(pattern, answer, re.DOTALL)
                for review_point in review_points:
                    reviews.append({
                        "change": match,
                        "review": review_point
                    })
        except ValueError:
            continue
    console.print("[bold green]✅  Review process completed.[/]")

    console.print("[bold blue]Aggregating reviews...[/]")
    aggregated_reviews = {}
    for review in reviews:
        commit_id, change_desc = review['change']
        review_text = review['review']
        key = (commit_id, change_desc)
        if key not in aggregated_reviews:
            aggregated_reviews[key] = []
        aggregated_reviews[key].append(review_text)

    for key, review_texts in track(aggregated_reviews.items(), description="Aggregating reviews"):
        review_points = ""
        for review_text in review_texts:
            review_points += f"\n{review_text}"
        question = prompts['aggregate_review_points']['question'] + review_points + "\n" + prompts['aggregate_review_points']['expected_answer']
        result = retrieval_chain.invoke(question)
        answer = result['answer']
        pattern = prompts['aggregate_review_points']['expected_pattern']
        aggregated_review = re.findall(pattern, answer, re.DOTALL)
        if len(aggregated_review) == 0:
            continue
        aggregated_review = aggregated_review[0]
        aggregated_reviews[key] = aggregated_review

    console.print("[bold green]✅  Reviews aggregated.[/]")

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Commit ID", style="dim", overflow="fold", min_width=20, width=20, max_width=50)
    table.add_column("Change Description", style="cyan", no_wrap=True)
    table.add_column("Review", style="green", width=50, min_width=50)

    table_file = []
    for (commit_id, change_description), reviews in aggregated_reviews.items():
        if commit_id is None or commit_id == "":
            commit_id = "N/A"
        change_description = re.sub('<[^<]+?>', '', change_description)
        change_description = change_description.lstrip()

        reviews_display = " ".join(reviews) if isinstance(reviews, list) else reviews
        reviews_display = reviews_display.lstrip()

        table.add_row(commit_id, change_description, reviews_display)
        table_file.append((commit_id, change_description, reviews_display))

    if output == "console":
        if len(table_file) == 0:
            print(aggregated_reviews)
            console.print("[bold geen]No comments in the review[/]")
        else:
            console.print(table)
    else:
        if output == "":
            save_file = os.getcwd() + OUTPUT_FILE
        else:
            save_file = output

        if not os.path.exists(save_file):
            with open(save_file, "w") as f:
                f.write("Commit ID,Change Description,Review\n")
        for row in table_file:
            row_file = str(row)
            with open(save_file, "a") as f:
                f.write(row_file)

        console.print(f"[bold green]✅  Reviews saved to {save_file}[/]")

    try:
        code_change_processor.delete_cache()
    except Exception as e:
        pass

if __name__ == "__main__":
    main()
