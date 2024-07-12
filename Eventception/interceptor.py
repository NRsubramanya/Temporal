import os
import requests
from temporalio.worker import WorkflowInboundInterceptor, ExecuteWorkflowInput
from typing import Any, Optional, Type
from datetime import timedelta
from temporalio import activity, workflow
from temporalio.worker import (
    ActivityInboundInterceptor,
    ExecuteActivityInput,
    ExecuteWorkflowInput,
    Interceptor,
    WorkflowInboundInterceptor,
    WorkflowInterceptorClassInput,
)
from activities.backend import BackendActivities 

class JobStatusUpdateInterceptor(WorkflowInboundInterceptor):
    def __init__(self, next: WorkflowInboundInterceptor):
        super().__init__(next)

    async def execute_workflow(self, input: ExecuteWorkflowInput) -> Any:
        print(f"Workflow input arguments: {input.args}")
        job_id = input.args[0]['job_id']
        job_details = {"job_id": job_id, "status": None}  # Initialize job details with job_id and status

        try:
            result = await self.next.execute_workflow(input)
            print("Workflow successfully executed.")
            
            # Update job status to 'success'
            job_details['status'] = "success"
            await workflow.execute_activity(
                BackendActivities.update_job_status, 
                job_details, 
                start_to_close_timeout=timedelta(seconds=30)
            )
            
            return result
        except Exception as e:
            print("Workflow execution failed.")
            
            # Update job status to 'failure'
            job_details['status'] = "failure"
            await workflow.execute_activity(
                BackendActivities.update_job_status, 
                job_details, 
                start_to_close_timeout=timedelta(seconds=30)
            )
            
            # Re-raise the exception to propagate it further
            raise e

class EventInterceptor(Interceptor):
    """Temporal Interceptor class which will report workflow & activity exceptions to Sentry"""

    def workflow_interceptor_class(
        self, input: WorkflowInterceptorClassInput
    ) -> Optional[Type[WorkflowInboundInterceptor]]:
        return JobStatusUpdateInterceptor
