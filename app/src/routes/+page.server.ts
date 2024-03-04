import { mnemonics, baseWords } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import { loadImage } from '$lib/server/loader';

const random = (words: string[]) => {
	const date = new Date();
	return (date.getFullYear() * date.getDate() * (date.getMonth() + 1)) % words.length;
};

export const load = async () => {
	const dailyWord = baseWords[random(baseWords)];

	const sampleMnemonics = await mnemonics
		.aggregate([{ $match: { word: dailyWord } }, { $sample: { size: 1 } }])
		.toArray();

	const featured = sampleMnemonics[0];
	featured.image = await loadImage(featured.image);

	return {
		dailyWord: dailyWord,
		featured: JSON.parse(JSON.stringify(featured)) as Mnemonic,
		title: 'WordSea • See the written',
		description:
			'Discover the dictionary featuring mnemonic images, definitions, pronunciation, audio recordings, and word derivatives. Enhance your vocabulary retention effortlessly while grasping the true essence of each word.',
		image: featured.image
	};
};
