<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';

	export let data;
</script>

<WordsList words={data.availableWords} />
