<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	let show = $state(false);

	onMount(() => {
		show = true;
	});
</script>

<div class="hero relative min-h-screen" style="background-image: url(banner.jpg);">
	<div class="hero-overlay bg-opacity-60"></div>
	<div class="hero-content text-center text-neutral-content">
		{#if show}
			<div class="max-w-xl space-y-12 py-16" in:fly={{ y: 50, duration: 1000 }}>
				<h1 class="text-6xl font-bold leading-tight">One CLI for Planetary Image Processing</h1>
				<p class="text-xl leading-relaxed">
					Streamline your workflow with a unified command line interface that integrates PIPP,
					AutoStakkert!, and RegiStax—compatible with all devices.
				</p>
				<div class="flex flex-col items-center gap-6">
					<a
						href="#quick-start"
						class="btn btn-secondary btn-lg w-56 transition-transform hover:scale-105"
						onclick={(e) => {
							e.preventDefault();
							document.querySelector('#quick-start')?.scrollIntoView({
								behavior: 'smooth'
							});
						}}
					>
						Get Started
					</a>
					<p class="text-sm opacity-90">Align, stack, sharpen, and more—effortlessly</p>
				</div>
			</div>
		{/if}
	</div>
</div>
