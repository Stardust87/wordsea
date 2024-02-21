<script lang="ts">
	import type { Mnemonic } from '$lib/types/Mnemonic';
	export let featured: Mnemonic;
	export let randomWord: string = '';
</script>

<div class="relative mb-4 flex w-full flex-col gap-2 rounded-lg md:w-1/2">
	<a href="/words/{randomWord}" class="rounded-lg">
		<img
			class="h-auto max-w-full rounded-lg shadow-xl duration-300"
			src="data:image/webp;base64,{featured.image}"
			alt={featured.prompt}
		/>
		<div
			class="absolute bottom-0 left-0 flex w-full justify-center rounded-b-lg bg-slate-800/60 py-2 shadow-xl md:py-5"
		>
			<span class="text-center text-lg font-semibold text-slate-100 md:text-xl">{randomWord}</span>
		</div>
	</a>
</div>
