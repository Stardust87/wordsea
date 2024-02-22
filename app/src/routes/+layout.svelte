<script>
	import Navbar from '$lib/components/navbar.svelte';
	import '../app.css';
</script>

<Navbar />
<main class="container mx-auto my-2 p-2 lg:my-4 lg:p-4">
	<slot />
</main>
