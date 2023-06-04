import httpx


class GithubClient:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.github.com"
    
    def get_check_suites(self, repo: str, ref: str) -> dict:
        url = f"{self.base_url}/repos/{repo}/commits/{ref}/check-suites"
        headers = {"Authorization": f"Bearer {self.token}"}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data

    def get_check_runs_in_suite(self, repo: str, check_suite_id: str) -> dict:
        url = f"{self.base_url}/repos/{repo}/check-suites/{check_suite_id}/check-runs"
        headers = {"Authorization": f"Bearer {self.token}"}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        return data
    
    # /repos/{owner}/{repo}/commits/{ref}/check-suites


    def fetch_run_id(self, repo: str, workflow: str) -> str:
        url = f"{self.base_url}/repos/{repo}/actions/workflows/{workflow}/runs"
        headers = {"Authorization": f"Bearer {self.token}"}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        # Assuming the first run in the list is the current run
        if data["total_count"] > 0:
            return str(data["workflow_runs"][0]["id"])
        else:
            raise ValueError("No workflow runs found.")

    def update_status(self, repo: str, run_id: str, status: str) -> None:
        url = f"{self.base_url}/repos/{repo}/check-runs/{run_id}"
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {"status": status}

        with httpx.Client() as client:
            response = client.patch(url, headers=headers, json=data)
            response.raise_for_status()
    
    def list_workflows(self, repo: str)-> str:
        url = f'{self.base_url}/repos/{repo}/actions/workflows'
        headers = {'Authorization': f'Bearer {self.token}'}

        with httpx.Client() as client:
            response = client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

        workflows = [workflow['name'] for workflow in data['workflows']]
        return workflows



# test = GithubClient(token)
# workflows = test.list_workflows(repo)
# fffff = test.get_check_suites(repo, "test3")
# aaaa = test.get_check_runs_in_suite(repo, fffff["check_suites"][1]["id"])
# asdf = test.fetch_run_id(repo, "Consumer Indexing")
# print(asdf)