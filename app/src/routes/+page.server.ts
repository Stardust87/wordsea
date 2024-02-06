import { mnemonics } from "$lib/server/database";

export const load = async ({ params }) => {
    const availableWords = await mnemonics.distinct("word");

    return {
        ...params,
        availableWords,
    }
}