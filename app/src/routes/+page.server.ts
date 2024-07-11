import { mnemonics, baseWords } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import { loadImage } from '$lib/server/loader';

const random = (words: string[]) => {
	const date = new Date();
	return (date.getFullYear() * date.getDate() * (date.getMonth() + 1)) % words.length;
};

export const load = async ({ url }) => {
	const dailyWord = baseWords[random(baseWords)];

	const dailyMnemonics = await mnemonics
		.find({ word: dailyWord })
		.sort({ $natural: -1 })
		.limit(1)
		.toArray();

	const featured = dailyMnemonics[0];
	featured.image = await loadImage(featured.image);

	const ogImageUrl = `${url.origin}/api/image?word=${dailyWord}&index=0`;

	return {
		dailyWord: dailyWord,
		featured: JSON.parse(JSON.stringify(featured)) as Mnemonic,
		title: 'WordSea • See the written',
		description:
			'Discover the dictionary featuring mnemonic images, definitions, pronunciation, audio recordings, and word derivatives. Enhance your vocabulary retention effortlessly while grasping the true essence of each word.',
		image: ogImageUrl
	};
};
