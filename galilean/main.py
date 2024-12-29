import os
from datetime import datetime
from typing import List, Tuple

import cv2
import numpy as np
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.table import Table

from detect_and_crop.handler import detect_and_crop
from evaluate_and_align.handler import evaluate_and_align
from image_stacking.handler import image_stacking
from postprocessing.handler import postprocessing

app = typer.Typer(help="Galilean - Planetary Image Processing CLI Tool")
console = Console()

def get_video_resolution(video_path: str) -> Tuple[int, int]:
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap.release()
    return width, height

def list_video_files(directory: str = "source") -> List[str]:
    if not os.path.exists(directory):
        console.print(f"[red]Error:[/red] Directory '{directory}' not found!")
        raise typer.Exit(1)
    
    video_files = []
    for file in os.listdir(directory):
        if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_files.append(os.path.join(directory, file))
    return video_files

def select_videos(video_files: List[str]) -> List[str]:
    if not video_files:
        console.print("[red]No video files found in the 'source' directory![/red]")
        raise typer.Exit(1)

    table = Table(title="Available Videos")
    table.add_column("Index", style="cyan")
    table.add_column("Filename", style="green")
    table.add_column("Resolution", style="yellow")

    for idx, file in enumerate(video_files, 1):
        width, height = get_video_resolution(file)
        table.add_row(str(idx), os.path.basename(file), f"{width}x{height}")

    console.print(table)
    
    while True:
        indices = Prompt.ask(
            "Enter video numbers to process (comma-separated)",
            default="1"
        )
        try:
            selected_indices = [int(idx.strip()) for idx in indices.split(",")]
            if all(1 <= idx <= len(video_files) for idx in selected_indices):
                return [video_files[idx-1] for idx in selected_indices]
        except ValueError:
            console.print("[red]Please enter valid numbers![/red]")

def get_crop_size(max_dimension: int) -> int:
    available_sizes = [360, 480, 720, 1080]
    valid_sizes = [size for size in available_sizes if size <= max_dimension]
    
    if not valid_sizes:
        console.print("[red]Error: Video resolution too small for available crop sizes[/red]")
        raise typer.Exit(1)

    options = {str(i): str(size) for i, size in enumerate(valid_sizes, 1)}
    
    console.print(Panel("Available crop sizes:", style="cyan"))
    for key, value in options.items():
        console.print(f"{key}. {value}p")
    
    while True:
        choice = Prompt.ask("Select crop size", choices=list(options.keys()))
        return int(options[choice])

def get_quality_threshold() -> float:
    qualities = {
        "1": 0.80,
        "2": 0.85,
        "3": 0.90,
        "4": 0.95,
        "5": 0.99,
        "6": 1.00
    }
    
    console.print(Panel("Image quality threshold:", style="cyan"))
    for key, value in qualities.items():
        console.print(f"{key}. {int(value * 100)}%")
    
    choice = Prompt.ask("Select quality threshold", choices=list(qualities.keys()))
    return qualities[choice]

def get_stacking_method() -> str:
    methods = {
        "1": "mean",
        "2": "median",
        "3": "mean_with_clipping",
        "4": "mean_with_median_clipping"
    }
    
    console.print(Panel("Stacking methods:", style="cyan"))
    for key, value in methods.items():
        console.print(f"{key}. {value.replace('_', ' ').title()}")
    
    choice = Prompt.ask("Select stacking method", choices=list(methods.keys()))
    return methods[choice]

def get_sharpening_factor() -> float:
    factors = {
        "1": 1.0,
        "2": 1.2,
        "3": 1.5,
    }
    
    console.print(Panel("Sharpening levels:", style="cyan"))
    console.print("1. Low")
    console.print("2. Moderate (Recommended)")
    console.print("3. High")
    
    choice = Prompt.ask("Select sharpening level", choices=list(factors.keys()))
    return factors[choice]

def get_scaling_factor() -> int:
    console.print(Panel("[yellow]⚠️ Warning: Super resolution is done using AI and may take longer to process[/yellow]", 
                        style="yellow"))
    choice = Prompt.ask("Select scaling factor", choices=["None", "2", "3"], default="None")
    return 1 if choice == "None" else int(choice)

@app.command()
def main():
    """
    Galilean - Video Stacking and Processing Tool
    """
    console.print(
        """
        [cyan]
   ____       _ _ _                  
  / ___| __ _| (_) | ___  __ _ _ __  
 | |  _ / _` | | | |/ _ \/ _` | '_ \ 
 | |_| | (_| | | | |  __/ (_| | | | |
  \____|\__,_|_|_|_|\___|\__,_|_| |_|
                                     
        [/cyan]
        """
    )
    
    video_files = list_video_files()
    selected_files = select_videos(video_files)
    
    min_height = min(get_video_resolution(f)[1] for f in selected_files)
    crop_size = get_crop_size(min_height)
    
    threshold = get_quality_threshold()
    stacking_method = get_stacking_method()
    sharpening_factor = get_sharpening_factor()
    scaling_factor = get_scaling_factor()
    
    images = []
    framerate = None
    output_dir = "out"
    os.makedirs(output_dir, exist_ok=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Loading videos...", total=len(selected_files))
        for file in selected_files:
            cap = cv2.VideoCapture(file)
            if not framerate:
                framerate = int(cap.get(cv2.CAP_PROP_FPS))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                images.append(frame)
            cap.release()
            progress.advance(task)
        
        # task = progress.add_task("Processing images...", total=len(images))
        # cropped_images = np.array([detect_and_crop(image, crop_size) for image in images])
        # progress.advance(task)
        
        task = progress.add_task("Aligning images...")
        aligned_images, best_index, best_score, avg_quality = evaluate_and_align(np.array(images), threshold)
        progress.advance(task)
        
        task = progress.add_task("Stacking and cropping images...")
        stacked_image = detect_and_crop(image_stacking(aligned_images, stacking_method), crop_size)
        progress.advance(task)
        
        task = progress.add_task("Post-processing...")
        postprocessed_image = postprocessing(stacked_image, sharpening_factor, scaling_factor)
        progress.advance(task)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stacked_image_output = os.path.join(output_dir, f"{timestamp}_stacked_image.tiff")
    postprocessed_image_output = os.path.join(output_dir, f"{timestamp}_postprocessed_image.tiff")
    
    with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
        task = progress.add_task("Saving outputs...")        
        cv2.imwrite(stacked_image_output, stacked_image.astype('uint8'))
        cv2.imwrite(postprocessed_image_output, postprocessed_image.astype('uint8'))
    
    console.print("\n[green]✓ Processing complete![/green]")
    results = Table(title="Processing Results")
    results.add_column("Metric", style="cyan")
    results.add_column("Value", style="green")
    
    results.add_row("Best Frame Index", str(best_index))
    results.add_row("Best Frame Score", f"{best_score:.3f}")
    results.add_row("Average Quality", f"{avg_quality:.3f}")
    results.add_row("Output Directory", output_dir)
    
    console.print(results)

if __name__ == "__main__":
    app()
