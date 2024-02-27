<script>
	import { page } from '$app/stores';
	import Navbar from '$lib/components/navbar.svelte';
	import SEO from '$lib/components/SEO.svelte';
	import '../app.css';
</script>

<SEO
	data={{ title: $page.data.title, description: $page.data.description, image: $page.data.image }}
/>

<Navbar />
<main class="container mx-auto my-2 p-2 lg:my-4 lg:p-4">
	<slot />
</main>
