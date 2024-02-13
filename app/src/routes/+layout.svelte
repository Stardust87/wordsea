<script>
	import Navbar from '$lib/components/navbar.svelte';
	import '../app.css';
</script>

<Navbar />
<main class="container mx-auto mb-4 mt-2 px-2 pb-2 lg:px-8 lg:pb-8">
	<slot />
</main>
