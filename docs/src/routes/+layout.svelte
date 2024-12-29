<script lang="ts">
	import '../app.css';
	import Footer from '../components/common/Footer.svelte';
	import Navbar from '../components/common/Navbar.svelte';
	let { children } = $props();
</script>

<div class="flex h-screen flex-col">
	<header
		class="sticky top-0 z-[50] border-b border-base-content/25 bg-base-200/50 backdrop-blur-md"
	>
		<Navbar />
	</header>
	<main class="mb-auto px-4">
		{@render children()}
	</main>
	<footer class="bg-neutral">
		<Footer />
	</footer>
</div>
