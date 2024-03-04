<script>
	import { page } from '$app/stores';
</script>

<div class="mx-auto flex h-auto w-full flex-col gap-2 rounded-lg md:w-1/2">
	<div class="flex flex-col items-center">
		<h1 class=" text-lg font-semibold lowercase text-cyan-500 md:text-2xl lg:text-3xl">
			{$page.status}
			{$page.error?.message}
		</h1>
		<a href="/">Go to <span class="underline"> Home Page</span></a>
	</div>
	<img class=" max-w-full rounded-lg shadow-xl duration-300" src="/error.png" alt="Error page" />
</div>
