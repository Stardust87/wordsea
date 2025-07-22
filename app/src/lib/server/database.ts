import { MONGODB_URL, MONGODB_DB_NAME } from '$env/static/private';
import { GridFSBucket, MongoClient } from 'mongodb';
import { Chance } from 'chance';

const client = new MongoClient(MONGODB_URL);
const db = client.db(MONGODB_DB_NAME);

export const gridfs = new GridFSBucket(db);
export const mnemonics = db.collection('mnemonics');
export const meanings = db.collection('meanings');

let _baseWords: string[] | null = null;

export async function getBaseWords(): Promise<string[]> {
	if (_baseWords === null) {
		let baseWords = await meanings.distinct('word', { derived_from: { $exists: false } });
		const wordsWithImage = await mnemonics
			.find({ image: { $exists: true } })
			.map((doc) => doc.word)
			.toArray();

		baseWords = baseWords.filter((word) => wordsWithImage.includes(word));
		_baseWords = new Chance(42).shuffle(baseWords);
	}
	return _baseWords;
}

// For backward compatibility, export a getter function
export const baseWords = {
	async get(): Promise<string[]> {
		return await getBaseWords();
	}
};
