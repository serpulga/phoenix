from fastapi import APIRouter, BackgroundTasks, Depends

from phoenix.models.task import Task, TaskRead
from phoenix.services.tasks import task_for_number, process_task


router = APIRouter()


@router.get("/primes/{number}", response_model=TaskRead)
def is_prime(
    bt: BackgroundTasks,
    task: Task = Depends(task_for_number),
):
    bt.add_task(process_task, task)
    return task
