import asyncio
from uuid import UUID

from temporalio import activity
from temporalio.client import Client

from used_stuff_market.availability import Availability
from used_stuff_market.payments import Payments
from used_stuff_market.shared_kernel.money import Currency, Money

tasks = []


@activity.defn
async def start_payment(item_id: int, owner_id: UUID, payment_id: UUID) -> int:
    Payments().initialize(
        owner_id=owner_id,
        uuid=payment_id,
        amount=Money(Currency.from_code("USD"), 100),
        description=f"Payment for item {item_id}",
    )
    # Let's pretend we wait for the user...
    task_token = activity.info().task_token
    tasks.append(asyncio.create_task(finish_async_activity(task_token)))

    activity.raise_complete_async()


@activity.defn
async def finalize(item_id: int) -> None:
    Availability().unregister(item_id)


@activity.defn
async def cancel(item_id: int, owner_id: UUID, payment_id: UUID) -> None:
    Availability().unlock(item_id, locked_by=owner_id)
    Payments().finalize(owner_id, payment_id)


@activity.defn
async def example(item_id: int) -> int:
    print(f"Received {item_id}")
    return item_id


async def finish_async_activity(task_token: bytes) -> None:
    # Pretend to do some work or wait for the end user
    await asyncio.sleep(1)

    # Get activity handle and finish the activity
    client = await Client.connect("localhost:7233")
    handle = client.get_async_activity_handle(task_token=task_token)

    await handle.complete()
