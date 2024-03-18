<script lang="ts">
	import ThemeSwitch from './themeSwitch.svelte';
	import Search from './search.svelte';
	import RandomWordButton from './randomWordButton.svelte';
</script>

<nav
	class="max-w-screen border-gray border-b bg-white py-2 dark:border-slate-700 dark:bg-slate-800"
>
	<div class="container m-auto flex flex-wrap items-center justify-between gap-y-2 px-2 lg:px-8">
		<a href="/" class="flex items-center space-x-2 rtl:space-x-reverse">
			<img src="/logo.png" class="h-8 w-8" alt="WordSea Logo" />
			<span class="self-center whitespace-nowrap text-xl font-semibold">WordSea</span>
		</a>
		<ThemeSwitch />
		<div
			class="flex w-full grow items-center gap-x-2 min-[480px]:mx-3 min-[480px]:w-auto sm:w-96 sm:grow-0"
		>
			<Search />
			<RandomWordButton />
		</div>
	</div>
</nav>
