import { ObjectId } from 'mongodb';

export interface Mnemonic {
	_id: ObjectId;
	word: string;
	prompt: string;
	explanation: string;
	images: string[];
	language_model: string;
	image_model: string;
}
