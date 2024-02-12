<script lang="ts">
	import Definition from '$lib/components/definition.svelte';
	import ThemeSwitch from '$lib/components/themeSwitch.svelte';
	import MnemonicImages from '$lib/components/mnemonicImages.svelte';
	import RecordingPlayer from '$lib/components/recordingPlayer.svelte';

	export let data;

	$: ({ word, mnemonics, meanings } = data);
</script>

<ThemeSwitch />

<a class="mt-4 block text-lg text-violet-600 underline" href="/">Home</a>
<h1 class="text-5xl">{word}</h1>
{#if meanings[0].audio}
	<RecordingPlayer audioUrl={meanings[0].audio} ipa={meanings[0].ipa} />
{:else}
	<p class="pb-2 pt-1 text-xl font-light text-slate-600 dark:text-slate-400">{meanings[0].ipa}</p>
{/if}

<div class="flex w-full flex-wrap gap-4 md:flex-nowrap">
	<MnemonicImages {mnemonics} />
	<Definition {meanings} />
</div>
