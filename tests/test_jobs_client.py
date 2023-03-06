import vcr
from pytest import fixture

from used_stuff_market.jobs_client import JobsClient


@fixture
def jobs_client() -> JobsClient:
    return JobsClient(base_url="https://localhost")


@vcr.use_cassette("tests/fixtures/vcr_cassettes/test_jobs_client.yaml", match_on=['method', 'scheme', 'port', 'path', 'query'])
def test_scheduled_job_has_status_new(jobs_client: JobsClient) -> None:
    job_id = jobs_client.schedule("test_job_1")

    job_data = jobs_client.get_job_details(job_id)

    assert job_data["data"]["status"] == "NEW"


@vcr.use_cassette("tests/fixtures/vcr_cassettes/test_jobs_client2.yaml", match_on=['method', 'scheme', 'port', 'path', 'query'])
def test_job_status_can_be_updated(jobs_client: JobsClient) -> None:
    job_id = jobs_client.schedule("test_job_2")

    update_result = jobs_client.update_job_status(job_id, "DONE")

    job_data = jobs_client.get_job_details(job_id)

    assert update_result["data"]["status"] == "DONE"
    assert job_data["data"]["status"] == "DONE"
