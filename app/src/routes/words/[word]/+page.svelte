<script lang="ts">
	export let data;

	$: ({ word, prompt, images, explanation } = data);
</script>

<div>
	<h1>Word {word}</h1>
	<p><strong>prompt</strong> {prompt}</p>
	<p><strong>explanation</strong> {explanation}</p>
	{#each images as image}
		<img src="data:image/png;base64,{image}" alt={prompt} width="512" height="512" />
	{/each}
</div>

<a class="home" href="/">Home</a>

<style>
	.home {
		display: block;
		text-align: center;
		margin-top: 1rem;
	}
</style>
