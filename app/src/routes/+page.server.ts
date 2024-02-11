import { mnemonics } from '$lib/server/database';

export const load = async () => {
	const availableWords: string[] = await mnemonics.distinct('word');

	return {
		availableWords
	};
};
