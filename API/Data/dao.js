import mysql2 from 'mysql2';
import { config } from 'dotenv';
config()

const connection = mysql2.createConnection({
    host: process.env.DATABASE_HOST,
    port: process.env.DATABASE_PORT,
    database: process.env.DATABASE_NAME,
    user: process.env.DATABASE_USER,
    password: process.env.DATABASE_PASSWORD
})

export {connection}