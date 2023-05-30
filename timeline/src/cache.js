import {createClient} from 'redis';

export async function existsInCache(username) {
    const client = createClient();
    client.on('error', console.log);
    await client.connect();
    const exists = await client.exists(`${username}-timeline`);
    console.log(exists);
    if (exists) {
        return await client.get(`${username}-timeline`);
    }
    await client.disconnect();
    return null;
}

export async function saveInCache(username, value) {
    console.log(`${username}-timeline`);
    const client = createClient();
    client.on('error', console.log);
    await client.connect();
    await client.set(`${username}-timeline`, JSON.stringify(value));
    await client.expire(`${username}-timeline`, 60);
    return client.disconnect();
}