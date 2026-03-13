import click
from src.config import Config
from src.github_client import GitHubClient
from src.llm_summerizer import LLMSummarizer

@click.group()
def cli():
    """Automated Daily Standup Generator CLI."""
    pass

@cli.command()
@click.option('--days', default=1, help='Number of days to look back for activity (default: 1).')
def generate(days):
    """
    Fetches recent GitHub activity and generates a standup summary.
    """
    try:
        # 1. Validate environment before doing anything
        Config.validate()
        
        # 2. Fetch raw data from GitHub
        gh_client = GitHubClient()
        click.echo(f"Initializing Standup Generator for user: {gh_client.username}")
        click.echo("-" * 40)
        
        recent_activity_raw = gh_client.get_combined_activity(days_ago=days)
        
        # 3. Generate the summary using the LLM
        llm = LLMSummarizer()
        click.echo("\n--- Generated Standup Report ---\n")
        
        summary = llm.generate_standup(recent_activity_raw)
        
        # 4. Output the result
        click.echo(summary)
        click.echo("\n" + "-" * 40)
        click.echo("Done! Have a great standup.")
        
    except ValueError as e:
        click.secho(f"Configuration Error: {e}", fg="red")
    except Exception as e:
        click.secho(f"An unexpected error occurred: {e}", fg="red")

if __name__ == '__main__':
    cli()
