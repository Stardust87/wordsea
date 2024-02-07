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

<ol class="list-roman list-inside py-4">
	{#each meanings as meaning}
		<li>
			<span class="text-xl italic">{meaning.pos} </span>
			{#if filterForms(meaning.forms, meaning.pos).length > 0}
				<span class="text-lg italic text-slate-800 dark:text-slate-400">
					&mdash; {filterForms(meaning.forms, meaning.pos)}
				</span>
			{/if}

			<ol class="ml-4 list-inside list-decimal">
				{#each meaning.senses as sense}
					<li>
						{sense.gloss}
						{#if sense.examples}
							<ul class="ml-8 list-inside list-disc">
								{#each sense.examples as example}
									<li>{example.text}</li>
								{/each}
							</ul>
						{/if}
					</li>
				{/each}
			</ol>
		</li>
	{/each}
</ol>
