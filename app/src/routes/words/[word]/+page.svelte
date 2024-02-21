<script lang="ts">
	import Definition from '$lib/components/definition.svelte';
	import MnemonicImages from '$lib/components/mnemonicImages.svelte';
	import RecordingPlayer from '$lib/components/recordingPlayer.svelte';
	import Derivation from '$lib/components/derivation.svelte';

	export let data;

	$: ({ word, mnemonics, meanings, derivatives } = data);
</script>

<h1 class="text-5xl">{word}</h1>

{#if meanings.length < 1}
	<p class="pb-2 pt-1 text-xl font-light text-slate-600 dark:text-slate-400">No meanings found</p>
{:else}
	{#if meanings[0].audio && meanings[0].ipa}
		<RecordingPlayer audioUrl={meanings[0].audio} ipa={meanings[0].ipa} />
	{:else if meanings[0].ipa}
		<p class="pb-2 pt-1 text-xl font-light text-slate-600 dark:text-slate-400">{meanings[0].ipa}</p>
	{:else}
		<p class="pb-2 pt-1"></p>
	{/if}

	<div class="flex w-full flex-wrap gap-4 md:flex-nowrap">
		{#if mnemonics.length > 0}
			<MnemonicImages {mnemonics} />
		{/if}
		<div class="w-full md:w-7/12">
			<Definition {meanings} />
			<Derivation derivedFrom={meanings[0].derived_from} {derivatives} />
		</div>
	</div>
{/if}
