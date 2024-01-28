<script lang="ts">
	export let data;

	const { availableWords } = data;

	$: ({ word, prompt, images, explanation } = data);
</script>

<div>
	<div class="words">
		{#each availableWords as word}
			<a class="word-link" href="/word/{word}">{word}</a>&nbsp;
		{/each}
	</div>
	<h1>Word {word}</h1>
	<p><strong>prompt</strong> {prompt}</p>
	<p><strong>explanation</strong> {explanation}</p>
	{#each images as image}
		<img src="data:image/png;base64,{image}" alt={prompt} width="512" height="512" />
	{/each}
</div>

<style>
	.words {
		margin-bottom: 1rem;
		display: flex;
		flex-wrap: wrap;
	}
	.word-link {
		margin-right: 0.5rem;
		margin-bottom: 0.5rem;
		padding: 0.1rem;
		border: 1px solid #ccc;
		border-radius: 4px;
		text-decoration: none;
		color: #333;
		background-color: #f5f5f5;
		transition: background-color 0.3s ease;
	}

	.word-link:hover {
		background-color: #e0e0e0;
	}
</style>
