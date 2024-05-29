import asyncio

from temporalio import activity
from temporalio.client import Client


# needed methods:
#  Payments.initialize (*should finish asynchronously)
#       If succeeds:
#           Availability.unregister
#       else:
#           Availability.unlock
#           Payments.cancel


@activity.defn
async def example(item_id: int) -> int:
    print(f"Received {item_id}")
    return item_id


# Async Activity Example

sequence = iter(range(1, 10_000))
tokens: dict[int, bytes] = {}
tasks = []


@activity.defn
async def async_activity_example(item_id: int) -> int:
    # do some work up to the point where e.g. need to wait for the user
    ...

    # Task token is required to resume execution asynchronously, elsewhere
    task_token = activity.info().task_token
    print(f"The token is {task_token!r}")

    # Gets next number and stores it, pretending to be a database
    number = next(sequence)
    tokens[number] = task_token

    # Schedule the async activity to be finished later
    # Simulate waiting for the end user
    tasks.append(asyncio.create_task(finish_async_activity(number)))

    # This stops execution and lets temporal know the activity will
    # be finished asynchronously
    activity.raise_complete_async()


async def finish_async_activity(index: int) -> None:
    # Pretend to do some work or wait for the end user
    await asyncio.sleep(1)

    # Get activity handle and finish the activity
    task_token = tokens.pop(index)
    client = await Client.connect("localhost:7233")
    handle = client.get_async_activity_handle(task_token=task_token)

    result = 123
    await handle.complete(result)
