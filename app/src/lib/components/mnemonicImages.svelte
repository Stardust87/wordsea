<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let mnemonics: Mnemonic[] = [];

	$: featured = mnemonics[0];
</script>

<div class="relative mb-4 flex w-full flex-col gap-2 lg:w-5/12">
	<div class="group relative">
		<img
			class="group-hover:brightness-25 h-auto max-w-full rounded-lg shadow-lg duration-300"
			src="data:image/png;base64,{featured.images[0]}"
			alt={featured.prompt}
		/>
		<div
			class="absolute inset-x-0 top-0 max-h-full overflow-y-auto p-2 text-slate-300 opacity-0 duration-300 group-hover:opacity-100"
		>
			<p class="font-bold">{featured.prompt}</p>
			<p class="italic">{featured.explanation.replace('prompt', 'image')}</p>
		</div>
	</div>
	<div class="grid grid-cols-4 gap-2">
		{#each mnemonics as mnemo}
			{#if mnemo._id !== featured._id}
				<button class="h-auto max-w-full" on:click={() => (featured = mnemo)}>
					<img
						class=" rounded-lg shadow-lg duration-300 hover:brightness-50"
						src="data:image/png;base64,{mnemo.images[0]}"
						alt={mnemo.prompt}
					/></button
				>
			{/if}
		{/each}
	</div>
</div>
