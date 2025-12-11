#!/usr/bin/env python3
"""
Image Optimization Script for hudi-resources repository
This script compresses PNG images to reduce repository size and improve load times.
"""

import os
import sys
from PIL import Image
from pathlib import Path

def optimize_png(image_path, quality=85):
    """
    Optimize a PNG image by reducing quality while maintaining visual appearance.
    
    Args:
        image_path: Path to the PNG file
        quality: Compression quality (0-100)
    
    Returns:
        Tuple of (original_size, new_size, savings_percent)
    """
    try:
        original_size = os.path.getsize(image_path)
        
        # Open and optimize the image
        with Image.open(image_path) as img:
            # Convert RGBA to RGB if necessary
            if img.mode == 'RGBA':
                # Create a white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[3])  # Use alpha channel as mask
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save with optimization
            img.save(image_path, 'PNG', optimize=True, quality=quality)
        
        new_size = os.path.getsize(image_path)
        savings = ((original_size - new_size) / original_size) * 100
        
        return original_size, new_size, savings
    except Exception as e:
        print(f"Error optimizing {image_path}: {e}", file=sys.stderr)
        return None, None, None

def main():
    """Main function to optimize all PNG images in the repository."""
    repo_root = Path(__file__).parent.parent
    
    # Find all PNG files
    png_files = list(repo_root.glob('*.png'))
    
    if not png_files:
        print("No PNG files found to optimize.")
        return
    
    print(f"Found {len(png_files)} PNG files to optimize...")
    print("-" * 80)
    
    total_original = 0
    total_new = 0
    
    for png_file in png_files:
        print(f"Optimizing: {png_file.name}...", end=' ')
        original, new, savings = optimize_png(png_file)
        
        if original is not None:
            total_original += original
            total_new += new
            print(f"✓ {original/1024/1024:.2f}MB → {new/1024/1024:.2f}MB ({savings:.1f}% saved)")
        else:
            print("✗ Failed")
    
    print("-" * 80)
    total_savings = ((total_original - total_new) / total_original) * 100 if total_original > 0 else 0
    print(f"Total: {total_original/1024/1024:.2f}MB → {total_new/1024/1024:.2f}MB")
    print(f"Total savings: {(total_original - total_new)/1024/1024:.2f}MB ({total_savings:.1f}%)")

if __name__ == '__main__':
    main()
