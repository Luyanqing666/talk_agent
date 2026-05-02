"""
任务执行模块测试
"""

import unittest
import asyncio
from src.tasks.task_executor import TaskExecutor, Task, TaskStatus


class TestTaskExecutor(unittest.TestCase):
    """任务执行器测试类"""

    def setUp(self):
        self.executor = TaskExecutor()

    def test_create_task(self):
        """测试创建任务"""
        async def test_function(param1, param2):
            return param1 + param2

        task = self.executor.create_task("测试任务", test_function, {"param1": 1, "param2": 2})
        self.assertEqual(task.name, "测试任务")
        self.assertEqual(task.params, {"param1": 1, "param2": 2})
        self.assertEqual(task.status, TaskStatus.PENDING)

    def test_execute_task(self):
        """测试执行任务"""
        async def test_function(result):
            await asyncio.sleep(0.1)
            return result

        task = self.executor.create_task("测试任务", test_function, {"result": "成功"})
        loop = asyncio.get_event_loop()
        executed_task = loop.run_until_complete(self.executor.execute_task(task.id))

        self.assertEqual(executed_task.status, TaskStatus.COMPLETED)
        self.assertEqual(executed_task.result, "成功")

    def test_list_tasks(self):
        """测试列出任务"""
        async def test_function():
            return "结果"

        # 创建多个任务
        for i in range(3):
            self.executor.create_task(f"任务{i}", test_function)

        tasks = self.executor.list_tasks()
        self.assertEqual(len(tasks), 3)

        completed_tasks = self.executor.list_tasks(TaskStatus.COMPLETED)
        self.assertEqual(len(completed_tasks), 0)

    def test_cancel_task(self):
        """测试取消任务"""
        async def long_running_task():
            await asyncio.sleep(1)
            return "完成"

        task = self.executor.create_task("长时间任务", long_running_task)
        loop = asyncio.get_event_loop()

        # 启动任务
        task_future = asyncio.ensure_future(self.executor.execute_task(task.id))

        # 立即取消
        self.assertTrue(self.executor.cancel_task(task.id))

        # 等待任务完成
        loop.run_until_complete(task_future)

        self.assertEqual(task.status, TaskStatus.CANCELLED)