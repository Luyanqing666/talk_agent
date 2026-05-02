"""
任务执行模块
处理各种任务的执行和管理
"""

from typing import Dict, Any, List, Callable, Optional
from dataclasses import dataclass
import asyncio
import logging
from enum import Enum, auto


class TaskStatus(Enum):
    """任务状态枚举"""
    PENDING = auto()
    RUNNING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


@dataclass
class Task:
    """任务数据类"""
    id: str
    name: str
    description: str
    function: Callable
    params: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[Exception] = None
    created_at: str = ""
    completed_at: str = ""


class TaskExecutor:
    """任务执行器"""

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.logger = logging.getLogger(__name__)

    def create_task(self, name: str, function: Callable, params: Dict[str, Any] = None) -> Task:
        """创建新任务"""
        if params is None:
            params = {}

        task = Task(
            id=f"task_{len(self.tasks) + 1}",
            name=name,
            description=f"Task: {name}",
            function=function,
            params=params,
            status=TaskStatus.PENDING,
            created_at=self._get_current_time()
        )

        self.tasks[task.id] = task
        return task

    async def execute_task(self, task_id: str) -> Task:
        """执行任务"""
        if task_id not in self.tasks:
            raise ValueError(f"Task not found: {task_id}")

        task = self.tasks[task_id]
        task.status = TaskStatus.RUNNING

        try:
            task.result = await task.function(**task.params)
            task.status = TaskStatus.COMPLETED
            task.completed_at = self._get_current_time()
            self.logger.info(f"Task completed: {task_id}")
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = e
            task.completed_at = self._get_current_time()
            self.logger.error(f"Task failed: {task_id}, error: {str(e)}")

        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """获取任务"""
        return self.tasks.get(task_id)

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """列出任务"""
        if status is None:
            return list(self.tasks.values())

        return [task for task in self.tasks.values() if task.status == status]

    def cancel_task(self, task_id: str) -> bool:
        """取消任务"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.status == TaskStatus.RUNNING:
                task.status = TaskStatus.CANCELLED
                task.completed_at = self._get_current_time()
                self.logger.info(f"Task cancelled: {task_id}")
                return True
        return False

    def _get_current_time(self) -> str:
        """获取当前时间"""
        from datetime import datetime
        return datetime.now().isoformat()