from fastapi import APIRouter, Depends

from phoenix.models.task import TaskResult
from phoenix.services.tasks import task_result


router = APIRouter()


@router.get("/tasks/{task_id}", response_model=TaskResult)
async def task_status(
    result: TaskResult = Depends(task_result),
):
    return result
