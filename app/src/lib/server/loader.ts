import { gridfs  } from '$lib/server/database';
import type { FSLink } from '$lib/types/FSLink';

export const loadImages = async (images: FSLink[]) => {
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