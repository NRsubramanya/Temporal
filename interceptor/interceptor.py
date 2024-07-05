from dataclasses import asdict, is_dataclass
from typing import Any, Optional, Type, Union

from temporalio import activity, workflow
from temporalio.worker import (
    ActivityInboundInterceptor,
    ExecuteActivityInput,
    ExecuteWorkflowInput,
    Interceptor,
    WorkflowInboundInterceptor,
    WorkflowInterceptorClassInput,
)


with workflow.unsafe.imports_passed_through():
    from sentry_sdk import Hub, capture_exception, set_context, set_tag


def _set_common_workflow_tags(info: Union[workflow.Info, activity.Info]):
    set_tag("temporal.workflow.type", info.workflow_type)
    set_tag("temporal.workflow.id", info.workflow_id)



class _WorkflowInterceptor(WorkflowInboundInterceptor):
    async def execute_workflow(self, input: ExecuteWorkflowInput) -> Any:
        # https://docs.sentry.io/platforms/python/troubleshooting/#addressing-concurrency-issues
        try:
           result = await super().execute_workflow(input)
           print("Workflow successfully executed.")
           return result
        except Exception as e:
           print("Workflow execution failed.")
           capture_exception()
           raise e


class SentryInterceptor(Interceptor):
    """Temporal Interceptor class which will report workflow & activity exceptions to Sentry"""


    def workflow_interceptor_class(
        self, input: WorkflowInterceptorClassInput
    ) -> Optional[Type[WorkflowInboundInterceptor]]:
        return _WorkflowInterceptor
