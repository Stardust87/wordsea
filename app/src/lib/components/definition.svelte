<script lang="ts">
	import type { Meaning } from '$lib/types/Meaning';
	export let meanings: Meaning[] = [];

	const filterForms = (forms: object, pos: string) => {
		return Object.entries(forms)
			.filter(([key, value]) => {
				if (pos === 'verb') {
					return ['third_person', 'present_participle', 'past_participle'].includes(key);
				} else if (pos === 'noun') {
					return ['plural'].includes(key);
				} else if (pos === 'adj') {
					return ['comparative', 'superlative'].includes(key);
				} else {
					return false;
				}
			})
			.map(([key, value]) => value)
			.join('; ');
	};
</script>

<!-- shadow-[0px_5px_20px_5px_#00000024] -->
<ol class="list-roman min-w-prose list-inside">
	{#each meanings as meaning}
		<div
			class="mb-4 rounded-md bg-white p-2 shadow-[0_3px_5px_rgb(0,0,0,0.2)] dark:bg-slate-700/50 dark:shadow-sm"
		>
			<li class="text-xl">
				<span class="italic">{meaning.pos} </span>
				{#if filterForms(meaning.forms, meaning.pos).length > 0}
					<span class="text-lg italic text-slate-600 dark:text-slate-400">
						&mdash; {filterForms(meaning.forms, meaning.pos)}
					</span>
				{/if}

				<ol class="ml-4 list-inside list-decimal">
					{#each meaning.senses as sense}
						<li class="mb-2 text-lg">
							{sense.gloss}
							{#if sense.examples}
								<ul class="ml-4 list-inside list-disc text-base text-slate-600 dark:text-slate-400">
									{#each sense.examples as example}
										<li>{example.text}</li>
									{/each}
								</ul>
							{/if}
						</li>
					{/each}
				</ol>
			</li>
		</div>
	{/each}
</ol>
