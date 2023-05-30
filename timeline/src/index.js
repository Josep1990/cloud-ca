import Fastify from 'fastify';
import { existsInCache, saveInCache } from './cache.js';
// import { getTimelineFor } from './mysql.js';
import { getTimelineFor } from './mongo.js';
import { userReadTimeline } from './stats/index.js';
import { isTokenValid } from './util.js';

const app = Fastify({
    logger: true
});

app.get('/timeline', async (request, response) => {
    // Task 1: get the username from the token. V
    // Task 2: pass the username into getTimelineFor V
    // Task 3: Reimplement the getTimelineFor with MongoDB

    // the token is in a header called Authorization
    const tokenHeader = request.headers['authorization'];

    // token has the structure of "bearer <token>". We only want <token>
    let token = {};
    try {
        token = isTokenValid(tokenHeader);
    } catch (error) {
        response.code(401).send({ msg: 'Unauthorized'});
    }
        
    // Here we either have:
    // - A token decoded in the variable token.
    // - An exception returned to the user with a 401 because the auth is incorrect.
    console.log(JSON.stringify(token));

    userReadTimeline(token['username']);
    // connect here....
    const cache = await existsInCache(token['username']);
    console.log()
    if (cache) {
        app.log.info('This is being served from the cache');
        return JSON.parse(cache);
    } else {
        const result = await getTimelineFor(token['username']);
        app.log.info('This is being served from the database');
        saveInCache(token['username'], result);
        return result;
    }
});

await app.listen({ port: 8081, host: '0.0.0.0' });
app.log.info('Fastify server started');