export interface Meaning {
    word: string;
    pos: string;
    senses: {
        gloss: string;
        examples?: {
            text: string;
        }[];
    }[];
    forms: {
        third_person?: string;
        present_participle?: string;
        past_participle?: string;
        plural?: string;
        comparative?: string;
        superlative?: string;
    };
    }

