<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';
	import DailyImage from '$lib/components/dailyImage.svelte';
	import About from '$lib/components/about.svelte';

	export let data;

	$: ({ featured, randomWord, availableWords } = data);
</script>

<div class="mt-4 flex w-full flex-wrap gap-4 md:mt-8 md:flex-nowrap">
	<About />
	{#if featured}
		<DailyImage {featured} {randomWord} />
	{/if}
</div>
<!-- <WordsList words={availableWords} /> -->
