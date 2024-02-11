import { mnemonics, meanings, gridfs } from '$lib/server/database';
import type { Mnemonic } from '$lib/types/Mnemonic';
import type { Meaning } from '$lib/types/Meaning';
import type { FSLink } from '$lib/types/FSLink';

const loadImages = async (images: FSLink[]) => {
	const imagesData: string[] = [];
	for (const image of images) {
		const stream = gridfs.openDownloadStream(image.data);

		const chunks: Buffer[] = [];
		stream.on('data', (chunk) => {
			chunks.push(chunk);
		});
		stream.on('end', () => {
			const img = Buffer.concat(chunks).toString('base64');
			imagesData.push(img);
		});
		await new Promise((resolve) => stream.on('end', resolve));
	}
	return imagesData;
};

export const load = async ({ params }) => {
	const { word } = params;

	const word_mnemonics = await mnemonics.find({ word }).toArray();
	for (const mnemonic of word_mnemonics) {
		mnemonic.images = await loadImages(mnemonic.images);
	}

	const word_meanings = await meanings.find({ word }).toArray();

	return {
		...params,
		mnemonics: JSON.parse(JSON.stringify(word_mnemonics)) as Array<Mnemonic>,
		meanings: JSON.parse(JSON.stringify(word_meanings)) as Array<Meaning>
	};
};
