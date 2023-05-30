
import mysql from 'mysql2/promise';

export async function getTimelineFor(username) { // TODO David: Username should be a parameter of the query coming from HTTP (in the JWT token)
    const con = await mysql.createConnection(
        {
            host: "localhost",
            port: 3306,
            user: "root", // TODO David: We want to pass an env var for this instead of hardcoding the user
            password: "root", // TODO David: We want to pass an env var for this instead of hardcoding the password
            database: "twitter"
        }
    )
    const [rows] = await con.query('SELECT * FROM tweets WHERE user = ?', [username]);
    con.destroy();
    return rows;
}