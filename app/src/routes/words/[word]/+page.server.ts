import { mnemonics, gridfs } from "$lib/server/database";

export const load = async ({ params }) => {
    const { word } = params;

    const mnemo = await mnemonics.findOne({ word }, { sort: { $natural: -1 } });
    const images: string[] = [];

    if (mnemo?.images) {
        for (const image of mnemo.images) {
            const imageId = image.data;
            const stream = gridfs.openDownloadStream(imageId);

            const chunks: Buffer[] = [];
            stream.on('data', (chunk) => {
                chunks.push(chunk);
            });
            stream.on('end', () => {
                const img = Buffer.concat(chunks).toString('base64');
                images.push(img);
            });
            await new Promise((resolve) => stream.on('end', resolve));
        }
    }


    return {
        ...params,
        prompt: mnemo?.prompt,
        explanation: mnemo?.explanation,
        images,
    }
}