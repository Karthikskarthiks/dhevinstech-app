require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');

const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: './wwebjs_auth'
    })
});

client.on('qr', (qr) => {
    console.log('Scan this QR code to login:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', async () => {
    console.log('Client ready. Fetching chats...');
    
    const chats = await client.getChats();
    console.log('\n=== Your Chats ===');
    chats.forEach(chat => {
        if (chat.isGroup) {
            console.log(`Group: ${chat.name} | ID: ${chat.id._serialized}`);
        } else {
            console.log(`Contact: ${chat.name || chat.id.user} | ID: ${chat.id._serialized}`);
        }
    });
    
    console.log('\nCopy the ID of your target group and add it to .env as WHATSAPP_GROUP_ID');
    process.exit(0);
});

client.initialize();