export interface Meaning {
    word: string;
    pos: string;
    senses: {
        gloss: string;
        examples?: {
            text: string;
        }[];
    }[];
}
