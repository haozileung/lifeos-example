---
name: ledger-manager
description: Manage Ledger double-entry bookkeeping files. Use this skill whenever the user mentions recording transactions (expenses, income, transfers), checking account balances or net worth, generating financial reports (balance, register, expenses, income), budget management, or ANYTHING related to personal finance, accounting, or the Ledger CLI tool. This includes phrases like "record a purchase", "add expense", "check my balance", "how much did I spend", "financial report", "budget tracking", or even general finance management questions where Ledger would be the appropriate tool.
---

# Ledger Manager Skill

管理 Ledger 会计文件，支持双式记账、交易记录和财务报告生成。

## 何时使用此技能

**在以下任何情况下，都应该使用此技能：**

### 交易记录

- 用户想要记录支出、收入、转账
- "记录一笔支出"、"添加收入"、"转账到储蓄账户"
- "买早餐花了25元"、"收到工资10000元"
- "支付房租"、"信用卡还款"

### 查询余额和资产

- 用户想查看账户余额或净资产
- "查看账户余额"、"显示所有资产"、"我现在的净资产是多少"
- "现金还剩多少"、"银行卡余额"
- "总资产有多少"

### 财务报告

- 用户想要财务分析或报告
- "本月支出报告"、"最近交易记录"、"按类别统计支出"
- "收入来源分析"、"支出趋势"
- "月度财务总结"

### 预算管理

- 用户提到预算或财务计划
- "设置预算"、"查看预算执行情况"
- "这个月超支了吗"
- "预算分析"

### 账户管理

- 用户想管理账户结构
- "创建新账户"、"列出所有账户"、"账户结构"
- "账户层级"

### 任何个人财务管理场景

- 即使没有明确提到 "Ledger"，如果用户的需求涉及个人财务记账、会计、追踪资金流向，都应该使用此技能

## 工作流程

使用此技能时，遵循以下步骤：

1. **识别用户意图**：确定用户想要记录交易、查看报告、还是管理账户
2. **检查环境**：
   - 检查是否设置了 `LEDGER_FILE` 环境变量
   - 如果未设置，询问用户 ledger 文件位置或帮助其创建
3. **执行操作**：
   - 对于交易记录：帮助用户格式化交易并添加到 ledger 文件
   - 对于查询：使用适当的 ledger 命令获取信息
   - 对于报告：生成并展示相关财务报告
4. **验证结果**：对于交易记录，验证是否符合双式记账原则

## 功能特性

### 1. 交易管理

- **创建交易**: 添加新的财务交易记录
- **编辑交易**: 修改现有交易
- **删除交易**: 删除指定的交易记录
- **验证交易**: 确保交易符合双式记账原则

### 2. 报告生成

- **余额报告 (balance)**: 查看所有账户的当前余额
- **账簿报告 (register)**: 查看交易明细和运行余额
- **支出报告**: 分析各类支出情况
- **收入报告**: 查看收入来源统计

### 3. 账户管理

- **列出账户**: 显示所有已定义的账户
- **账户结构**: 查看账户层级关系
- **账户余额**: 查看特定账户的余额

### 4. 商品与货币

- **多币种支持**: 支持多种货币记账
- **价格追踪**: 记录商品价格变动
- **货币转换**: 自动进行货币换算

## 使用场景

触发此技能的常见场景：

1. **记录交易**: "记录一笔支出"、"添加收入"、"转账到储蓄账户"
2. **查看余额**: "查看账户余额"、"显示所有资产"、"我现在的净资产是多少"
3. **生成报告**: "本月支出报告"、"最近交易记录"、"按类别统计支出"
4. **账户管理**: "创建新账户"、"列出所有账户"、"账户结构"
5. **查询交易**: "查找特定交易"、"搜索收款人"、"按日期筛选"

## 交易格式

### 基本交易格式

```
YYYY/MM/DD [*|!] [(CODE)] Payee or Description
  Account1  Amount
  Account2  -Amount
```

**示例**：

```
2026/03/07 * 超市购物
  Expenses:Food:Groceries  ¥150.00
  Assets:Cash
```

### 交易状态标记

- `*` - 已清算 (cleared)
- `!` - 待处理 (pending)
- 无标记 - 未清算

### 账户类型

- **Assets (资产)**: Assets:Checking, Assets:Savings, Assets:Cash
- **Liabilities (负债)**: Liabilities:CreditCard, Liabilities:Loan
- **Income (收入)**: Income:Salary, Income:Bonus
- **Expenses (支出)**: Expenses:Food, Expenses:Transport, Expenses:Housing
- **Equity (权益)**: Equity:OpeningBalances

## 常用命令模式

### 查看余额

```bash
ledger balance                    # 所有账户余额
ledger balance ^Assets           # 只显示资产账户
ledger balance ^Expenses --monthly  # 按月显示支出
```

### 查看交易记录

```bash
ledger register                   # 所有交易
ledger register Assets:Checking   # 特定账户交易
ledger register --monthly         # 按月汇总
```

### 生成报告

```bash
ledger -p "this month" balance ^Expenses  # 本月支出
ledger -p "last month" register           # 上月交易
```

## 元数据和标签

### 添加标签

```
2026/03/07 * 收到工资 :Salary:
  Assets:Checking  ¥10000.00
  Income:Salary
```

### 添加元数据

```
2026/03/07 * 购买书籍
  Expenses:Books  ¥89.00
  ; :Tags: reading, self-improvement
  ; Author: 某某
  Assets:Cash
```

## 自动化交易

### 自动交易规则

```
= /^Expenses:Food/
  [Budget:Food]  -1
  [Equity:Budget] 1
```

### 周期性交易

```
~ monthly
  Expenses:Rent  ¥3000.00
  Assets:Checking
```

## 预算和预测

### 预算报告

```bash
ledger --budget balance ^Expenses
```

### 财务预测

```bash
ledger --forecast "yearly" balance ^Assets
```

## 配置文件

### 环境变量

- `LEDGER_FILE`: 主账本文件路径
- `LEDGER_PRICE_DB`: 价格数据库文件路径
- `LEDGER_INIT`: 配置文件路径

### 配置示例

```bash
# ~/.ledgerrc
--price-db ~/finance/pricedb.dat
--wide
--date-format %Y/%m/%d
```

## 最佳实践

1. **账户命名**: 使用冒号分隔的层级结构

   ```
   Assets:Bank:Checking
   Expenses:Food:Groceries
   ```

2. **交易平衡**: 确保每个交易的总额为零

   ```
   2026/03/07 测试
     Expenses:Test  ¥100
     Assets:Cash    ¥-100  # 总和为0
   ```

3. **使用标签**: 通过标签组织和分类交易

   ```
   ; :project:lifeos:
   ; :quarterly:
   ```

4. **定期归档**: 将旧年度数据归档到单独文件
   ```bash
   ledger -f main.dat -b 2020/01/01 -e 2021/01/01 print > 2020.dat
   ```

## 文件组织

建议的目录结构：

```
~/finance/
├── ledger.dat          # 主账本
├── pricedb.dat         # 价格数据库
├── budget.dat          # 预算文件
├── archive/            # 历史归档
│   ├── 2024.dat
│   └── 2023.dat
└── reports/            # 生成的报告
```

## 集成 LifeOS

在 LifeOS 系统中，可以将 Ledger 作为个人财务管理工具：

1. **日常记录**: 在 Daily Notes 中快速记录交易
2. **定期审查**: 在 Weekly/Monthly Notes 中查看财务报告
3. **预算管理**: 使用 Periodic Notes 跟踪预算执行
4. **目标设定**: 在 Yearly Notes 中设定财务目标

## 相关资源

- [Ledger 官方文档](https://ledger-cli.org/doc/ledger3.txt)
- [Ledger 教程](https://ledger-cli.org/)
- [双式记账原理](https://en.wikipedia.org/wiki/Double-entry_bookkeeping)

## 注意事项

1. **备份**: 定期备份 ledger 文件
2. **验证**: 使用 `ledger check` 验证文件格式
3. **版本控制**: 使用 git 追踪账本变更
4. **隐私**: ledger 文件可能包含敏感财务信息，注意保护

## 快速开始

### 对于新用户

如果你是第一次使用 Ledger，按以下步骤开始：

#### 1. 创建初始账本文件

```bash
# 设置 ledger 文件路径环境变量
export LEDGER_FILE=~/finance/ledger.dat

# 或者在 ~/.ledgerrc 中配置
echo "--file ~/finance/ledger.dat" > ~/.ledgerrc
```

#### 2. 设置初始账户和余额

创建一个初始交易来建立账户：

```
; 初始余额设置
2026/01/01 * 开户余额
  Assets:Checking        ¥5000.00
  Assets:Cash            ¥1000.00
  Equity:OpeningBalances
```

#### 3. 记录第一笔交易

```
2026/01/01 * 早餐
  Expenses:Food:Breakfast  ¥25.00
  Assets:Cash
```

#### 4. 验证和查看

```bash
# 验证文件格式
ledger check

# 查看所有账户余额
ledger balance

# 查看交易历史
ledger register
```

### 常见任务快速参考

| 任务         | 命令                                       | 说明                 |
| ------------ | ------------------------------------------ | -------------------- |
| 查看总资产   | `ledger balance ^Assets`                   | 只显示资产账户       |
| 查看本月支出 | `ledger -p "this month" balance ^Expenses` | 本月所有支出         |
| 查看特定账户 | `ledger register Assets:Checking`          | 支票账户交易明细     |
| 查看净资产   | `ledger balance ^Assets ^Liabilities`      | 资产减负债           |
| 按月统计     | `ledger balance --monthly ^Expenses`       | 每月支出汇总         |
| 搜索交易     | `ledger register 超市`                     | 搜索包含"超市"的交易 |
