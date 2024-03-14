import { json } from '@sveltejs/kit';
import type { RequestHandler } from './$types';
// import { mnemonics } from '$lib/server/database';
import { baseWords } from '$lib/server/database'


export const GET = (async () => {
	const word = baseWords[Math.floor(Math.random() * baseWords.length)];
	return json({ word });
}) satisfies RequestHandler;
