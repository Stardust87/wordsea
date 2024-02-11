<script lang="ts">
	import Definition from '$lib/components/definition.svelte';
	import ThemeSwitch from '$lib/components/themeSwitch.svelte';
	import MnemonicImages from '$lib/components/mnemonicImages.svelte';

	export let data;

	$: ({ word, mnemonics, meanings } = data);
</script>

<ThemeSwitch />

<a class="mt-4 block text-lg text-violet-600 underline" href="/">Home</a>

<div>
	<h1 class="text-5xl">{word}</h1>
	<p class="py-1 text-xl font-light dark:text-slate-400">{meanings[0].ipa}</p>

	<MnemonicImages {mnemonics} />
	<Definition {meanings} />
</div>
