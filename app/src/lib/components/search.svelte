<script lang="ts">
	import { onMount } from 'svelte';
	import { clickoutside } from '@svelte-put/clickoutside';
	import { goto } from '$app/navigation';
	import { PUBLIC_TYPESENSE_INDEX } from '$env/static/public';

	import { typesenseInstantSearchAdapter } from '$lib/typesense';
	import instantsearch from 'instantsearch.js';
	import { configure, searchBox, hits } from 'instantsearch.js/es/widgets';

	let hideResults: boolean = true;
	onMount(async () => {
		const typesenseAdapter = typesenseInstantSearchAdapter();
		const searchClient = {
			...typesenseAdapter.searchClient,
			search(requests: any[]) {
				if (requests.every(({ params }) => !params.query)) {
					return Promise.resolve({
						results: requests.map(() => ({
							hits: [],
							nbHits: 0,
							nbPages: 0,
							page: 0,
							processingTimeMS: 0,
							hitsPerPage: 0,
							exhaustiveNbHits: false,
							query: '',
							params: ''
						}))
					});
				}

				return typesenseAdapter.searchClient.search(requests);
			}
		};

		const search = instantsearch({
			indexName: PUBLIC_TYPESENSE_INDEX,
			searchClient,
			future: {
				preserveSharedStateOnUnmount: true
			},
			onStateChange({ uiState, setUiState }) {
				if (
					uiState[PUBLIC_TYPESENSE_INDEX].query === undefined ||
					uiState[PUBLIC_TYPESENSE_INDEX].query === ''
				) {
					hideResults = true;
				} else {
					hideResults = false;
				}

				setUiState(uiState);
			}
		});

		const clearSearch = () => {
			search.renderState[PUBLIC_TYPESENSE_INDEX].searchBox?.clear();
		};

		search.addWidgets([
			configure({
				hitsPerPage: 12,
				distinct: true
			}),
			hits({
				container: '#hits',
				templates: {
					item(hit, { html, components }) {
						return html`<a
							onclick=${clearSearch}
							href="/words/${hit.word}"
							class="block w-full px-2 py-1 focus:bg-cyan-500/25 focus:outline-none"
							>${components.Highlight({ attribute: 'word', hit })}</a
						>`;
					},
					empty(results, { html }) {
						return html`<p class="${hideResults}">No results for ${results.query}</p>`;
					}
				}
			}),
			searchBox({
				container: '#searchbox',
				placeholder: 'Search for words',
				showReset: false,
				showSubmit: false,
				cssClasses: {
					input: [
						'w-full block p-2 text-md text-gray-900 rounded-md shadow-sm bg-slate-100 dark:bg-slate-700/50 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white'
					]
				}
			})
		]);

		search.start();

		const searchForm: HTMLFormElement = document.querySelector(
			'#searchbox form'
		) as HTMLFormElement;

		searchForm?.addEventListener('keydown', (event) => {
			if ((event as KeyboardEvent).key === 'Enter') {
				const firstHit = document.querySelector('#hits a') as HTMLAnchorElement;
				if (firstHit) {
					goto(firstHit.href);
					searchForm.querySelector('input')?.blur();
					clearSearch();
				}
			}
		});

		searchForm?.querySelector('input')?.addEventListener('focus', () => {
			const query = search.renderState[PUBLIC_TYPESENSE_INDEX].searchBox?.query;
			if (query !== undefined && query !== '') {
				hideResults = false;
			}
		});

		const handleKeydown = (event: KeyboardEvent) => {
			if (event.key === 'ArrowDown' || event.key === 'ArrowUp') {
				event.preventDefault();
				const hits = document.querySelectorAll('#hits a') as NodeListOf<HTMLAnchorElement>;
				const currentFocusedIndex = Array.from(hits).findIndex(
					(hit) => hit === document.activeElement
				);

				let nextIndex =
					(currentFocusedIndex + (event.key === 'ArrowDown' ? 1 : -1) + hits.length) % hits.length;

				if (currentFocusedIndex === -1 && event.key === 'ArrowUp') {
					nextIndex += 1;
				}
				if (currentFocusedIndex === 0 && event.key === 'ArrowUp') {
					searchForm.querySelector('input')?.focus();
				} else {
					hits[nextIndex]?.focus();
				}
			}

			if (event.key === 'Escape') {
				hideResults = true;
				searchForm.querySelector('input')?.blur();
			}
		};

		const wrapper = document.querySelector('#searchbar') as HTMLDivElement;
		wrapper.addEventListener('keydown', handleKeydown);
	});
</script>

<div
	id="searchbar"
	class="relative w-full grow min-[480px]:mx-4 min-[480px]:w-auto sm:w-96 sm:grow-0"
	use:clickoutside
	on:clickoutside={() => {
		hideResults = true;
	}}
>
	<div id="searchbox"></div>
	<div
		class="{hideResults
			? 'hide-results'
			: ''} absolute top-full z-50 mt-1 w-full rounded-md bg-slate-100 shadow-md dark:bg-slate-700"
		id="hits"
	></div>
</div>

<style>
	:global(.hide-results) {
		display: none;
	}

	:global(#hits mark) {
		background-color: transparent;
		font-weight: 800;
		color: inherit;
	}
</style>
