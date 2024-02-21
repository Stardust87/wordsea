<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';
	import DailyImage from '$lib/components/dailyImage.svelte';

	export let data;

	$: ({ featured, randomWord, availableWords } = data);
</script>

<div>
	{#if featured}
		<DailyImage {featured} {randomWord} />
	{/if}

	<WordsList words={availableWords} />
</div>
