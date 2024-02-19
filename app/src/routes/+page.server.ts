import { mnemonics  } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import { loadImages } from '$lib/server/loader';



const random = (words: string[]) => {
	const date = new Date();
	return (date.getFullYear() * date.getDate() * (date.getMonth() + 1)) % words.length;
  }

export const load = async () => {
	const availableWords: string[] = await mnemonics.distinct('word');
	const randomWord = availableWords[random(availableWords)];

	const word_mnemonics = await mnemonics.find({word:randomWord}).sort({ $natural: -1 }).limit(5).toArray();
	if (word_mnemonics.length > 0) {
		for (const mnemonic of word_mnemonics) {
			mnemonic.images = await loadImages(mnemonic.images);
		}
	}
	
	return {
		availableWords: availableWords, 
		randomWord: randomWord,
		mnemonics: word_mnemonics.length > 0 ? JSON.parse(JSON.stringify(word_mnemonics)) as Array<Mnemonic> : [],
	};
};
