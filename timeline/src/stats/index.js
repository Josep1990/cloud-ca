
import {createClient} from 'redis';

export async function userReadTimeline(username) {
    const client = createClient();
    client.on('error', console.log);
    await client.connect();
    await client.lPush('user-stats', `User ${username} has read timeline`);
    return client.disconnect();

}