"""
Agent项目主程序
提供命令行界面和基本功能
"""

import argparse
import logging
import sys
from src.agent.agent import Agent
from src.dialogue.dialogue_manager import DialogueManager
from src.tasks.task_executor import TaskExecutor
from src.utils.utils import format_time


def setup_logging():
    """设置日志"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def create_parser():
    """创建命令行参数解析器"""
    parser = argparse.ArgumentParser(description='Agent项目命令行工具')
    subparsers = parser.add_subparsers(dest='command', help='可用命令')

    # 对话相关命令
    dialogue_parser = subparsers.add_parser('dialogue', help='对话管理')
    dialogue_subparsers = dialogue_parser.add_subparsers(dest='subcommand')

    dialogue_list = dialogue_subparsers.add_parser('list', help='列出所有对话')
    dialogue_load = dialogue_subparsers.add_parser('load', help='加载对话')
    dialogue_load.add_argument('dialogue_id', help='对话ID')
    dialogue_search = dialogue_subparsers.add_parser('search', help='搜索对话')
    dialogue_search.add_argument('keyword', help='搜索关键词')
    dialogue_delete = dialogue_subparsers.add_parser('delete', help='删除对话')
    dialogue_delete.add_argument('dialogue_id', help='对话ID')

    # 任务相关命令
    task_parser = subparsers.add_parser('task', help='任务管理')
    task_subparsers = task_parser.add_subparsers(dest='subcommand')

    task_list = task_subparsers.add_parser('list', help='列出任务')
    task_list.add_argument('--status', choices=['pending', 'running', 'completed', 'failed', 'cancelled'],
                         help='按状态过滤')
    task_execute = task_subparsers.add_parser('execute', help='执行任务')
    task_execute.add_argument('task_id', help='任务ID')
    task_cancel = task_subparsers.add_parser('cancel', help='取消任务')
    task_cancel.add_argument('task_id', help='任务ID')

    # 交互模式
    subparsers.add_parser('interactive', help='交互模式')

    return parser


def list_dialogues(dialogue_manager):
    """列出所有对话"""
    dialogues = dialogue_manager.list_dialogues()
    print("\n=== 对话列表 ===")
    for dialogue in dialogues:
        print(f"ID: {dialogue['id']}")
        print(f"时间: {format_time(dialogue['timestamp'])}")
        print(f"消息数: {dialogue['message_count']}")
        print("-" * 40)


def load_dialogue(dialogue_manager, dialogue_id):
    """加载对话"""
    try:
        agent_state = dialogue_manager.load_dialogue(dialogue_id)
        print(f"\n=== 对话内容 ({dialogue_id}) ===")
        for message in agent_state.conversation_history:
            role = "用户" if message["role"] == "user" else "助手"
            print(f"{role}: {message['content']}")
            print(f"时间: {format_time(message['timestamp'])}")
            print("-" * 30)
    except FileNotFoundError:
        print(f"错误: 对话 {dialogue_id} 不存在")


def search_dialogues(dialogue_manager, keyword):
    """搜索对话"""
    results = dialogue_manager.search_dialogues(keyword)
    print(f"\n=== 搜索结果 (关键词: {keyword}) ===")
    for result in results:
        print(f"ID: {result['id']}")
        print(f"时间: {format_time(result['timestamp'])}")
        print(f"消息: {result['message']}")
        print("-" * 40)


def delete_dialogue(dialogue_manager, dialogue_id):
    """删除对话"""
    if dialogue_manager.delete_dialogue(dialogue_id):
        print(f"成功删除对话: {dialogue_id}")
    else:
        print(f"错误: 对话 {dialogue_id} 不存在或无法删除")


def list_tasks(task_executor, status=None):
    """列出任务"""
    status_map = {
        'pending': TaskStatus.PENDING,
        'running': TaskStatus.RUNNING,
        'completed': TaskStatus.COMPLETED,
        'failed': TaskStatus.FAILED,
        'cancelled': TaskStatus.CANCELLED
    }

    tasks = task_executor.list_tasks(status_map.get(status))
    print("\n=== 任务列表 ===")
    for task in tasks:
        print(f"ID: {task.id}")
        print(f"名称: {task.name}")
        print(f"状态: {task.status.name}")
        if task.result is not None:
            print(f"结果: {task.result}")
        if task.error is not None:
            print(f"错误: {task.error}")
        print(f"创建时间: {format_time(task.created_at)}")
        if task.completed_at:
            print(f"完成时间: {format_time(task.completed_at)}")
        print("-" * 40)


def interactive_mode():
    """交互模式"""
    print("=== Agent交互模式 ===")
    print("输入 'exit' 退出，输入 'help' 查看帮助")

    agent = Agent("InteractiveAgent")
    dialogue_manager = DialogueManager()
    task_executor = TaskExecutor()

    while True:
        try:
            user_input = input("\n您: ").strip()
            if user_input.lower() == 'exit':
                break
            elif user_input.lower() == 'help':
                print("可用命令:")
                print("  exit - 退出")
                print("  help - 显示帮助")
                print("  save - 保存当前对话")
                print("  clear - 清空历史")
                print("  tasks - 查看任务")
                continue

            if user_input.lower() == 'save':
                dialogue_id = dialogue_manager.save_dialogue(agent.state)
                print(f"对话已保存，ID: {dialogue_id}")
                continue

            if user_input.lower() == 'clear':
                agent.clear_history()
                print("历史已清空")
                continue

            if user_input.lower() == 'tasks':
                list_tasks(task_executor)
                continue

            response = agent.process_message(user_input)
            print(f"助手: {response}")

        except KeyboardInterrupt:
            print("\n退出交互模式")
            break
        except Exception as e:
            print(f"错误: {e}")


def main():
    """主函数"""
    setup_logging()
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 初始化组件
    agent = Agent("CLI_Agent")
    dialogue_manager = DialogueManager()
    task_executor = TaskExecutor()

    # 处理命令
    if args.command == 'dialogue':
        if args.subcommand == 'list':
            list_dialogues(dialogue_manager)
        elif args.subcommand == 'load':
            load_dialogue(dialogue_manager, args.dialogue_id)
        elif args.subcommand == 'search':
            search_dialogues(dialogue_manager, args.keyword)
        elif args.subcommand == 'delete':
            delete_dialogue(dialogue_manager, args.dialogue_id)

    elif args.command == 'task':
        if args.subcommand == 'list':
            list_tasks(task_executor, args.status)
        elif args.subcommand == 'execute':
            # 这里可以添加任务执行逻辑
            print(f"执行任务: {args.task_id}")
        elif args.subcommand == 'cancel':
            # 这里可以添加任务取消逻辑
            print(f"取消任务: {args.task_id}")

    elif args.command == 'interactive':
        interactive_mode()


if __name__ == '__main__':
    main()