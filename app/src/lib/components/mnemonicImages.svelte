<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let mnemonics: Mnemonic[] = [];

	$: featured = mnemonics[0];
</script>

<div class="relative flex w-full flex-col gap-2 md:w-5/12">
	<div class="group relative">
		<img
			class="group-hover:brightness-25 h-auto max-w-full rounded-lg shadow-lg duration-300"
			src="data:image/webp;base64,{featured.image}"
			alt={featured.prompt}
		/>
		<div
			class="absolute inset-x-0 top-0 max-h-full overflow-y-auto p-2 text-slate-300 opacity-0 duration-300 group-hover:opacity-100"
		>
			<span class="text-violet-500">{featured.language_model}-{featured.image_model}</span>
			<p class="italic">{featured.prompt}</p>
			<p class="font-bold">{featured.explanation.replace('prompt', 'image')}</p>
		</div>
	</div>
	{#if mnemonics.length > 1}
		<div class="grid grid-cols-4 gap-2">
			{#each mnemonics as mnemo}
				{#if mnemo._id !== featured._id}
					<button class="h-auto max-w-full" on:click={() => (featured = mnemo)}>
						<img
							class="rounded-lg shadow-md duration-300 hover:brightness-50"
							src="data:image/webp;base64,{mnemo.image}"
							alt={mnemo.prompt}
						/></button
					>
				{/if}
			{/each}
		</div>
	{/if}
</div>
