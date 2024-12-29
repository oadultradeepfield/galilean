<div class="hidden max-w-5xl px-6 md:breadcrumbs md:my-4 md:flex md:justify-center md:text-sm">
	<ul>
		<li><a href="#Prerequisites">Prerequisites</a></li>
		<li><a href="#Creating-the-Source-Directory">Creating the Source Directory</a></li>
		<li><a href="#Starting-the-CLI">Starting the CLI</a></li>
		<li><a href="#Contributing">Contributing</a></li>
	</ul>
</div>
<div class="prose mx-auto mb-12 mt-4 max-w-3xl space-y-6 px-6">
	<h1 class="mb-6 text-center text-3xl font-bold">User Manual</h1>

	<h2 id="Prerequisites" class="text-2xl font-bold">Prerequisites</h2>
	<p>
		Before using this manual, please ensure that you have installed and set up the directory as
		described on the
		<a class="link link-primary" href="/installation">Installation</a> page.
	</p>

	<h2 id="Creating-the-Source-Directory" class="text-2xl font-bold">
		Creating the Source Directory
	</h2>
	<p>
		In the same folder as <code>main.py</code>, create a folder named <code>source</code> and place
		all the videos you want to process in it. Supported video formats are <code>.mp4</code>,
		<code>.mov</code>, <code>.avi</code>, and <code>.mkv</code>. Make sure your videos are in one of
		these formats before proceeding to the next section.
	</p>

	<h2 id="Starting-the-CLI" class="text-2xl font-bold">Starting the CLI</h2>
	<p>To start the program, run the following command in your terminal or command prompt:</p>
	<div class="mockup-code">
		<pre data-prefix="$"><code>python3 main.py</code></pre>
	</div>
	<p>
		This will launch the CLI tool and prompt you to choose a video for processing. The interface
		should look something like this:
	</p>
	<div class="mockup-code">
		<pre><code class="text-cyan-400">
			____       _ _ _                  
		   / ___| __ _| (_) | ___  __ _ _ __  
		  | |  _ / _` | | | |/ _ \/ _` | '_ \ 
		  | |_| | (_| | | | |  __/ (_| | | | |
		   \____|\__,_|_|_|_|\___|\__,_|_| |_|
										
				Available Videos              
	┏━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┓
	┃ Index ┃ Filename            ┃ Resolution ┃
	┡━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━┩
	│ 1     │ example_jupiter.MOV │ 640x360    │
	│ 2     │ example_saturn.MOV  │ 640x360    │
	│ 3     │ example_moon.MOV    │ 640x480    │
	└───────┴─────────────────────┴────────────┘
	Enter video numbers to process (comma-separated) (1):</code
			></pre>
	</div>
	<p>
		In this example, there are three files in the <code>source</code> folder, each with its
		resolution shown in the metadata. To proceed, type the number (index) of the video you want to
		use, as shown above. You can also select multiple videos by typing their numbers separated by
		commas, like <code>1,2,3</code>, if they contain the same objects recorded in different videos.
		In this tutorial, we'll use "Jupiter" as an example.
	</p>
	<p class="italic text-base-content/50">
		Note: Galilean CLI does not process each video separately. This means you cannot select videos
		of different objects in the same run and expect all results. Instead, you will receive a single
		stacked image of all the objects!
	</p>

	<h3 class="text-xl font-bold">Selecting Crop Size</h3>
	<p>
		Next, you will be asked to select the cropping resolution. Since our original video has a low
		resolution, the output can only be cropped to smaller sizes. For larger original files, there
		are more options, such as <code>360</code>, <code>480</code>, <code>720</code>, and
		<code>1080</code>.
	</p>
	<div class="mockup-code">
		<pre><code class="text-success">	Enter video numbers to process (comma-separated) (1): 1</code
			><code class="text-cyan-400">
	╭───────────────────────╮
	│ Available crop sizes: │
	╰───────────────────────╯
	1. 360p
	Select crop size [1]:</code
			></pre>
	</div>
	<p>
		This cropping process is similar to software like PIPP. However, our implementation will align
		the images using phase correlation and then perform other steps. The cropping happens in the
		final step, after stacking, to create centralized images.
	</p>

	<h3 class="text-xl font-bold">Choosing Number of Images</h3>
	<p>
		Galilean will evaluate each video frame to assess its quality based on contrast, sharpness, and
		signal-to-noise ratio. This helps select the template image to which the algorithm will align
		the others. It's common to have a few good images and many blurry ones, so we provide options to
		choose which images to keep. Below, you can select the percentage of images you want to retain.
	</p>
	<div class="mockup-code">
		<pre><code class="text-cyan-400"
				><code class="text-success">	Select crop size [1]: 1</code>
	╭──────────────────────────╮
	│ Image quality threshold: │
	╰──────────────────────────╯
	1. 80%
	2. 85%
	3. 90%
	4. 95%
	5. 99%
	6. 100%
	Select quality threshold [1/2/3/4/5/6]:</code
			></pre>
	</div>
	<p>
		Since the original footage has already filtered out frames with unstable camera movement, we
		will use 95% as an example.
	</p>

	<h3 class="text-xl font-bold">Choosing Stacking Method</h3>
	<p>
		Stacking is a key technique used in software like AutoStakkert! and other astro image processing
		tools. It helps improve the signal-to-noise ratio, and in the case of lucky imaging, it reduces
		turbulence and enhances clarity.
	</p>
	<div class="mockup-code">
		<pre><code class="text-cyan-400"
				><code class="text-success">	Select quality threshold [1/2/3/4/5/6]: 4</code>
	╭───────────────────╮
	│ Stacking methods: │
	╰───────────────────╯
	1. Mean
	2. Median
	3. Mean With Clipping
	4. Mean With Median Clipping
	Select stacking method [1/2/3/4]:</code
			></pre>
	</div>
	<p>
		Mean stacking usually provides the best signal-to-noise ratio, while median stacking is useful
		when there are unwanted objects in the scene (like satellites, though that's not typically an
		issue here). Mean with clipping removes pixels that deviate too much from the mean, capping them
		at a set value. Median clipping, on the other hand, clips values to the median of the pixels.
		For simplicity, we'll use "Mean" for this demonstration.
	</p>

	<h3 class="text-xl font-bold">Adjust Sharpening Factor</h3>
	<p>
		At this stage, you're in the postprocessing phase, similar to what you would do in RegiStax.
		Galilean will prompt you to choose a sharpening factor to enhance the images further. It's worth
		experimenting with different options to see how they affect your final output, but "Moderate" is
		a good starting point.
	</p>
	<div class="mockup-code">
		<pre><code class="text-cyan-400"
				><code class="text-success">	Select stacking method [1/2/3/4]: 1</code>
	╭────────────────────╮
	│ Sharpening levels: │
	╰────────────────────╯
	1. Low
	2. Moderate (Recommended)
	3. High
	Select sharpening level [1/2/3]:</code
			></pre>
	</div>
	<p>
		The sharpening effect, done with Laplacian Transforms, is gentle, so it should preserve most of
		the raw data. We will use the "Moderate" option in this demonstration.
	</p>
	<p class="italic text-base-content/50">
		Note: Our postprocessing steps are not perfect, so we recommend using other image processing
		software, like Photoshop, to fine-tune the results. The program also applies auto white balance
		using the Gray World assumption, but tweaking it in your preferred software is still
		recommended.
	</p>

	<h3 class="text-xl font-bold">Super-resolution</h3>
	<p>
		Our software currently cannot replicate the Drizzle algorithm used in most astrophotography
		tools. Instead, we use an AI-based solution with a deep learning model called <a
			class="link link-primary"
			href="https://github.com/sanghyun-son/EDSR-PyTorch">ESDR</a
		>. While it may take longer to process, this allows you to upscale your original image by 2x or
		3x.
	</p>
	<div class="mockup-code">
		<pre><code class="text-cyan-400"
				><code class="text-success">	Select sharpening level [1/2/3]: 2</code><code
					class="text-error">
	╭───────────────────────────────────────────────────────────────────────────╮
	│ Warning: Super resolution is done using AI and may take longer to process │
	╰───────────────────────────────────────────────────────────────────────────╯</code
				>
	Select scaling factor [None/2/3] (None):</code
			></pre>
	</div>
	<p>
		If you prefer to skip this step, simply input "None." In this example, we'll use 3x scaling to
		demonstrate the effect. After submitting, you're all set! Please sit back and relax, as
		processing may take a few minutes depending on the size and duration of the video. If everything
		is done correctly, you should see an output like this:
	</p>
	<div class="mockup-code">
		<pre>
		<code class="text-success">
	Select scaling factor [None/2/3] (None): 3
	⠋ Saving outputs...

	✓ Processing complete!
			Processing Results     
	┏━━━━━━━━━━━━━━━━━━┳━━━━━━━┓
	┃ Metric           ┃ Value ┃
	┡━━━━━━━━━━━━━━━━━━╇━━━━━━━┩
	│ Best Frame Index │ 1737  │
	│ Best Frame Score │ 0.888 │
	│ Average Quality  │ 0.677 │
	│ Output Directory │ out   │
	└──────────────────┴───────┘
	</code></pre>
	</div>
	<p>
		While Galilean processes your output, you will see messages guiding you through each step. If
		you see "Postprocessing," it's a good sign that the output is almost ready. The final output
		will include an analysis of the best frame score and its index. The average quality is
		calculated across the video, and your output will be saved in a folder named <code>out</code>.
		Check this folder to ensure everything is correct. You should find two files: the stacked image
		and the postprocessed image.
	</p>
	<div class="diff aspect-[16/9]">
		<div class="diff-item-1">
			<img alt="after" src="jupiter_after.jpg" />
		</div>
		<div class="diff-item-2">
			<img alt="before" src="jupiter_before.jpg" />
		</div>
		<div class="diff-resizer"></div>
	</div>

	<h2 id="Contributing" class="text-2xl font-bold">Contributing</h2>
	<p>
		Whether you think Galilean is awesome or needs improvement, we'd love your feedback! This
		project was started by Phanuphat Srisukhawasu during winter break as a side project, inspired by
		the lack of support for PIPP, AutoStakkert!, and RegiStax on Mac. If you have suggestions for
		improvements or want to report bugs, feel free to open pull requests or issues on our <a
			class="link link-primary"
			href="https://github.com/oadultradeepfield/galilean">GitHub</a
		>. We are currently exploring better image alignment algorithms and enhanced postprocessing
		capabilities.
	</p>

	<p class="text-center font-semibold">Happy processing!</p>
</div>
