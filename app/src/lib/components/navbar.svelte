<script lang="ts">
	import ThemeSwitch from './themeSwitch.svelte';
</script>

<nav
	class="max-w-screen border-b-2 border-slate-200 bg-slate-100/50 shadow-sm dark:border-slate-700 dark:bg-slate-800"
>
	<div class="container mx-auto flex flex-wrap items-center justify-between px-2 py-1 lg:px-8">
		<a href="/" class="flex items-center space-x-3 rtl:space-x-reverse">
			<span class="self-center whitespace-nowrap text-3xl font-semibold text-violet-400"
				>WordSea</span
			>
		</a>
		<button
			data-collapse-toggle="navbar-default"
			type="button"
			class="inline-flex h-10 w-10 items-center justify-center rounded-lg p-2 text-sm text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 md:hidden dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
			aria-controls="navbar-default"
			aria-expanded="false"
		>
			<span class="sr-only">Open main menu</span>
			<svg
				class="h-5 w-5"
				aria-hidden="true"
				xmlns="http://www.w3.org/2000/svg"
				fill="none"
				viewBox="0 0 17 14"
			>
				<path
					stroke="currentColor"
					stroke-linecap="round"
					stroke-linejoin="round"
					stroke-width="2"
					d="M1 1h15M1 7h15M1 13h15"
				/>
			</svg>
		</button>

		<div class="hidden w-full md:block md:w-auto" id="navbar-default">
			<ul
				class="d:p-0 mt-4 flex flex-col rounded-lg border p-4 font-medium md:mt-0 md:flex-row md:space-x-8 md:border-0 rtl:space-x-reverse"
			>
				<li>
					<a
						href="/"
						class=" block px-3 py-2 text-violet-600 md:p-0 dark:text-violet-400"
						aria-current="page">Home</a
					>
				</li>
				<li>
					<a
						href="/"
						class="block px-3 py-2 text-gray-900 md:border-0 md:p-0 md:hover:text-violet-600 dark:text-white dark:hover:text-white md:dark:hover:text-violet-400"
						>About</a
					>
				</li>
				<li>
					<a
						href="/"
						class="block px-3 py-2 text-gray-900 md:border-0 md:p-0 md:hover:text-violet-600 dark:text-white dark:hover:text-white md:dark:hover:text-violet-400"
						>Dashboard</a
					>
				</li>
				<li>
					<a
						href="/"
						class="block px-3 py-2 text-gray-900 md:border-0 md:p-0 md:hover:text-violet-600 dark:text-white dark:hover:text-white md:dark:hover:text-violet-400"
						>Pricing</a
					>
				</li>
			</ul>
		</div>
		<ThemeSwitch />
	</div>
</nav>
