<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let mnemonics: Mnemonic[] = [];
	export let randomWord: string = '';

	$: featured = mnemonics[Math.floor(Math.random() * mnemonics.length)];
</script>

<div class="relative left-1/2 mb-4 flex -translate-x-1/2 justify-center rounded-lg md:w-1/2">
	<a href="/words/{randomWord}" class="rounded-lg">
		<img
			class="h-auto max-w-full rounded-lg shadow-xl duration-300"
			src="data:image/webp;base64,{featured.images[0]}"
			alt={featured.prompt}
		/>
		<div
			class="absolute bottom-0 left-0 flex w-full justify-center rounded-lg bg-slate-800/60 py-2 md:py-5"
		>
			<span class="text-center text-lg font-semibold text-slate-300 md:text-xl">{randomWord}</span>
		</div>
	</a>
</div>
