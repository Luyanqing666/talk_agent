"""
工具函数模块
包含各种实用的工具函数
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import logging


def format_time(timestamp: str) -> str:
    """格式化时间戳"""
    try:
        dt = datetime.fromisoformat(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return timestamp


def clean_text(text: str) -> str:
    """清理文本，去除多余空白和特殊字符"""
    if not text:
        return ""
    # 去除多余空白
    text = re.sub(r'\s+', ' ', text).strip()
    # 去除特殊字符
    text = re.sub(r'[^\w\s一-鿿,.!?，。！？]', '', text)
    return text


def parse_json_safe(text: str) -> Optional[Dict[str, Any]]:
    """安全解析JSON字符串"""
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def extract_keywords(text: str, keywords: List[str]) -> Dict[str, bool]:
    """从文本中提取关键词"""
    text = text.lower()
    return {keyword: keyword.lower() in text for keyword in keywords}


def calculate_reading_time(text: str, words_per_minute: int = 200) -> float:
    """计算阅读时间（分钟）"""
    word_count = len(text.split())
    return word_count / words_per_minute


def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"


def generate_id(prefix: str = "item") -> str:
    """生成唯一ID"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"{prefix}_{timestamp}"


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length].rstrip() + suffix


def create_pagination(items: List[Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
    """创建分页"""
    total_items = len(items)
    total_pages = (total_items + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    paginated_items = items[start:end]

    return {
        "items": paginated_items,
        "page": page,
        "per_page": per_page,
        "total_items": total_items,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }