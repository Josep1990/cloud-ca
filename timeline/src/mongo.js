import { MongoClient } from "mongodb";

export async function getTimelineFor(username) { // TODO David: Username should be a parameter of the query coming from HTTP (in the JWT token)
    const client = new MongoClient('mongodb://root:secret@localhost:27017/?authMechanism=DEFAULT');
    const twitter = client.db('twitter');
    const tweets = twitter.collection('timeline');
    const tweetsList = await tweets.findOne({'username': username});
    client.close();
    return tweetsList['tweets'];
}
