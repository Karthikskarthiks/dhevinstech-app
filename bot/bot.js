require('dotenv').config();
const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const cron = require('node-cron');
const { Pool } = require('pg');

const pool = new Pool({
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '6543'),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    ssl: { rejectUnauthorized: false }
});

const client = new Client({
    authStrategy: new LocalAuth({
        dataPath: './wwebjs_auth'
    })
});

client.on('qr', (qr) => {
    console.log('QR Code received - scan to login:');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp client is ready!');
    startScheduler();
});

client.on('authenticated', () => {
    console.log('WhatsApp client authenticated');
});

client.on('auth_failure', (msg) => {
    console.error('Authentication failed:', msg);
});

client.initialize();

function formatWorkDetail(wd) {
    const labours = wd.labours.join(', ');
    const vendor = wd.vendor || 'N/A';
    const site = `${wd.site_name} - ${wd.site_location}`;
    
    let msg = `*WORK UPDATE* - ${wd.date}\n`;
    msg += `📍 Site: ${site}\n`;
    msg += `👷 Labours: ${labours}\n`;
    msg += `🏢 Vendor: ${vendor}\n`;
    msg += `📝 Work: ${wd.work_description}\n`;
    
    if (wd.material_description) {
        msg += `🧱 Material: ${wd.material_description}\n`;
    }
    if (wd.check_in) {
        msg += `🕐 Check-in: ${wd.check_in}\n`;
    }
    if (wd.check_out) {
        msg += `🕐 Check-out: ${wd.check_out}\n`;
    }
    
    return msg;
}

async function getUnsentUpdates() {
    const today = new Date().toISOString().split('T')[0];
    
    const query = `
        SELECT 
            wd.id,
            wd.date,
            wd.work_description,
            wd.material_description,
            wd.check_in,
            wd.check_out,
            wd.sent_to_whatsapp,
            v.name as vendor,
            s.site_name,
            s.location as site_location,
            json_agg(l.name) as labours
        FROM mywork_workdetail wd
        LEFT JOIN mywork_vendor v ON wd.vendor_id = v.id
        LEFT JOIN mywork_site s ON wd.site_id = s.id
        LEFT JOIN mywork_workdetail_labours wl ON wd.id = wl.workdetail_id
        LEFT JOIN mywork_labour l ON wl.labour_id = l.id
        WHERE wd.sent_to_whatsapp = false 
        AND wd.date = $1
        GROUP BY wd.id, v.name, s.site_name, s.location
        ORDER BY wd.created_at ASC
    `;
    
    const result = await pool.query(query, [today]);
    return result.rows;
}

async function markAsSent(ids) {
    if (ids.length === 0) return;
    
    const query = `
        UPDATE mywork_workdetail 
        SET sent_to_whatsapp = true 
        WHERE id = ANY($1)
    `;
    
    await pool.query(query, [ids]);
}

async function sendWorkUpdates() {
    try {
        const chatId = process.env.WHATSAPP_GROUP_ID;
        if (!chatId) {
            console.error('WHATSAPP_GROUP_ID not configured in .env');
            return;
        }

        const unsent = await getUnsentUpdates();
        console.log(`Found ${unsent.length} unsent updates`);

        if (unsent.length === 0) {
            console.log('No updates to send');
            return;
        }

        const sentIds = [];
        for (const wd of unsent) {
            try {
                const message = formatWorkDetail(wd);
                await client.sendMessage(chatId, message);
                sentIds.push(wd.id);
                console.log(`Sent update ${wd.id} for ${wd.date}`);
                await new Promise(resolve => setTimeout(resolve, 2000));
            } catch (err) {
                console.error(`Failed to send update ${wd.id}:`, err.message);
            }
        }

        if (sentIds.length > 0) {
            await markAsSent(sentIds);
            console.log(`Marked ${sentIds.length} updates as sent`);
        }
    } catch (err) {
        console.error('Error sending updates:', err);
    }
}

function startScheduler() {
    console.log('Starting cron scheduler...');
    
    cron.schedule('30 17 * * *', () => {
        console.log('Running scheduled job at 22:30 IST (17:00 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('5 17 * * *', () => {
        console.log('Running scheduled job at 22:05 IST (17:05 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('10 17 * * *', () => {
        console.log('Running scheduled job at 22:10 IST (17:10 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('15 17 * * *', () => {
        console.log('Running scheduled job at 22:15 IST (17:15 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('20 17 * * *', () => {
        console.log('Running scheduled job at 22:20 IST (17:20 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('25 17 * * *', () => {
        console.log('Running scheduled job at 22:25 IST (17:25 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('35 17 * * *', () => {
        console.log('Running scheduled job at 22:35 IST (17:35 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('40 17 * * *', () => {
        console.log('Running scheduled job at 22:40 IST (17:40 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('45 17 * * *', () => {
        console.log('Running scheduled job at 22:45 IST (17:45 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('50 17 * * *', () => {
        console.log('Running scheduled job at 22:50 IST (17:50 UTC)');
        sendWorkUpdates();
    });

    cron.schedule('55 17 * * *', () => {
        console.log('Running scheduled job at 22:55 IST (17:55 UTC)');
        sendWorkUpdates();
    });

    console.log('Cron jobs scheduled every 5 minutes starting 22:30 IST');
}

process.on('SIGINT', async () => {
    console.log('Shutting down...');
    await pool.end();
    await client.destroy();
    process.exit(0);
});