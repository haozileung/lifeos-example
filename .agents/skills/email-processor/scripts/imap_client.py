#!/usr/bin/env python3
"""
IMAP邮件客户端 - 读取、筛选和处理邮件
用于email-processor技能
"""

import imaplib
import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple, Any
import re
import sys
import os
import warnings
from pathlib import Path
from dotenv import load_dotenv

# 抑制 markdownify 的 XML 解析警告
warnings.filterwarnings("ignore", message=".*XMLParsedAsHTMLWarning.*")
warnings.filterwarnings("ignore", category=DeprecationWarning)

import markdownify

# ============================================================================
# Constants
# ============================================================================

class Encodings:
    """Encoding fallback order for decoding email content."""
    FALLBACK_ORDER = ["utf-8", "gbk", "gb2312", "iso-8859-1", "windows-1252"]

class PathConfig:
    """路径配置"""
    DEFAULT_MAIL_DIR = "mails"  # 默认邮件保存目录

# Task extraction classes removed - functionality disabled

# Pre-compile regex patterns for better performance
FROM_PATTERN = re.compile(r'(?:")?([^"\<]+)(?:")?\s*\<([^>]+)\>')
DATETIME_SPLIT_PATTERN = re.compile(r'\s+')


def try_decode_with_fallback(payload: bytes, encodings: List[str] = None) -> Optional[str]:
    """
    尝试多种编码方式解码字节流

    Args:
        payload: 要解码的字节数据
        encodings: 编码列表，默认使用 Encodings.FALLBACK_ORDER

    Returns:
        解码后的字符串，如果所有编码都失败则返回 None
    """
    if encodings is None:
        encodings = Encodings.FALLBACK_ORDER

    for encoding in encodings:
        try:
            return payload.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return None


def get_config_from_dotenv(env_file: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    从 .env 文件读取邮箱配置

    支持的配置项：
    - IMAP_SERVER: IMAP服务器地址
    - IMAP_PORT: IMAP端口（默认993）
    - IMAP_USERNAME: 邮箱用户名
    - IMAP_PASSWORD: 邮箱密码或应用专用密码

    Args:
        env_file: .env 文件路径，如果为 None 则查找默认位置

    Returns:
        dict: 包含 server, port, username, password, env_file 的字典，如果配置不完整则返回 None
    """
    # 查找 .env 文件
    if env_file:
        env_path = Path(env_file)
    else:
        # 按优先级查找 .env 文件
        script_dir = Path(__file__).parent.parent
        possible_paths = [
            Path('.env'),  # 当前目录
            Path.home() / '.email-processor.env',  # 用户主目录
            script_dir / '.env',  # 技能目录
            script_dir / '.env.example',  # 示例配置（如果用户复制了）
        ]

        env_path = None
        for path in possible_paths:
            if path.exists():
                env_path = path
                break

    # 修复：移除冗余的文件存在性检查（TOCTOU anti-pattern）
    if not env_path:
        return None

    # 加载 .env 文件
    load_dotenv(env_path)

    server = os.getenv("IMAP_SERVER")
    username = os.getenv("IMAP_USERNAME")
    password = os.getenv("IMAP_PASSWORD")
    port = os.getenv("IMAP_PORT", "993")

    # 检查必需的配置
    if not all([server, username, password]):
        return None

    return {
        "server": server,
        "port": int(port),
        "username": username,
        "password": password,
        "env_file": str(env_path)
    }


def decode_header_value(header_value: str) -> str:
    """
    解码MIME编码的头字段值（如发件人、主题等）

    Args:
        header_value: 可能包含MIME编码的头字段值

    Returns:
        解码后的字符串
    """
    if not header_value:
        return ""

    try:
        decoded_parts = decode_header(header_value)
        result = ""
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                # 尝试使用指定的编码，默认为utf-8
                encoding = encoding or "utf-8"
                try:
                    result += part.decode(encoding)
                except (UnicodeDecodeError, LookupError):
                    # 如果指定编码失败，尝试其他常见编码
                    for fallback_encoding in ["utf-8", "gbk", "gb2312", "iso-8859-1"]:
                        try:
                            result += part.decode(fallback_encoding)
                            break
                        except:
                            continue
                    else:
                        # 所有编码都失败，使用忽略错误模式
                        result += part.decode(encoding, errors="ignore")
            else:
                result += part
        return result
    except Exception as e:
        # 解码失败，返回原始值
        return header_value


class EmailClient:
    """IMAP邮件客户端"""

    def __init__(self, server: str, port: int, username: str, password: str):
        """
        初始化IMAP客户端

        Args:
            server: IMAP服务器地址
            port: IMAP端口（通常993）
            username: 邮箱地址
            password: 密码或应用专用密码
        """
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.mail = None

    def connect(self) -> bool:
        """连接到IMAP服务器"""
        try:
            self.mail = imaplib.IMAP4_SSL(self.server, self.port)
            self.mail.login(self.username, self.password)
            self.mail.select("INBOX")
            return True
        except Exception as e:
            print(f"连接失败: {e}", file=sys.stderr)
            return False

    def disconnect(self):
        """断开连接"""
        if self.mail:
            try:
                self.mail.close()
                self.mail.logout()
            except:
                pass

    def search_emails(
        self,
        since_date: Optional[str] = None,
        from_sender: Optional[str] = None,
        to_recipient: Optional[str] = None,
        subject: Optional[str] = None,
        unread_only: bool = False,
        limit: int = 100,
        page: int = 1
    ) -> List[int]:
        """
        搜索邮件

        Args:
            since_date: 起始日期（格式：01-Mar-2026）
            from_sender: 发件人邮箱
            to_recipient: 收件人邮箱
            subject: 主题关键词
            unread_only: 仅未读邮件
            limit: 每页最大返回数量
            page: 页码（从1开始，默认为1）

        Returns:
            邮件ID列表
        """
        if not self.mail:
            return []

        # 构建搜索条件
        criteria = []
        if since_date:
            criteria.append(f'(SINCE "{since_date}")')
        if from_sender:
            criteria.append(f'(FROM "{from_sender}")')
        if to_recipient:
            criteria.append(f'(TO "{to_recipient}")')
        if subject:
            criteria.append(f'(SUBJECT "{subject}")')
        if unread_only:
            criteria.append('(UNSEEN)')

        search_criteria = " ".join(criteria) if criteria else "(ALL)"

        try:
            # 检查搜索条件是否包含非ASCII字符（如中文）
            has_non_ascii = any(ord(c) > 127 for c in search_criteria)

            # 如果包含非ASCII字符，使用UTF-8字符集；否则使用默认（ASCII）
            if has_non_ascii:
                # 尝试使用UTF-8字符集进行搜索
                try:
                    status, messages = self.mail.search("UTF-8", search_criteria)
                except UnicodeEncodeError:
                    # 如果UTF-8失败，尝试修改为IMAP的CHARSET语法
                    status, messages = self.mail.search(f'CHARSET UTF-8 {search_criteria}'.encode('utf-8'), None)
            else:
                status, messages = self.mail.search(None, search_criteria)

            if status != "OK":
                return []

            email_ids = messages[0].split()
            # 转换为字符串并返回最近的邮件（ID倒序）
            email_ids_str = [str(int(email_id)) for email_id in email_ids]
            email_ids_str = list(reversed(email_ids_str))

            # 计算分页偏移量
            offset = (page - 1) * limit
            start_idx = offset
            end_idx = offset + limit

            # 返回指定页的数据
            if start_idx >= len(email_ids_str):
                return []  # 页码超出范围
            return email_ids_str[start_idx:end_idx]

        except Exception as e:
            print(f"搜索失败: {e}", file=sys.stderr)
            return []

    def fetch_emails(self, email_ids: List[int]) -> List[Dict]:
        """
        获取并解析邮件

        Args:
            email_ids: 邮件ID列表

        Returns:
            邮件数据列表
        """
        emails = []

        for email_id in email_ids:
            try:
                # 获取邮件（RFC822格式）
                status, msg_data = self.mail.fetch(str(email_id), "(RFC822)")
                if status != "OK":
                    continue

                # 解析邮件
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                email_data = self._parse_email(msg)
                email_data["id"] = email_id
                emails.append(email_data)

            except Exception as e:
                print(f"解析邮件 {email_id} 失败: {e}", file=sys.stderr)
                continue

        return emails

    def _parse_email(self, msg) -> Dict:
        """解析邮件对象"""
        email_data = {
            "from": "",
            "from_name": "",
            "from_email": "",
            "to": "",
            "subject": "",
            "date": "",
            "body": "",
            "attachments": [],
            "is_unread": False
        }

        # 发件人
        from_header = msg.get("From", "")
        # 先解码MIME编码
        decoded_from = decode_header_value(from_header)
        email_data["from"] = decoded_from

        # 尝试分离姓名和邮箱
        from_match = re.search(r"(?:\")?([^\"\<]+)(?:\")?\s*\<([^>]+)\>", decoded_from)
        if from_match:
            email_data["from_name"] = from_match.group(1).strip()
            email_data["from_email"] = from_match.group(2).strip()
        else:
            email_data["from_email"] = decoded_from

        # 收件人
        email_data["to"] = msg.get("To", "")

        # 主题（处理编码）
        subject = msg.get("Subject", "")
        email_data["subject"] = decode_header_value(subject) if subject else ""

        # 日期
        email_data["date"] = msg.get("Date", "")

        # 邮件正文
        body = self._extract_body(msg)
        email_data["body"] = body

        # 附件
        email_data["attachments"] = self._extract_attachments(msg)

        # 未读状态（如果有Flags字段）
        flags = msg.get("Flags", "")
        if "\\Seen" not in flags:
            email_data["is_unread"] = True

        return email_data

    def _extract_body(self, msg) -> str:
        """提取邮件正文，优先使用纯文本，避免复杂HTML表格"""
        text_body = ""
        html_body = ""

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))

                # 跳过附件
                if "attachment" in content_disposition:
                    continue

                try:
                    payload = part.get_payload(decode=True)
                    if not payload:
                        continue

                    # 尝试多种编码解码
                    decoded = None
                    for encoding in Encodings.FALLBACK_ORDER:
                        try:
                            decoded = payload.decode(encoding)
                            break
                        except:
                            continue

                    if decoded:
                        if content_type == "text/plain" and not text_body:
                            text_body = decoded
                        elif content_type == "text/html" and not html_body:
                            html_body = decoded
                except Exception as e:
                    # 静默失败，继续处理其他部分
                    continue
        else:
            # 非多部分邮件
            try:
                payload = msg.get_payload(decode=True)
                if payload:
                    content_type = msg.get_content_type()
                    for encoding in Encodings.FALLBACK_ORDER:
                        try:
                            decoded = payload.decode(encoding)
                            if content_type == "text/html":
                                html_body = decoded
                            else:
                                text_body = decoded
                            break
                        except:
                            continue
            except:
                text_body = str(msg.get_payload())

        if html_body:
            return html_body.strip()

        if text_body:
            return text_body.strip()
        return ""

    def _extract_attachments(self, msg) -> List[str]:
        """提取附件列表"""
        attachments = []

        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition", ""))

            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    # 解码文件名
                    decoded = decode_header(filename)[0]
                    if isinstance(decoded[0], bytes):
                        encoding = decoded[1] or "utf-8"
                        try:
                            filename = decoded[0].decode(encoding)
                        except:
                            filename = str(decoded[0])
                    attachments.append(filename)

        return attachments


# Task extraction function removed - functionality disabled

def generate_single_email(email_data: Dict) -> str:
    """
    生成单个邮件的Markdown格式

    Args:
        email_data: 邮件数据

    Returns:
        Markdown文本
    """
    subject = email_data.get("subject", "(无主题)")
    date = email_data.get("date", "")
    from_email = email_data.get("from_email", "")
    body = email_data.get("body", "")

    # 邮件标题
    md = f"# {subject}\n\n"
    md += f"**发件人**: {from_email}\n"
    md += f"**日期**: {date}\n"
    md += f"\n---\n\n"

    # 邮件正文（原始内容，不做任何处理）
    md += f"{body}\n"
    md += f"\n---\n"

    return md


def generate_markdown_summary(
    emails: List[Dict],
    date_str: str = None
) -> str:
    """
    生成Markdown格式的邮件列表（仅标题和正文，不做加工）

    Args:
        emails: 邮件列表
        date_str: 日期字符串（未使用）

    Returns:
        Markdown文本
    """
    md = ""

    for email_data in emails:
        md += generate_single_email(email_data)
        md += "\n\n"

    return md


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全的字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    # 替换不安全的字符
    filename = filename.replace("/", "-")
    filename = filename.replace("\\", "-")
    filename = filename.replace(":", "-")
    filename = filename.replace("*", "")
    filename = filename.replace("?", "")
    filename = filename.replace("\"", "")
    filename = filename.replace("<", "")
    filename = filename.replace(">", "")
    filename = filename.replace("|", "")

    # 移除前后空格
    filename = filename.strip()

    # 限制文件名长度
    if len(filename) > 200:
        filename = filename[:200]

    return filename


def save_emails_to_directory(emails: List[Dict], output_dir: str, skip_existing: bool = True) -> Tuple[int, int]:
    """
    将每封邮件保存到单独的文件中

    Args:
        emails: 邮件列表
        output_dir: 输出目录路径
        skip_existing: 是否跳过已存在的文件（默认 True）

    Returns:
        Tuple of (成功保存的文件数量, 跳过的文件数量)
    """
    import os
    from pathlib import Path

    # 创建输出目录
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    saved_count = 0
    skipped_count = 0

    for i, email_data in enumerate(emails, 1):
        subject = email_data.get("subject", "(无主题)")
        date = email_data.get("date", "")

        # 尝试解析日期
        try:
            from email.utils import parsedate_to_datetime
            dt = parsedate_to_datetime(date)
            date_str = dt.strftime("%Y%m%d-%H%M")
        except:
            date_str = f"email{i:03d}"

        # 生成文件名：日期_主题.md
        filename_subject = sanitize_filename(subject)
        filename = f"{date_str}_{filename_subject}.md"

        # 文件路径
        filepath = Path(output_dir) / filename

        # 如果文件已存在，根据 skip_existing 决定是否跳过
        if filepath.exists():
            if skip_existing:
                skipped_count += 1
                print(f"- 跳过（已存在）: {filepath.name}", file=sys.stderr)
                continue
            else:
                # 如果不跳过，添加数字后缀避免冲突
                counter = 1
                while filepath.exists():
                    filepath = Path(output_dir) / f"{date_str}_{filename_subject}_{counter}.md"
                    counter += 1

        # 生成邮件内容
        content = generate_single_email(email_data)

        # 保存到文件
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            saved_count += 1
            print(f"+ 已保存: {filepath.name}", file=sys.stderr)
        except Exception as e:
            print(f"x 保存失败 {filepath.name}: {e}", file=sys.stderr)

    return saved_count, skipped_count


def main():
    """命令行接口"""
    import argparse

    # 从 .env 文件读取配置
    env_config = get_config_from_dotenv()

    parser = argparse.ArgumentParser(
        description="IMAP邮件处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
配置说明：
  该工具强制使用 .env 文件存储邮箱凭据，不支持环境变量。

  .env 文件位置（按优先级）：
    1. 当前目录的 .env 文件
    2. ~/.email-processor.env
    3. 技能目录的 .env 文件

  .env 文件格式：
    IMAP_SERVER=imap.qq.com
    IMAP_PORT=993
    IMAP_USERNAME=your@email.com
    IMAP_PASSWORD=your-app-password

  示例：
    # 创建配置文件
    cp .env.example .env
    # 编辑 .env 文件填入你的邮箱信息
    # 然后直接运行（无需传递凭据参数）
    python3 imap_client.py --since "07-Mar-2026"
        """
    )

    # .env 配置参数（如果找到 .env 文件，这些参数自动填充）
    if env_config:
        parser.add_argument("--server", default=env_config["server"],
                          help=f"IMAP服务器地址（默认: 从 .env 读取: {env_config['server']}）")
        parser.add_argument("--port", type=int, default=env_config["port"],
                          help=f"IMAP端口（默认: 从 .env 读取: {env_config['port']}）")
        parser.add_argument("--username", default=env_config["username"],
                          help=f"邮箱地址（默认: 从 .env 读取: {env_config['username']}）")
        parser.add_argument("--password", default=env_config["password"],
                          help="密码或应用专用密码（默认: 从 .env 读取）")
        parser.add_argument("--env-file", help=".env 文件路径（可选）")
    else:
        # 如果没找到 .env 文件，所有参数必须手动提供
        parser.add_argument("--server", required=True, help="IMAP服务器地址")
        parser.add_argument("--port", type=int, default=993, help="IMAP端口（默认993）")
        parser.add_argument("--username", required=True, help="邮箱地址")
        parser.add_argument("--password", required=True, help="密码或应用专用密码")
        parser.add_argument("--env-file", help=".env 文件路径（可选）")

    # 搜索和筛选参数
    parser.add_argument("--since", help="起始日期 (格式: 01-Mar-2026)")
    parser.add_argument("--from", dest="from_sender", help="发件人邮箱")
    parser.add_argument("--subject", help="主题关键词")
    parser.add_argument("--unread", action="store_true", help="仅未读邮件")
    parser.add_argument("--limit", type=int, default=100, help="每页最大邮件数（默认100）")
    parser.add_argument("--page", type=int, default=1, help="页码（从1开始，默认1）")

    # 输出参数
    parser.add_argument("--output", help="输出文件路径（所有邮件保存到一个文件）")
    parser.add_argument("--output-dir", help="输出目录路径（每封邮件保存为单独文件）")
    parser.add_argument("--print", action="store_true", help="输出到控制台（默认保存到 mails 文件夹）")
    parser.add_argument("--skip-existing", action="store_true", default=True, help="跳过已存在的文件（默认启用）")
    parser.add_argument("--no-skip-existing", action="store_false", dest="skip_existing", help="不跳过已存在的文件（覆盖默认）")

    args = parser.parse_args()

    # 如果指定了 --env-file，重新加载配置
    if args.env_file:
        env_config = get_config_from_dotenv(args.env_file)
        if not env_config:
            print(f"错误: 无法从 {args.env_file} 加载配置", file=sys.stderr)
            sys.exit(1)
        args.server = env_config["server"]
        args.port = env_config["port"]
        args.username = env_config["username"]
        args.password = env_config["password"]

    # 如果找不到 .env 文件且没有提供必需参数，给出友好提示
    if not env_config:
        print("⚠️  警告: 未找到 .env 配置文件", file=sys.stderr)
        print("", file=sys.stderr)
        print("推荐做法：创建 .env 文件存储邮箱凭据", file=sys.stderr)
        print("", file=sys.stderr)
        print("步骤：", file=sys.stderr)
        print("  1. 复制示例配置:", file=sys.stderr)
        print("     cp .env.example .env", file=sys.stderr)
        print("  2. 编辑 .env 文件，填入你的邮箱信息", file=sys.stderr)
        print("  3. 重新运行命令", file=sys.stderr)
        print("", file=sys.stderr)
        print("或者直接通过命令行参数提供凭据（不推荐）", file=sys.stderr)
        print("", file=sys.stderr)

    # 连接并搜索
    if env_config:
        client = EmailClient(args.server, args.port, args.username, args.password)
        print(f"✓ 使用 .env 配置: {env_config['env_file']}", file=sys.stderr)
        print(f"✓ 邮箱: {args.username}", file=sys.stderr)
    else:
        client = EmailClient(args.server, args.port, args.username, args.password)
        print(f"⚠️  使用命令行参数配置（不推荐）", file=sys.stderr)

    if not client.connect():
        sys.exit(1)

    try:
        email_ids = client.search_emails(
            since_date=args.since,
            from_sender=args.from_sender,
            subject=args.subject,
            unread_only=args.unread,
            limit=args.limit,
            page=args.page
        )

        print(f"第 {args.page} 页：找到 {len(email_ids)} 封邮件（每页 {args.limit} 封）", file=sys.stderr)

        if not email_ids:
            if args.page > 1:
                print(f"第 {args.page} 页没有邮件（已是最后一页）", file=sys.stderr)
            else:
                print("没有找到符合条件的邮件")
            sys.exit(0)

        emails = client.fetch_emails(email_ids)
        print(f"成功解析 {len(emails)} 封邮件", file=sys.stderr)

        # 处理输出
        if args.print:
            # 输出到控制台
            markdown = generate_markdown_summary(emails)
            print(markdown)
        elif args.output_dir:
            # 每封邮件保存到单独文件
            saved_count, skipped_count = save_emails_to_directory(emails, args.output_dir, skip_existing=args.skip_existing)
            if skipped_count > 0:
                print(f"+ 已保存 {saved_count} 封邮件，- 跳过 {skipped_count} 封（已存在）", file=sys.stderr)
            else:
                print(f"+ 已保存 {saved_count} 封邮件到目录: {args.output_dir}", file=sys.stderr)
        elif args.output:
            # 所有邮件保存到一个文件
            markdown = generate_markdown_summary(emails)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(markdown)
            print(f"+ 已保存到文件: {args.output}", file=sys.stderr)
        else:
            # 默认：保存到技能目录的 mails 文件夹
            script_dir = Path(__file__).parent.parent
            default_mail_dir = script_dir / PathConfig.DEFAULT_MAIL_DIR
            saved_count, skipped_count = save_emails_to_directory(emails, str(default_mail_dir), skip_existing=args.skip_existing)
            if skipped_count > 0:
                print(f"+ 已保存 {saved_count} 封邮件，- 跳过 {skipped_count} 封（已存在）", file=sys.stderr)
            else:
                print(f"+ 已保存 {saved_count} 封邮件到默认目录: {default_mail_dir}", file=sys.stderr)

    finally:
        client.disconnect()


if __name__ == "__main__":
    main()
