import { MONGODB_URL, MONGODB_DB_NAME } from "$env/static/private";
import { GridFSBucket, MongoClient } from "mongodb";

const client = new MongoClient(MONGODB_URL);
const db = client.db(MONGODB_DB_NAME);

export const gridfs = new GridFSBucket(db);
export const mnemonics = db.collection("mnemonics");
export const words = db.collection("words");