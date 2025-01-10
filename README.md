# Galilean

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![SvelteKit](https://img.shields.io/badge/sveltekit-%23ff3e00.svg?style=for-the-badge&logo=svelte&logoColor=white)
![TailwindCSS](https://img.shields.io/badge/tailwindcss-%2338B2AC.svg?style=for-the-badge&logo=tailwind-css&logoColor=white)
![DaisyUI](https://img.shields.io/badge/daisyui-5A0EF8?style=for-the-badge&logo=daisyui&logoColor=white)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Vercel](https://img.shields.io/badge/vercel-%23000000.svg?style=for-the-badge&logo=vercel&logoColor=white)

## Project Overview

Galilean is a Python CLI tool inspired by popular planetary image processing software like PIPP, AutoStakkert!, and RegiStax. The original author, Phanuphat Srisukhawasu, is an astrophotography enthusiast. Unfortunately, as he now uses macOS instead of Windows, he cannot run these unsupported software tools natively. As a side project, he developed this CLI app to replicate their functionality. While the project is still under development and not perfect, it aims to provide similar capabilities.

**Note**: For the installation guide, user manual, and examples, please visit [this page](https://galilean.vercel.app/). This README is intended for local development and contributions only.

## Getting Started

The project is structured into two main folders: `docs` and `galilean`. The `docs` folder contains the Svelte project used to create the documentation website for non-technical users. The `galilean` folder contains the Python and OpenCV source code. If you're contributing to image processing, focus on the `galilean` folder.

### Installation

Start by cloning the GitHub repository:

```bash
git clone https://github.com/oadultradeepfield/galilean
cd galilean
```

### Working on Python Source Code

The Python source code is organized into four processing steps: `detect_and_crop`, `evaluate_and_align`, `image_stacking`, and `postprocessing`. Navigate to the part you're interested in modifying. Any changes should be tested using the `test.py` file. To run the tests, use:

```bash
python3 galilean/test.py
```

The test uses sample images located in the `test/input` directory. The results will be generated as separate folders for each processing step in the `test/out` directory (which is included in `.gitignore`). As a rule of thumb, running the tests should produce no errors, and the results should not degrade the original image quality.

If you want to test on real-world data, create a `source` folder inside the `galilean` directory and add your videos there. Run the following command to start processing:

```bash
python3 galilean/main.py
```

Follow the prompts in the CLI. More detailed information can be found on [this page](https://galilean.vercel.app/user-manual).

### Working on Documentation

The documentation is designed as a website to make it more accessible to non-technical users. It is built using Svelte and SvelteKit, built with Vite. The styling is done using Tailwind CSS with daisyUI, and the package manager used is `pnpm`. Ensure you have it installed before starting. After setup, you can use the following commands for local development:

```bash
cd docs
pnpm install
pnpm run dev
```

The server will start on port 5173 by default. Open http://localhost:5173 in your browser to view the generated website.

## Contribution Guidelines

Contributions are highly welcome! Please fork this repository and create pull requests. Ensure that your pull request includes a clear and descriptive explanation of the changes made and why your approach is an improvement. Contributions to alignment algorithms and postprocessing steps are especially appreciated.

## License

This project is licensed under the GNU General Public License v3.0
. See the [LICENSE](/LICENSE) file for details.
