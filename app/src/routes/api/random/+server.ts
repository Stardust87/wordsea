import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
import { mnemonics } from '$lib/server/database';

export const GET = (async () => {
	const randomWord = await mnemonics
		.aggregate([
			{ $match: { image: { $exists: true } } },
			{ $sample: { size: 1 } },
			{ $project: { word: 1, _id: 0 } }
		])
		.toArray();
	const word = randomWord[0].word;
	return json({ word });
}) satisfies RequestHandler;
