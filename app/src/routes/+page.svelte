<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';
	import DailyImage from '$lib/components/dailyImage.svelte';
	import About from '$lib/components/about.svelte';

	export let data;

	$: ({ featured, randomWord, availableWords } = data);
</script>

<div class="flex w-full flex-wrap gap-4 md:flex-nowrap">
	{#if featured}
		<DailyImage {featured} {randomWord} />
	{/if}
	<About />
</div>
<WordsList words={availableWords} />
