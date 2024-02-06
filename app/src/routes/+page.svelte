<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';

	export let data;
	const { availableWords } = data;
</script>

<WordsList words={availableWords} />
