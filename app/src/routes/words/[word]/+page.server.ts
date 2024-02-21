import { mnemonics, meanings } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import type { Meaning } from '$lib/types/Meaning';
import { loadImage, loadDerivatives } from '$lib/server/loader.js';

export const load = async ({ params }) => {
	const { word } = params;
	const word_meanings = await meanings.find({ word }).toArray();

	const hasDerivedFrom = word_meanings
		.map((meaning) => meaning.derived_from)
		.some((val) => val !== undefined);

	let word_mnemonics;
	if (hasDerivedFrom) {
		word_mnemonics = await mnemonics
			.find({ word })
			.sort({
				$natural: -1
			})
			.limit(5)
			.toArray();
	} else {
		word_mnemonics = await mnemonics
			.find({ word, image: { $exists: true } })
			.sort({ $natural: -1 })
			.limit(5)
			.toArray();
	}

	if (word_mnemonics.length > 0) {
		for (const mnemonic of word_mnemonics) {
			mnemonic.image = await loadImage(mnemonic.image);
		}
	}

	const derivatives = await loadDerivatives(word);

	return {
		...params,
		mnemonics:
			word_mnemonics.length > 0
				? (JSON.parse(JSON.stringify(word_mnemonics)) as Array<Mnemonic>)
				: [],
		meanings:
			word_meanings.length > 0 ? (JSON.parse(JSON.stringify(word_meanings)) as Array<Meaning>) : [],
		derivatives: derivatives ? derivatives : []
	};
};
