<script lang="ts">
	export let audioUrl: string = '';
	export let ipa: string = '';

	const playRecording = () => {
		const audio = new Audio(audioUrl);
		audio.play();
	};
</script>

<button
	on:click={playRecording}
	class="group flex items-center pb-2 pt-1 text-slate-600 hover:text-slate-800 dark:text-slate-400 hover:dark:text-slate-300"
>
	<p class="text-xl font-light group-hover:font-normal">{ipa}</p>
	<svg
		xmlns="http://www.w3.org/2000/svg"
		class="ml-2 h-4 w-4"
		viewBox="0 0 384 512"
		fill="currentColor"
		><path
			d="M73 39c-14.8-9.1-33.4-9.4-48.5-.9S0 62.6 0 80V432c0 17.4 9.4 33.4 24.5 41.9s33.7 8.1 48.5-.9L361 297c14.3-8.7 23-24.2 23-41s-8.7-32.2-23-41L73 39z"
		/></svg
	>
</button>
