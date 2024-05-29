from temporalio.client import Client
from temporalio.worker import Worker

from used_stuff_market.processes.buying import activities
from used_stuff_market.processes.buying.workflow import BuyingWorkflow
from used_stuff_market.processes.config import TASK_QUEUE_NAME


async def main() -> None:
    client = await Client.connect("localhost:7233", namespace="default")

    worker = Worker(
        client,
        task_queue=TASK_QUEUE_NAME,
        workflows=[BuyingWorkflow],
        activities=[
            activities.start_payment,
            activities.finalize,
            activities.cancel,
        ],
    )
    await worker.run()
