import { mnemonics, meanings } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import type { Meaning } from '$lib/types/Meaning';
import { loadImage, loadDerivatives } from '$lib/server/loader.js';

export const load = async ({ params }) => {
	const { word } = params;
	let word_meanings = await meanings.find({ word }).toArray();

	let word_mnemonics = await mnemonics
		.find({ word, image: { $exists: true } })
		.sort({ $natural: -1 })
		.limit(5)
		.toArray();

	if (word_mnemonics.length > 0) {
		for (const mnemonic of word_mnemonics) {
			mnemonic.image = await loadImage(mnemonic.image);
		}
	}

	const derivatives = await loadDerivatives(word);

	word_mnemonics = word_mnemonics.length > 0 ? JSON.parse(JSON.stringify(word_mnemonics)) : [];
	word_meanings = word_meanings.length > 0 ? JSON.parse(JSON.stringify(word_meanings)) : [];

	const alphabet = 'abc';
	const description = word_meanings
		.map(
			(meaning, index) =>
				`${index + 1}. ${meaning['senses']
					.slice(0, 3)
					.map((sense: { gloss: string }, index: number) => `${alphabet[index]}) ${sense.gloss}`)
					.join(' ')}`
		)
		.join(' ');

	return {
		...params,
		mnemonics: word_mnemonics as Mnemonic[],
		meanings: word_meanings as Meaning[],
		derivatives: derivatives ? derivatives : [],
		title: `${word} meaning • WordSea`,
		description: description,
		image: word_mnemonics.length > 0 ? word_mnemonics[0].image : undefined
	};
};
