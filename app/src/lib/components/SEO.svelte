<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';

	export let data: {
		title: string;
		description: string;
		image: string;
	};

	let origin = '';
	onMount(() => {
		origin = window.location.origin;
	});
</script>

<svelte:head>
	<title>{data.title}</title>
	<meta name="description" content={data.description} />
	<meta property="og:title" content={data.title} />
	<meta property="og:description" content={data.description} />
	<meta property="og:image" content={data.image} />
	<meta property="og:type" content="website" />
	<meta property="og:url" content={origin + $page.url.pathname} />
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={data.title} />
	<meta name="twitter:description" content={data.description} />
	<meta name="twitter:image" content={data.image} />
	<link rel="canonical" href={origin + $page.url.pathname} />
</svelte:head>
