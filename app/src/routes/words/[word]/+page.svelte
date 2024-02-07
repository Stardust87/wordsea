<script lang="ts">
	import Definition from '$lib/components/definition.svelte';
	import ThemeSwitch from '$lib/components/themeSwitch.svelte';
	export let data;

	$: ({ word, prompt, images, explanation, meanings } = data);
</script>

<ThemeSwitch />

<a class="mt-4 block text-lg text-violet-600 underline" href="/">Home</a>

<div>
	<h1 class="text-5xl">{word}</h1>
	<p><span class="font-medium"> prompt </span> <span class="italic"> {prompt} </span></p>

	<div class="my-4 flex flex-wrap items-center gap-4">
		{#each images as image}
			<img
				class="rounded-lg shadow-lg"
				src="data:image/png;base64,{image}"
				alt={prompt}
				width="384"
				height="384"
				title={explanation}
			/>
		{/each}
	</div>

	<Definition {meanings} />
</div>
