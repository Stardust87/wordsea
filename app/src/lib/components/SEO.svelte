<script lang="ts">
	import { page } from '$app/stores';

	export let data: {
		title: string;
		description: string;
		image: string;
	};

	const image = `data:image/webp;base64,${data.image}`;
</script>

<svelte:head>
	<title>{data.title}</title>
	<meta name="description" content={data.description} />
	<meta property="og:title" content={data.title} />
	<meta property="og:description" content={data.description} />
	<meta property="og:image" content={image} />
	<meta property="og:type" content="website" />
	<!-- <meta property="og:url" content={data.url} /> -->
	<meta name="twitter:card" content="summary_large_image" />
	<meta name="twitter:title" content={data.title} />
	<meta name="twitter:description" content={data.description} />
	<meta name="twitter:image" content={image} />
	<link rel="canonical" href={$page.url.pathname} />
</svelte:head>
