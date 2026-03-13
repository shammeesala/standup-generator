from github import Github
from github import Auth
from src.config import Config
from datetime import datetime, timedelta

class GitHubClient:
    def __init__(self):
        # Using an access token
        auth = Auth.Token(Config.GITHUB_TOKEN)
        self.g = Github(auth=auth)
        
        # We need the user object to search for their activity
        self.user = self.g.get_user()
        self.username = self.user.login

    def get_recent_commits(self, days_ago: int = 1) -> str:
        """
        Fetches commit messages authored by the user across all their repos 
        in the past `days_ago` days. Formats them into a raw string.
        """
        since_date = datetime.now() - timedelta(days=days_ago)
        
        print(f"Fetching commits since {since_date.strftime('%Y-%m-%d')}...")
        
        commits_str = f"--- Commits in the last {days_ago} days ---\n"
        count = 0
        
        # Iterate over all repos accessible by the user
        for repo in self.g.get_user().get_repos():
            try:
                # Get commits by the specific user since the date
                commits = repo.get_commits(author=self.username, since=since_date)
                for commit in commits:
                    commits_str += f"- Repo: {repo.name} | Message: {commit.commit.message}\n"
                    count += 1
            except Exception as e:
                # Some repos might be empty or throw errors
                continue
                
        if count == 0:
            commits_str += "No commits found.\n"
            
        return commits_str

    def get_recent_prs(self, days_ago: int = 1) -> str:
        """
        Fetches Pull Requests created or reviewed by the user 
        in the past `days_ago` days. Formats them into a raw string.
        """
        since_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        print(f"Fetching PRs since {since_date}...")
        
        prs_str = f"--- Pull Requests in the last {days_ago} days ---\n"
        count = 0
        
        # Use GitHub Search API to find PRs authored by the user updated recently
        query = f"is:pr author:{self.username} updated:>={since_date}"
        issues = self.g.search_issues(query)
        
        for pr_issue in issues:
            state = pr_issue.state
            title = pr_issue.title
            repo_name = pr_issue.repository.name if pr_issue.repository else "Unknown Repo"
            
            prs_str += f"- Repo: {repo_name} | PR: {title} | State: {state}\n"
            count += 1
            
        if count == 0:
            prs_str += "No pull requests found.\n"
            
        return prs_str

    def get_combined_activity(self, days_ago: int = 1) -> str:
        """Helper to get both commits and PRs as a single text block."""
        commits = self.get_recent_commits(days_ago)
        prs = self.get_recent_prs(days_ago)
        return commits + "\n" + prs
