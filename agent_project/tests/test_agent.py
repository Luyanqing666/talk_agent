"""
Agent模块测试
"""

import unittest
from src.agent.agent import Agent, AgentState


class TestAgent(unittest.TestCase):
    """Agent测试类"""

    def setUp(self):
        self.agent = Agent("TestAgent")

    def test_initial_state(self):
        """测试初始状态"""
        self.assertEqual(self.agent.name, "TestAgent")
        self.assertEqual(len(self.agent.state.conversation_history), 0)

    def test_process_message(self):
        """测试消息处理"""
        response = self.agent.process_message("你好")
        self.assertIn("你好", response)
        self.assertEqual(len(self.agent.state.conversation_history), 2)

    def test_get_conversation_history(self):
        """测试获取对话历史"""
        self.agent.process_message("测试消息")
        history = self.agent.get_conversation_history()
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")

    def test_clear_history(self):
        """测试清空历史"""
        self.agent.process_message("测试消息")
        self.agent.clear_history()
        self.assertEqual(len(self.agent.state.conversation_history), 0)