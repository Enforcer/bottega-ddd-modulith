import asyncio
import random
import traceback

from temporalio.client import Client, WorkflowFailureError

from used_stuff_market.processes.config import TASK_QUEUE_NAME
from used_stuff_market.processes.buying.workflow import BuyingWorkflow


async def main() -> None:
    client = await Client.connect("localhost:7233")

    item_id = random.randint(1, 1_000_000)

    try:
        await client.execute_workflow(
            BuyingWorkflow.run,
            args=[item_id],
            id=f"pay-for-item-{item_id}",  # needs to be UNIQUE!
            task_queue=TASK_QUEUE_NAME,
        )
    except WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(main())
