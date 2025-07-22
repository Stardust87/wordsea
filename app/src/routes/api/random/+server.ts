import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
// import { mnemonics } from '$lib/server/database';
import { getBaseWords } from '$lib/server/database';

export const GET = (async () => {
	const words = await getBaseWords();
	const word = words[Math.floor(Math.random() * words.length)];
	return json({ word });
}) satisfies RequestHandler;
