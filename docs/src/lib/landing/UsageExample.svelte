<script lang="ts">
	import { fly } from 'svelte/transition';
	import { onMount } from 'svelte';

	let visible = false;

	onMount(() => {
		const section = document.querySelector('#quick-start');
		const observer = new IntersectionObserver(
			([entry]) => {
				if (entry.isIntersecting) {
					visible = true;
				}
			},
			{ threshold: 0.2 }
		);

		if (section) observer.observe(section);
		return () => observer.disconnect();
	});
</script>

<div id="quick-start" class="flex min-h-screen flex-col justify-center px-8 py-24">
	<div class="text-center">
		{#if visible}
			<div class="prose mx-auto max-w-2xl space-y-8" in:fly={{ y: 50, duration: 1000, delay: 200 }}>
				<h1 class="text-5xl font-bold">Quick Start</h1>
				<p class="text-xl">
					Get started in just a few steps! Clone the repository, add your planetary video, and
					process it effortlessly.
				</p>
				<div class="mockup-code text-left">
					<pre class="text-success" data-prefix="$"><code
							>git clone https://github.com/oadultradeepfield/galilean</code
						></pre>
					<pre class="text-cyan-500" data-prefix="$"><code>cd galilean/galilean/</code></pre>
				</div>
				<p class="text-xl">
					Add your planetary video to a <code>source</code> folder, then run:
				</p>
				<div class="mockup-code text-left">
					<pre class="text-success" data-prefix="$"><code>python3 main.py</code></pre>
				</div>
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
