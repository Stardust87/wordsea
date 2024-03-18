<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let featured: Mnemonic;
	export let word: string = '';
</script>

<div class="flex h-auto w-full flex-col gap-2 rounded-lg md:w-1/2">
	<div class="relative my-auto">
		<a href="/words/{word}" class="rounded-lg">
			<img
				class=" h-auto max-w-full rounded-lg shadow-xl duration-300"
				src="data:image/webp;base64,{featured.image}"
				alt={featured.prompt}
			/>
			<div
				class="absolute left-0 top-0 flex w-full justify-center rounded-t-lg bg-slate-800/60 py-2 shadow-xl md:bottom-0 md:top-auto md:rounded-b-lg md:rounded-t-none md:py-4"
			>
				<span class="text-center text-lg font-semibold text-slate-100 md:text-xl">{word}</span>
			</div>
		</a>
	</div>
</div>
