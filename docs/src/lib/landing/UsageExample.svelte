<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';
	let visible = $state(false);

	onMount(() => {
		const section = document.querySelector('#quick-start');
		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.isIntersecting) {
						visible = true;
					}
				});
			},
			{ threshold: 0.2 }
		);

		if (section) observer.observe(section);
		return () => observer.disconnect();
	});
</script>

<div id="quick-start" class="hero min-h-screen py-24">
	<div class="hero-content text-center text-neutral-content">
		{#if visible}
			<div class="max-w-3xl space-y-12" in:fly={{ y: 50, duration: 1000, delay: 200 }}>
				<h1 class="text-5xl font-bold leading-tight">Quick Start</h1>
				<p class="text-xl leading-relaxed">
					Get started in just a few steps! Clone the repository, add your planetary video, and
					process it effortlessly.
				</p>
				<div class="mockup-code w-full text-left">
					<pre data-prefix="$"><code class="text-success"
							>git clone https://github.com/oadultradeepfield/galilean</code
						></pre>
					<pre data-prefix="$"><code class="text-cyan-500">cd galilean/galilean/</code></pre>
				</div>
				<p class="text-xl leading-relaxed">
					Add your planetary video to a <code>source</code> folder, then run:
				</p>
				<div class="mockup-code w-full text-left">
					<pre data-prefix="$"><code class="text-success">python3 main.py</code></pre>
				</div>
				<p class="text-xl leading-relaxed">Enjoy your results!</p>
				<div class="diff aspect-[16/9] shadow-xl">
					<div class="diff-item-1">
						<img alt="after" src="jupiter_after.jpg" />
					</div>
					<div class="diff-item-2">
						<img alt="before" src="jupiter_before.jpg" />
					</div>
					<div class="diff-resizer"></div>
				</div>
			</div>
		{/if}
	</div>
</div>
