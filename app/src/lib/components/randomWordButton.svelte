<script lang="ts">
	export let word: string;
</script>

<div class="mt-16">
	<a
		class="rounded bg-cyan-600 px-4 py-1 font-medium text-white shadow-md hover:bg-cyan-800"
		href="/words/{word}">{word}</a
	>
</div>
