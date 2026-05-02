"""
对话管理模块
处理对话的存储、检索和管理功能
"""

from typing import List, Dict, Any
from .agent import AgentState
import json
import os
from datetime import datetime


class DialogueManager:
    """对话管理器"""

    def __init__(self, storage_path: str = "dialogues"):
        self.storage_path = storage_path
        os.makedirs(storage_path, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    def save_dialogue(self, agent_state: AgentState, dialogue_id: str = None) -> str:
        """保存对话"""
        if dialogue_id is None:
            dialogue_id = f"dialogue_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        dialogue_data = {
            "id": dialogue_id,
            "timestamp": datetime.now().isoformat(),
            "conversation_history": agent_state.conversation_history,
            "user_preferences": agent_state.user_preferences,
            "context": agent_state.context
        }

        file_path = os.path.join(self.storage_path, f"{dialogue_id}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(dialogue_data, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Dialogue saved: {dialogue_id}")
        return dialogue_id

    def load_dialogue(self, dialogue_id: str) -> AgentState:
        """加载对话"""
        file_path = os.path.join(self.storage_path, f"{dialogue_id}.json")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dialogue not found: {dialogue_id}")

        with open(file_path, 'r', encoding='utf-8') as f:
            dialogue_data = json.load(f)

        return AgentState(
            conversation_history=dialogue_data.get("conversation_history", []),
            user_preferences=dialogue_data.get("user_preferences", {}),
            context=dialogue_data.get("context", {})
        )

    def list_dialogues(self) -> List[Dict[str, Any]]:
        """列出所有对话"""
        dialogues = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    dialogue_data = json.load(f)
                    dialogues.append({
                        "id": dialogue_data["id"],
                        "timestamp": dialogue_data["timestamp"],
                        "message_count": len(dialogue_data["conversation_history"])
                    })

        return sorted(dialogues, key=lambda x: x["timestamp"], reverse=True)

    def delete_dialogue(self, dialogue_id: str) -> bool:
        """删除对话"""
        file_path = os.path.join(self.storage_path, f"{dialogue_id}.json")

        if os.path.exists(file_path):
            os.remove(file_path)
            self.logger.info(f"Dialogue deleted: {dialogue_id}")
            return True
        return False

    def search_dialogues(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索对话"""
        results = []
        for filename in os.listdir(self.storage_path):
            if filename.endswith('.json'):
                file_path = os.path.join(self.storage_path, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    dialogue_data = json.load(f)
                    history = dialogue_data.get("conversation_history", [])

                    for message in history:
                        if keyword.lower() in message.get("content", "").lower():
                            results.append({
                                "id": dialogue_data["id"],
                                "timestamp": dialogue_data["timestamp"],
                                "message": message["content"]
                            })
                            break

        return results