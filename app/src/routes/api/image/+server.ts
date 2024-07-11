import { mnemonics } from '$lib/server/database';
import { loadImage } from '$lib/server/loader';

export async function GET({ setHeaders, url }) {
	try {
		const word = url.searchParams.get('word');
		const index = url.searchParams.get('index') ?? '';

		const word_mnemonics = await mnemonics
			.find({ word, image: { $exists: true } })
			.sort({ $natural: -1 })
			.limit(5)
			.toArray();

		if (word_mnemonics.length === 0) {
			return new Response('No mnemonics found for the given word.', { status: 404 });
		}

		const mnemonic = word_mnemonics[Number(index)];
		if (!mnemonic) {
			return new Response('Index out of bounds.', { status: 404 });
		}

		const image = await loadImage(mnemonic.image);
		if (!image) {
			return new Response('Image could not be loaded.', { status: 500 });
		}

		const imageBuffer = Buffer.from(image, 'base64');

		setHeaders({
			'Content-Type': 'image/webp',
			'Content-Length': imageBuffer.length.toString()
		});

		return new Response(imageBuffer);
	} catch (error) {
		console.error(error);
		return new Response('Internal server error.', { status: 500 });
	}
}
