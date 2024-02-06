<script lang="ts">
	export let words: string[] = [];
</script>

<div class="flex h-screen items-center justify-center">
	<div class="mx-auto my-4 flex w-3/4 flex-wrap justify-center gap-2">
		{#each words as word}
			<a
				class="rounded bg-violet-500 px-4 py-1 font-medium text-white shadow-md hover:bg-violet-700"
				href="/words/{word}">{word}</a
			>
		{/each}
	</div>
</div>
