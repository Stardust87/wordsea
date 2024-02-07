<script lang="ts">
	import WordsList from '$lib/components/wordsList.svelte';
	import ThemeSwitch from '$lib/components/themeSwitch.svelte';

	export let data;
	const { availableWords } = data;
</script>

<ThemeSwitch />
<WordsList words={availableWords} />
