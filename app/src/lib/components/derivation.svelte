<script lang="ts">
	export let derivedFrom: string = '';
	export let derivatives: string[] = [];
</script>

{#if derivedFrom || derivatives.length > 0}
	<div class="flex flex-wrap items-center gap-y-2">
		{#if derivedFrom}
			<span
				class="mr-2 block rounded bg-slate-50 px-2 py-1 font-medium shadow-md dark:bg-slate-700/50"
				>Derived from
			</span>
			<a
				class="mr-2 rounded bg-cyan-600 px-2 py-1 font-medium text-white shadow-md hover:bg-cyan-800"
				href={`/words/${derivedFrom}`}
				>{derivedFrom}
			</a>
		{/if}
		{#if derivatives.length > 0}
			<span
				class="mr-2 block rounded bg-slate-50 px-2 py-1 font-medium shadow-md dark:bg-slate-700/50"
				>Derivatives
			</span>
			{#each derivatives as derivative}
				<a
					class="mr-2 block rounded bg-cyan-600 px-2 py-1 font-medium text-white shadow-md hover:bg-cyan-800"
					href={`/words/${derivative}`}
					>{derivative}
				</a>
			{/each}
		{/if}
	</div>
{/if}
