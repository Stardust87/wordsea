<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';
	import DailyImage from '$lib/components/dailyImage.svelte';

	export let data;
</script>

<div>
	{#if data.mnemonics.length > 0}
		<DailyImage mnemonics={data.mnemonics} randomWord={data.randomWord} />
	{/if}

	<WordsList words={data.availableWords} />
</div>
