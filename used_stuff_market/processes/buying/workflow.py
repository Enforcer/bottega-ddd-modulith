from datetime import timedelta

from temporalio import workflow
from temporalio.common import RetryPolicy
from temporalio.exceptions import ActivityError

with workflow.unsafe.imports_passed_through():
    # activities need to be imported under this context manager
    from used_stuff_market.processes.buying.activities import (
        example,
        async_activity_example,
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

        result = await workflow.execute_activity(
            example,
            retry_policy=retry_policy,
            args=[item_id],
            start_to_close_timeout=timedelta(seconds=10),
        )

        try:
            result = await workflow.execute_activity(
                async_activity_example,
                args=[item_id],
                retry_policy=retry_policy,
                start_to_close_timeout=timedelta(seconds=1),
            )
        except ActivityError as e:
            print(f"Got exception: {e}")
            raise

        print(f"End of workflow, got from activity: {result}")
