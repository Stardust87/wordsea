import { MONGODB_URL, MONGODB_DB_NAME } from '$env/static/private';
import { GridFSBucket, MongoClient } from 'mongodb';

const client = new MongoClient(MONGODB_URL);
const db = client.db(MONGODB_DB_NAME);

export const gridfs = new GridFSBucket(db);
export const mnemonics = db.collection('mnemonics');
export const meanings = db.collection('meanings');
let baseWords = await meanings
	.find({ derived_from: { $exists: false } })
	.map((doc) => doc.word)
	.toArray();

const wordsWithImage = await mnemonics
	.find({ image: { $exists: true } })
	.map((doc) => doc.word)
	.toArray();

baseWords = baseWords.filter((word) => wordsWithImage.includes(word));
export { baseWords };
