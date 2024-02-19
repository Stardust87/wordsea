<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let mnemonics: Mnemonic[] = [];
	export let randomWord: string = '';

	$: featured = mnemonics[0];
</script>

<div class="relative left-1/2 mb-4 flex -translate-x-1/2 justify-center md:w-1/2">
	<img
		class="h-auto max-w-full rounded-lg shadow-lg duration-300"
		src="data:image/webp;base64,{featured.images[0]}"
		alt={featured.prompt}
	/>
	<div class="absolute bottom-0 left-0 flex w-full justify-center bg-slate-800/60 py-5">
		<a href="/words/{randomWord}" class="text-center text-xl font-semibold text-slate-300"
			>{randomWord}</a
		>
	</div>
</div>
