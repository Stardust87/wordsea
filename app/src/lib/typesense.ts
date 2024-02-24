import {
	PUBLIC_TYPESENSE_SEARCH_ONLY_API_KEY,
	PUBLIC_TYPESENSE_HOST,
	PUBLIC_TYPESENSE_PORT,
	PUBLIC_TYPESENSE_PROTOCOL
} from '$env/static/public';

import TypesenseInstantSearchAdapter from 'typesense-instantsearch-adapter';

export const typesenseInstantSearchAdapter = () =>
	new TypesenseInstantSearchAdapter({
		server: {
			apiKey: PUBLIC_TYPESENSE_SEARCH_ONLY_API_KEY,
			nodes: [
				{
					host: PUBLIC_TYPESENSE_HOST,
					port: parseInt(PUBLIC_TYPESENSE_PORT),
					protocol: PUBLIC_TYPESENSE_PROTOCOL
				}
			]
		},
		additionalSearchParameters: {
			query_by: 'word,forms',
			prioritize_token_position: true,
			num_typos: 2,
			sort_by: '_text_match:desc, word:asc'
		}
	});
