import { mnemonics, meanings, gridfs } from "$lib/server/database";
import type { Meaning } from "$lib/types/Meaning.ts";

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

    const word_meanings_db = await meanings.find({ word }, { projection: { _id: false } }).toArray();
    const word_meanings: Meaning[] = JSON.parse(JSON.stringify(word_meanings_db));

    return {
        ...params,
        prompt: mnemo?.prompt,
        explanation: mnemo?.explanation,
        meanings: word_meanings,
        images,
    }
}