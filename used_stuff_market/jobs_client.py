import requests


class JobsClient:
    def __init__(self, base_url: str = "https://api.restful-api.dev"):
        self._base_url = base_url

    def schedule(self, job_name: str) -> str:
        """
        Schedule a job and returns its id.
        """
        url = self._base_url + "/objects"
        payload = {"name": job_name, "data": {"status": "NEW"}}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["id"]

    def get_job_details(self, job_id: str) -> dict:
        """
        Gets job details.
        """
        url = self._base_url + "/objects"
        params = {"id": job_id}
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()[0]

    def update_job_status(self, job_id: str, new_status: str) -> dict:
        url = self._base_url + "/objects/" + job_id
        payload = {"data": {"status": new_status}}
        response = requests.put(url, json=payload)
        response.raise_for_status()
        return response.json()
