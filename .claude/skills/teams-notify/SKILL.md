---
name: teams-notify
description: Send notifications to Microsoft Teams channels via Power Automate webhook. Use this skill whenever the user asks to send messages to Teams, notify a Teams channel, push updates to Teams, or post to Microsoft Teams - even if they don't explicitly use the word "webhook". This handles the webhook POST request and provides clear feedback.
---

# Teams Notification Skill

This skill sends messages to Microsoft Teams channels through a Power Automate webhook URL using Adaptive Card format.

## How It Works

The skill makes a POST request to a pre-configured Power Automate webhook, which then forwards the message to a Teams channel. This is useful for:

- Sending notifications from scripts or automations
- Posting updates to team channels
- Alerting team members about important events
- Integrating other tools with Teams

## Required Parameters

- **message** (required): The message content to send. Supports a [Commonmark subset](https://learn.microsoft.com/en-us/adaptive-cards/authoring-cards/text-features): **bold**, _italic_, lists, and `[links](url)`. Use `\r` for line breaks in lists.

## Optional Parameters

- **title** (optional): A title or heading for the message. Useful for providing context.

## Webhook Configuration

The webhook URL is read from the environment variable **`TEAMS_WEBHOOK_URL`**.

- **Source**: `.env` file in the vault root (git-ignored, not committed)
- **Format**: `TEAMS_WEBHOOK_URL=https://...`

**IMPORTANT**: Before sending, always verify the variable is set. If not, error out:

```bash
if [ -z "${TEAMS_WEBHOOK_URL:-}" ]; then
  echo "Error: TEAMS_WEBHOOK_URL not set. Add it to .env in the vault root."
  exit 1
fi
```

## Request Format

**IMPORTANT**: The webhook requires **Adaptive Card** format (not simple JSON). TextBlock content follows [Adaptive Cards text features](https://learn.microsoft.com/en-us/adaptive-cards/authoring-cards/text-features)—use `\r` for line breaks in lists.

### Basic Format (message only)

```json
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": null,
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "Your message here with **markdown** support",
            "wrap": true
          }
        ]
      }
    }
  ]
}
```

### Format with Title

```json
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": null,
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "TITLE",
            "size": "Large",
            "weight": "Bolder",
            "wrap": true
          },
          {
            "type": "TextBlock",
            "text": "MESSAGE",
            "wrap": true
          }
        ]
      }
    }
  ]
}
```

## Step-by-Step Process

### 1. Extract Parameters

From the user's request, identify:

- The message content (required)
- Any title or heading (optional)

If the message is not clearly specified, ask the user to provide it.

### 2. Prepare the Payload

Create an Adaptive Card JSON object. Always use a file to avoid JSON escaping issues.

**With title:**

```bash
cat > /tmp/teams_payload.json << 'EOF'
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": null,
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "TITLE",
            "size": "Large",
            "weight": "Bolder",
            "wrap": true
          },
          {
            "type": "TextBlock",
            "text": "MESSAGE",
            "wrap": true
          }
        ]
      }
    }
  ]
}
EOF
```

**Without title (message only):**

```bash
cat > /tmp/teams_payload.json << 'EOF'
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "contentUrl": null,
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.2",
        "body": [
          {
            "type": "TextBlock",
            "text": "MESSAGE",
            "wrap": true
          }
        ]
      }
    }
  ]
}
EOF
```

### 3. Send the Request

Use curl to send a POST request to the webhook:

```bash
# Verify webhook URL is available
if [ -z "${TEAMS_WEBHOOK_URL:-}" ]; then
  echo "Error: TEAMS_WEBHOOK_URL not set. Add it to .env in the vault root."
  exit 1
fi

curl -X POST "$TEAMS_WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d @/tmp/teams_payload.json \
  -w "\n\nHTTP Status: %{http_code}\n"
# Then delete the file
rm /tmp/teams_payload.json
```

### 4. Interpret the Response

- **Success**: The webhook typically returns a 200 OK or 202 Accepted response. Inform the user that the message was sent successfully.
- **Failure**: Check for common issues:
  - Connection errors (network problems)
  - 4xx errors (invalid request format)
  - 5xx errors (Power Automate/Teams service issues)

Provide clear feedback about what happened.

## Text Formatting (Adaptive Cards)

Adaptive Cards `TextBlock` supports a **Commonmark subset** only. Follow [Microsoft's Text Features spec](https://learn.microsoft.com/en-us/adaptive-cards/authoring-cards/text-features) for compatibility.

### Supported Markdown

| Style         | Syntax                | Example                                      |
| ------------- | --------------------- | -------------------------------------------- |
| **Bold**      | `**text**`            | `**Important**`                              |
| _Italic_      | `_text_`              | `_emphasis_`                                 |
| Bullet list   | `- Item 1\r- Item 2`  | Use `- ` prefix + `\r` between items         |
| Numbered list | `1. First\r2. Second` | Use `\r` between items                       |
| Hyperlinks    | `[Title](url)`        | `[Adaptive Cards](https://adaptivecards.io)` |

### List Formatting Rules

**CRITICAL**: Lists MUST follow these rules to render correctly in Teams:

1. **Use `- ` (markdown dash) prefix**, NOT `• ` (bullet character). Teams renderer only recognizes `- ` as a list marker.
2. **Use `\r` (JSON carriage return) between items**. In the heredoc, write `\r` literally — JSON parses it as a carriage return (0x0D).
3. **Set `"wrap": true`** on every TextBlock that contains lists.
4. **All list items go in ONE TextBlock** — do not split into separate TextBlocks.

**Correct ✅:**
```json
{
  "type": "TextBlock",
  "text": "- 完成任务 A\r- 进行中任务 B\r- 待启动任务 C",
  "wrap": true
}
```

**Wrong ❌:**
```json
{
  "type": "TextBlock",
  "text": "• 项目 A\r• 项目 B",
  "wrap": true
}
```
> `• ` (Unicode bullet) is NOT a markdown list marker — Teams renders it as plain text, showing as one block.

### Structured Message Layout (Recommended)

For messages with sections (title + paragraphs + lists), use **multiple TextBlock elements** with appropriate `"spacing"` and `"weight"`:

```json
{
  "body": [
    {
      "type": "TextBlock",
      "text": "周报 - 2026-W16",
      "size": "Large",
      "weight": "Bolder",
      "wrap": true
    },
    {
      "type": "TextBlock",
      "text": "✅ 本周完成",
      "weight": "Bolder",
      "wrap": true,
      "spacing": "medium"
    },
    {
      "type": "TextBlock",
      "text": "- 项目 A 完成\r- 项目 B 完成\r- 项目 C 完成",
      "wrap": true,
      "spacing": "small"
    },
    {
      "type": "TextBlock",
      "text": "📌 下周计划",
      "weight": "Bolder",
      "wrap": true,
      "spacing": "medium"
    },
    {
      "type": "TextBlock",
      "text": "- 任务 X\r- 任务 Y",
      "wrap": true,
      "spacing": "small"
    }
  ]
}
```

**Spacing options**: `default`, `none`, `small`, `medium`, `large`, `extraLarge`, `padding`.

### Not Supported

- Headers (`##`, `###`)
- Tables
- Images
- Code blocks (`` `code` ``)
- `• ` (Unicode bullet character) as list marker

### Date/Time Formatting (optional)

For localized date/time, use `{{DATE(...)}}` and `{{TIME(...)}}`:

- `{{DATE(2017-02-14T06:00:00Z, SHORT)}}` → "Mon, Feb 14th, 2017"
- `{{TIME(2017-02-14T06:00:00Z)}}` → "6:00 AM"

Rules: **CASE SENSITIVE**, no spaces inside `{{}}`, strict RFC 3339 format.

## Examples

### Example 1: Simple message

**User says**: "Send 'Hello team!' to teams"

**Process**:

1. Extract message: "Hello team!"
2. No title provided
3. Create Adaptive Card with single TextBlock containing the message
4. Send using curl with -d @/tmp/teams_payload.json
5. Report success

### Example 2: Message with title

**User says**: "Notify teams about deployment: 'Production deployment completed successfully'"

**Process**:

1. Extract title: "Deployment Notification"
2. Extract message: "Production deployment completed successfully"
3. Create Adaptive Card with title (large, bold) and message
4. Send using curl with -d @/tmp/teams_payload.json
5. Report success

### Example 3: Formatted message (list)

**User says**: "Send to teams with title 'Daily Update':

- Completed task A
- Working on task B
- Blocked on task C"

**Process**:

1. Extract title: "Daily Update"
2. Format message as: `- Completed task A\r- Working on task B\r- Blocked on task C` (use `- ` prefix + `\r` between items, NOT `• `)
3. Create Adaptive Card with `"wrap": true` on TextBlock
4. Send using curl with -d @/tmp/teams_payload.json
5. Report success

## Troubleshooting

### Common Issues

**"Property 'type' must be 'AdaptiveCard'" error**

- Make sure the JSON structure follows the Adaptive Card schema exactly
- The content.type must be "AdaptiveCard"
- The outer type must be "message"
- Check that contentType is "application/vnd.microsoft.card.adaptive"

**"400 Bad Request"**

- The JSON payload may be malformed
- Ensure Content-Type is set to application/json
- Check that all required fields are present
- Use a file (-d @file.json) to avoid shell escaping issues

**"401 Unauthorized" or "403 Forbidden"**

- The webhook signature may have expired
- The Power Automate flow may need to be reconfigured

**"500 Internal Server Error"**

- Power Automate or Teams service issue
- Wait and retry, or check Power Automate flow status

### Debugging Tips

1. Always use a file for the payload (-d @file.json) to avoid escaping issues
2. Show the response status code and body
3. If the request fails, provide specific error details
4. Suggest next steps for resolving the issue

## Important Notes

- The webhook URL is stored in `TEAMS_WEBHOOK_URL` environment variable (`.env` file), never hardcoded
- Messages are sent asynchronously - immediate success response means the request was accepted, not necessarily delivered
- There may be a slight delay between sending and the message appearing in Teams
- Character limits may apply depending on Power Automate/Teams configuration
- Always use the Adaptive Card format as required by Power Automate "When a Teams webhook request is received" trigger
- The wrap: true property is important for proper text wrapping in Teams
