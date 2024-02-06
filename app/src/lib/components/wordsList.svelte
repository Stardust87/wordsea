<script lang="ts">
	export let words: string[] = [];
</script>

<div class="words">
	{#each words as word}
		<a class="word-link" href="/words/{word}">{word}</a>&nbsp;
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
