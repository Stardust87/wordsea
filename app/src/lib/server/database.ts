import { MONGODB_URL, MONGODB_DB_NAME } from '$env/static/private';
import { GridFSBucket, MongoClient } from 'mongodb';

const client = new MongoClient(MONGODB_URL);
const db = client.db(MONGODB_DB_NAME);

export const gridfs = new GridFSBucket(db);
export const mnemonics = db.collection('mnemonics');
export const meanings = db.collection('meanings');

export const baseWords = await meanings
	.aggregate([
		{ $lookup: { from: 'mnemonics', localField: 'word', foreignField: 'word', as: 'mnemonics' } },
		{ $match: { derived_from: { $exists: false }, mnemonics: { $not: { $size: 0 } } } },
		{ $project: { word: true } },
		{ $group: { _id: '$word' } },
		{ $sort: { _id: 1 } }
	])
	.map((doc) => doc._id)
	.toArray();
