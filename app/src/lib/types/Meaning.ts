import { ObjectId } from 'mongodb';

export interface Meaning {
	_id: ObjectId;
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
	ipa: string;
	audio: string;
	derived_from: string;
}
