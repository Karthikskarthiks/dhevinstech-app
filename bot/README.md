# WhatsApp Bot for Work Updates

## Architecture
Django Website → Supabase DB → Node.js WhatsApp Bot → WhatsApp Group

## Setup Instructions

### 1. Install Dependencies
```bash
cd bot
npm install
```

### 2. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your Supabase details:
```bash
cp .env.example .env
```

### 3. Get WhatsApp Group ID
Run the helper script to get your group ID:
```bash
node get-group-id.js
```
1. Scan the QR code with WhatsApp
2. Note the group ID from the output (format: `1234567890-abcdefg@g.us`)
3. Add it to `.env` as `WHATSAPP_GROUP_ID`

### 4. Start the Bot
```bash
npm start
```

## Deployment Options

### Option A: Local Machine (Recommended for Free)
- Run the bot on your computer or a Raspberry Pi
- Keep it on during scheduled times (11 PM onwards)
- QR login persists in `wwebjs_auth/` folder

### Option B: VPS ($5/month)
- DigitalOcean, Linode, or AWS EC2 micro
- Run with `screen` or `pm2`
```bash
npm install -g pm2
pm2 start bot.js --name whatsapp-bot
pm2 save
pm2 startup
```

### Option C: Render (Free Plan)
Create a `Dockerfile`:
```dockerfile
FROM node:18-alpine
RUN apk add --no-cache chromium
ENV CHROME_PATH=/usr/bin/chromium-browser
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
CMD ["node", "bot.js"]
```

Add to `render.yaml`:
```yaml
services:
  - type: web
    name: whatsapp-bot
    runtime: docker
    dockerfilePath: ./Dockerfile
```

**Note:** Free dynos sleep after 15 minutes. For production, a VPS is recommended.

## Cron Schedule (IST)
- 22:30, 22:35, 22:40, 22:45, 22:50, 22:55

## Troubleshooting

**"Cannot login" after phone number change:**
- Delete `wwebjs_auth/` folder
- Rescan QR code

**"Session expired":**
- Same as above - clear auth and re-login

**"Cannot send to group":**
- Make sure the bot's WhatsApp number is in the group
- Check `WHATSAPP_GROUP_ID` format (ends with `@g.us`)