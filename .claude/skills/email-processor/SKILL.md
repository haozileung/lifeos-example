---
name: email-processor
description: 读取、筛选和导出IMAP邮件，返回邮件标题和正文。当用户需要检查邮件、获取邮件内容、搜索特定邮件、导出邮件时使用此技能。支持按发件人、日期、主题关键词筛选邮件。
---

# Email Processor Skill

通过IMAP协议读取邮件，返回原始标题和正文内容。

## 何时使用

当用户提到以下需求时触发：

- "检查邮件"、"查看邮件"、"获取邮件内容"
- "搜索邮件"、"查找邮件"、"筛选邮件"
- "按发件人查找"、"按主题搜索"
- "今日邮件"、"最近邮件"
- "重要邮件"、"未读邮件"
- "导出邮件"、"原始邮件"

## 前置条件

**重要**：此技能**使用 .env 文件**存储邮箱凭据。

### 配置步骤

#### 1. 安装依赖

```bash
# Arch Linux
sudo pacman -S python-dotenv

# Ubuntu/Debian
sudo apt install python3-dotenv

# 或使用 pip
pip install python-dotenv
```

#### 2. 创建 .env 文件

```bash
# 复制示例配置
cp .env.example .env

# 编辑配置
nano .env  # 或使用你喜欢的编辑器
```

#### 3. 填入邮箱配置

```bash
# .env 文件内容
IMAP_SERVER=imap.qq.com          # 你的IMAP服务器
IMAP_PORT=993                    # IMAP端口（通常是993）
IMAP_USERNAME=your@email.com     # 你的邮箱地址
IMAP_PASSWORD=your-password      # 密码或授权码
```

**重要提示**：

- ⚠️ **不要将 .env 文件提交到版本控制**
- ⚠️ **QQ邮箱需要使用"授权码"，不是QQ密码**
- ⚠️ **Gmail需要使用"应用专用密码"**

### 脚本路径

从 vault 根目录调用脚本：

```bash
python3 .claude/skills/email-processor/scripts/imap_client.py --help
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10
```

### .env 文件位置

工具按优先级查找 .env 文件：

1. 当前目录：`./.env`
2. 用户主目录：`~/.email-processor.env`
3. 技能目录：`.claude/skills/email-processor/.env`

### 安全建议

```bash
# 设置文件权限（仅所有者可读写）
chmod 600 .env
chmod 600 ~/.email-processor.env

# 添加到 .gitignore
echo ".env" >> .gitignore
echo "*.env" >> .gitignore
```

### 验证配置

（从 vault 根目录执行）

```bash
# 查看帮助
python3 .claude/skills/email-processor/scripts/imap_client.py --help

# 测试连接
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 1
```

## 输出格式说明

- **完整标题**：邮件主题
- **元数据**：发件人、日期
- **邮件内容**：原始内容，不做任何处理

## 核心功能

### 1. 连接IMAP服务器

使用Python的`imaplib`库连接到IMAP服务器：

```python
import imaplib
import email
from email.header import decode_header

# 连接配置
IMAP_SERVER = "imap.gmail.com"  # 或其他IMAP服务器
IMAP_PORT = 993
USERNAME = "user@example.com"
PASSWORD = "app-specific-password"

# 建立连接
mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(USERNAME, PASSWORD)
mail.select("INBOX")
```

### 2. 搜索和筛选邮件

#### 按日期范围

```python
# 今日邮件
since_date = imaplib.Time2Internaldate(now)
mail.search(None, f'(SINCE "{since_date}")')

# 最近7天
mail.search(None, '(SINCE "01-Mar-2026")')
```

#### 按发件人/收件人

```python
# 特定发件人
mail.search(None, '(FROM "sender@example.com")')

# 发送给特定地址
mail.search(None, '(TO "recipient@example.com")')
```

#### 按主题/关键词

```python
# 主题包含关键词
mail.search(None, '(SUBJECT "urgent")')
```

#### 组合条件

```python
# 今日来自特定发件人的邮件
mail.search(None, f'(SINCE "{since_date}" FROM "boss@company.com")')

# 未读邮件
mail.search(None, '(UNSEEN)')
```

### 3. 解析邮件内容

```python
def parse_email(msg):
    """解析邮件对象，提取关键信息"""
    email_data = {
        "from": "",
        "to": "",
        "subject": "",
        "date": "",
        "body": ""
    }

    # 发件人
    email_data["from"] = msg.get("From", "")
    # 收件人
    email_data["to"] = msg.get("To", "")
    # 主题（处理编码）
    subject = msg.get("Subject", "")
    if subject:
        decoded_subject = decode_header(subject)[0]
        if isinstance(decoded_subject[0], bytes):
            email_data["subject"] = decoded_subject[0].decode(decoded_subject[1] or "utf-8")
        else:
            email_data["subject"] = decoded_subject[0]
    # 日期
    email_data["date"] = msg.get("Date", "")

    # 邮件正文（原始内容，不做处理）
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))

            # 跳过附件
            if "attachment" in content_disposition:
                continue

            # 提取第一个正文部分（纯文本或HTML）
            if content_type in ["text/plain", "text/html"]:
                payload = part.get_payload(decode=True)
                if payload:
                    decoded = payload.decode("utf-8", errors="ignore")
                    email_data["body"] = decoded
                    break

    return email_data
```

## 使用流程

1. **获取配置信息**：从用户处获取IMAP服务器和凭据
2. **确定筛选条件**：根据用户需求设置搜索条件
3. **搜索邮件**：使用IMAP SEARCH命令
4. **解析邮件**：提取发件人、主题、日期、正文
5. **导出邮件内容**：返回完整标题和正文

## 输出格式

每封邮件的输出格式：

```markdown
# {邮件主题}

**发件人**: {发件人邮箱}
**日期**: {邮件日期}

---

{邮件正文（原始内容，不做任何处理）}

---
```

**示例输出**：

```markdown
# 招商银行信用卡电子账单

**发件人**: ccsvc@message.cmbchina.com
**日期**: Sun, 8 Mar 2026 09:21:54 +0800 (CST)

---

尊敬的 X 先生，您好！以下是您的 个人消费卡账户03月账单

请您点击阅读《招商银行信用卡章程》（"章程"）、《招商银行信用卡（个人卡）通用领用合约》（"合约"），以确保充分知悉和理解合约及章程内容。

|                       |             |
| --------------------- | ----------- |
| 2026/02/08-2026/03/07 | ¥ 60,000.00 |

|            |          |
| ---------- | -------- |
| ¥ 3,450.34 | ¥ 172.52 |

|            |            |
| ---------- | ---------- |
| 2026/03/25 | ¥ 3,450.34 |

---
```

## 常见IMAP服务器

| 邮箱服务 | IMAP服务器            | 端口 | 特殊配置         |
| -------- | --------------------- | ---- | ---------------- |
| Gmail    | imap.gmail.com        | 993  | 需要应用专用密码 |
| Outlook  | outlook.office365.com | 993  | 可能需要启用IMAP |
| Yahoo    | imap.mail.yahoo.com   | 993  | 需要应用密码     |
| iCloud   | imap.mail.me.com      | 993  | 需要应用专用密码 |
| QQ邮箱   | imap.qq.com           | 993  | 需要授权码       |

## 错误排查

### 连接失败

```
错误: imaplib.error: [AUTHENTICATIONFAILED] Authentication failed.
解决: 检查用户名和密码，Gmail用户使用应用专用密码
```

### 编码错误

```
错误: UnicodeDecodeError
解决: 使用decode(errors='ignore')或尝试多种编码(utf-8, gbk, iso-8859-1)
```

### 搜索无结果

```
确认: 邮箱中确实有符合条件邮件
检查: IMAP搜索语法是否正确（RFC 3501）
测试: 使用简单条件如'(UNSEEN)'测试连接
```

## 命令行参数

从 vault 根目录执行：

```bash
SCRIPT=.claude/skills/email-processor/scripts/imap_client.py

# 基本用法（默认保存到技能目录的 mails 文件夹）
python3 $SCRIPT --limit 10

# 输出到控制台
python3 $SCRIPT --limit 10 --print

# 按日期筛选
python3 $SCRIPT --since "07-Mar-2026"

# 按发件人筛选
python3 $SCRIPT --from "sender@example.com"

# 按主题筛选
python3 $SCRIPT --subject "urgent"

# 仅未读邮件
python3 $SCRIPT --unread

# 保存所有邮件到单个文件
python3 $SCRIPT --limit 10 --output emails.md

# 每封邮件保存到单独文件
python3 $SCRIPT --limit 10 --output-dir ~/Documents/emails

# 分页浏览（第2页，每页20封）
python3 $SCRIPT --page 2 --limit 20

# 控制排序（默认倒序：最新邮件在前）
python3 $SCRIPT --limit 10          # 倒序（默认）
python3 $SCRIPT --limit 10 --reverse # 同上，明确指定倒序
python3 $SCRIPT --limit 10 --no-reverse  # 正序：旧邮件在前
```

### 输出模式说明

**1. 默认模式**（推荐）✨
每封邮件自动保存到技能目录的 `mails/` 文件夹

```bash
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10
# 保存到：.claude/skills/email-processor/mails/
```

**2. 控制台输出** (`--print`)
所有邮件内容直接输出到终端

```bash
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10 --print
```

**3. 单文件模式** (`--output`)
所有邮件合并保存到一个 Markdown 文件

```bash
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10 --output emails.md
```

**4. 自定义目录模式** (`--output-dir`)
每封邮件保存为单独的 Markdown 文件到指定目录

```bash
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10 --output-dir ~/Documents/emails
```

**5. 排序控制** (`--reverse` / `--no-reverse`)
控制邮件的排序方式

```bash
# 倒序（最新邮件在前，默认行为）
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10 --reverse

# 正序（旧邮件在前）
python3 .claude/skills/email-processor/scripts/imap_client.py --limit 10 --no-reverse
```

**说明**：

- **默认行为**：`--reverse` 默认启用，最新邮件优先显示
- **倒序**：邮件ID从大到小排列，新收到的邮件在前
- **正序**：邮件ID从小到大排列，旧邮件在前
- **适用场景**：
  - 查看最新邮件：使用默认倒序
  - 按时间顺序阅读历史邮件：使用 `--no-reverse`

### 文件命名格式

当使用默认模式或 `--output-dir` 时，每封邮件保存为单独文件：

**格式**：`YYYYMMDD-HHMM_邮件主题.md`

**示例**：

```
20260307-1150_是时候再下一单了.md
20260307-1154_资金归集-单笔-全部执行成功邮件.md
20260307-1126_每日信用管家.md
```

**特点**：

- 📅 日期时间前缀便于排序
- 🔒 自动清理特殊字符（/ \ : \* ? " < > |）
- 🔢 自动避免文件名冲突
- 📁 自动创建输出目录

### 默认邮件目录

邮件默认保存在：

```
.claude/skills/email-processor/mails/
```

**重要**：

- ✅ 该目录已加入 `.gitignore`，不会被提交到版本控制
- ✅ 邮件内容可能包含敏感信息，请勿分享
- ✅ 定期清理该目录以释放空间

## 技术依赖

- Python 3.7+
- imaplib (标准库)
- email (标准库)
- python-dotenv (环境变量管理)

**注意**：不再依赖 BeautifulSoup 和 html 库，因为不进行HTML清理。

## 安全提示

⚠️ **重要安全提醒**：

- 永远不要在代码中硬编码密码
- 使用 .env 文件存储凭据
- 建议使用应用专用密码而非账户主密码
- 定期轮换凭据
- 在处理完成后立即断开IMAP连接
- 不要在版本控制中提交包含凭据的文件
