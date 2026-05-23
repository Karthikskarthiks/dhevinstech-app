const { Pool } = require('pg');
require('dotenv').config();

const pool = new Pool({
    host: process.env.DB_HOST,
    port: parseInt(process.env.DB_PORT || '6543'),
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME,
    ssl: { rejectUnauthorized: false }
});

async function resetSentFlags() {
    try {
        const result = await pool.query(
            'UPDATE mywork_workdetail SET sent_to_whatsapp = false WHERE date = CURRENT_DATE'
        );
        console.log(`Reset ${result.rowCount} records to unsent`);
    } catch (err) {
        console.error('Error:', err);
    } finally {
        await pool.end();
    }
}

resetSentFlags();