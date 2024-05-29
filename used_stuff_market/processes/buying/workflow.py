from datetime import timedelta
from uuid import UUID

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    # activities need to be imported under this context manager
    from used_stuff_market.processes.buying.activities import (
        cancel,
        finalize,
        start_payment,
    )


@workflow.defn
class BuyingWorkflow:
    @workflow.run
    async def run(self, item_id: int) -> None:
        retry_policy = RetryPolicy(
            maximum_attempts=3,
            maximum_interval=timedelta(seconds=2),
            non_retryable_error_types=["ValueError"],
        )

        payment_id = UUID(int=item_id)
        owner_id = UUID(int=item_id)
        try:
            await workflow.execute_activity(
                start_payment,
                retry_policy=retry_policy,
                args=[item_id, owner_id, payment_id],
                start_to_close_timeout=timedelta(seconds=10),
            )
        except ActivityError as e:
            print(f"Got exception: {e}")
            await workflow.execute_activity(
                cancel,
                args=[item_id, owner_id, payment_id],
                start_to_close_timeout=timedelta(seconds=10),
            )
        else:
            await workflow.execute_activity(
                finalize, args=[item_id], start_to_close_timeout=timedelta(seconds=10)
            )
