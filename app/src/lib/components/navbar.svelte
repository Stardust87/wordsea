<script lang="ts">
	import ThemeSwitch from './themeSwitch.svelte';
	import Search from './search.svelte';
</script>

<nav
	class="max-w-screen border-gray mb-8 border-b bg-white py-2 dark:border-slate-700 dark:bg-slate-800"
>
	<div class="container m-auto flex flex-wrap items-center justify-between px-2 lg:px-8">
		<a href="/" class="flex items-center space-x-2 rtl:space-x-reverse">
			<img src="/logo.png" class="h-8" alt="WordSea Logo" />
			<span class="self-center whitespace-nowrap text-xl font-semibold">WordSea</span>
		</a>
		<Search />
		<ThemeSwitch />
	</div>
</nav>
