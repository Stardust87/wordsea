import { gridfs, meanings } from '$lib/server/database';
import type { FSLink } from '$lib/types/FSLink';

export const loadImage = async (image: FSLink) => {
	const stream = gridfs.openDownloadStream(image.data);

	const chunks: Buffer[] = [];
	stream.on('data', (chunk) => {
		chunks.push(chunk);
	});

	let imageString: string = '';
	stream.on('end', () => {
		imageString = Buffer.concat(chunks).toString('base64');
	});

	await new Promise((resolve) => stream.on('end', resolve));
	return imageString;
};

export const loadDerivatives = async (word: string) => {
	const derivatives = await meanings.find({ derived_from: word }).toArray();
	return derivatives.map((meaning) => meaning.word) as string[];
};
