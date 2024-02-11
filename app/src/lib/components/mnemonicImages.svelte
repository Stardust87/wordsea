<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let mnemonics: Mnemonic[] = [];
</script>

{#each mnemonics as mnemo}
	<p>
		<span class="font-medium"> prompt </span> <span class="italic"> {mnemo.prompt} </span>
	</p>
	<div class="my-4 flex flex-wrap items-center gap-4">
		{#each mnemo.images as image}
			<img
				class="rounded-lg shadow-lg"
				src="data:image/png;base64,{image}"
				alt={mnemo.prompt}
				width="384"
				height="384"
				title={mnemo.explanation}
			/>
		{/each}
	</div>
{/each}
