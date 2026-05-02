"""
对话管理模块测试
"""

import unittest
import os
import shutil
from src.dialogue.dialogue_manager import DialogueManager
from src.agent.agent import AgentState


class TestDialogueManager(unittest.TestCase):
    """对话管理器测试类"""

    def setUp(self):
        self.test_dir = "test_dialogues"
        self.manager = DialogueManager(self.test_dir)
        # 清理测试目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def tearDown(self):
        # 清理测试目录
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_save_and_load_dialogue(self):
        """测试保存和加载对话"""
        agent_state = AgentState(conversation_history=[{"role": "user", "content": "测试消息"}])
        dialogue_id = self.manager.save_dialogue(agent_state)

        self.assertTrue(os.path.exists(os.path.join(self.test_dir, f"{dialogue_id}.json")))

        loaded_state = self.manager.load_dialogue(dialogue_id)
        self.assertEqual(len(loaded_state.conversation_history), 1)
        self.assertEqual(loaded_state.conversation_history[0]["content"], "测试消息")

    def test_list_dialogues(self):
        """测试列出对话"""
        agent_state = AgentState(conversation_history=[{"role": "user", "content": "测试消息1"}])
        self.manager.save_dialogue(agent_state)

        agent_state = AgentState(conversation_history=[{"role": "user", "content": "测试消息2"}])
        self.manager.save_dialogue(agent_state)

        dialogues = self.manager.list_dialogues()
        self.assertEqual(len(dialogues), 2)

    def test_search_dialogues(self):
        """测试搜索对话"""
        agent_state = AgentState(conversation_history=[{"role": "user", "content": "包含关键词的测试消息"}])
        self.manager.save_dialogue(agent_state)

        results = self.manager.search_dialogues("关键词")
        self.assertEqual(len(results), 1)
        self.assertIn("关键词", results[0]["message"])

    def test_delete_dialogue(self):
        """测试删除对话"""
        agent_state = AgentState(conversation_history=[{"role": "user", "content": "测试消息"}])
        dialogue_id = self.manager.save_dialogue(agent_state)

        self.assertTrue(self.manager.delete_dialogue(dialogue_id))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, f"{dialogue_id}.json")))