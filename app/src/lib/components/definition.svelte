<script lang="ts">
	import type { Meaning } from '$lib/types/Meaning';
	export let meanings: Meaning[] = [];
</script>

<ol class="list-roman list-inside">
	{#each meanings as meaning}
		<li>
			<span class="text-xl italic">{meaning.pos}</span>
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
