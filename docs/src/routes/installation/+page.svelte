<div class="hidden px-6 md:breadcrumbs md:my-4 md:flex md:justify-center md:text-sm">
	<ul>
		<li><a href="#Prerequisites">Prerequisites</a></li>
		<li><a href="#Cloning-the-GitHub-Repository">Cloning the GitHub Repository</a></li>
		<li><a href="#Installing-Python-Packages">Installing Python Packages</a></li>
		<li><a href="#Next-Steps">Next Steps</a></li>
	</ul>
</div>
<div class="prose mx-auto mb-12 mt-4 max-w-3xl space-y-6 py-6">
	<h1 class="mb-6 text-center text-3xl font-bold">Installation Guide</h1>

	<h2 id="Prerequisites" class="text-2xl font-bold">Prerequisites</h2>
	<ul>
		<li>
			<strong>Git:</strong>
			Before starting, ensure that Git is installed on your system. Git is required to clone the project
			from its GitHub repository. If you don’t have Git installed, please follow the step-by-step guide
			on
			<a class="link link-primary" href="https://git-scm.com/downloads">this page</a>.
		</li>
		<li>
			<strong>Python:</strong> You also need Python (version 3.X) installed to run the project. If
			Python is not installed on your system, visit
			<a class="link link-primary" href="https://www.python.org/">the official Python website</a>
			for installation instructions.
		</li>
	</ul>

	<h2 id="Cloning-the-GitHub-Repository" class="text-2xl font-bold">
		Cloning the GitHub Repository
	</h2>
	<p>
		The GitHub repository for this project is available at <a
			class="link link-primary"
			href="https://github.com/oadultradeepfield/galilean">this link</a
		>. Follow the steps below to clone the repository and navigate to the appropriate folder:
	</p>
	<ol>
		<li>Open your terminal or command prompt.</li>
		<li>Clone the repository to your desired directory.</li>
		<li>
			Navigate into the <code>galilean</code> folder, which contains the main Python codebase.
		</li>
	</ol>
	<p class="italic text-base-content/50">
		Note: The <code>docs</code> folder contains files for rendering this documentation. Unless you plan
		to contribute to the documentation, you can ignore it.
	</p>
	<div class="mockup-code">
		<pre data-prefix="$"><code>git clone https://github.com/oadultradeepfield/galilean</code></pre>
		<pre data-prefix="$"><code>cd galilean/galilean/</code></pre>
	</div>

	<h2 id="Installing-Python-Packages" class="text-2xl font-bold">Installing Python Packages</h2>
	<p>
		This project relies on several Python libraries listed in the <code>requirements.txt</code> file.
		To install all the required packages at once, run the following command in your terminal:
	</p>
	<div class="mockup-code">
		<pre data-prefix="$"><code>python3 -m pip install -r requirements.txt</code></pre>
	</div>
	<p>If the installation completes without any errors, you're ready to start using the program!</p>
	<h2 id="Next-Steps" class="text-2xl font-bold">Next Steps</h2>
	<p>
		Once the setup is complete, you can begin processing your planetary and solar system images
		captured through lucky imaging. To learn how to use the program, please visit the <a
			href="/user-manual"
			class="link link-primary">User Manual</a
		> page for step-by-step instructions.
	</p>
	<p class="text-center font-semibold">Happy processing!</p>
</div>
