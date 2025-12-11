.PHONY: help install optimize-images generate-toc validate-links all clean

help:
	@echo "Available commands:"
	@echo "  make install         - Install Python dependencies"
	@echo "  make optimize-images - Optimize all PNG images"
	@echo "  make generate-toc    - Generate table of contents for README"
	@echo "  make validate-links  - Check all links in README"
	@echo "  make all             - Run all optimization tasks"
	@echo "  make clean           - Remove temporary files"

install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

optimize-images: install
	@echo "Optimizing images..."
	python3 scripts/optimize_images.py

generate-toc: install
	@echo "Generating table of contents..."
	python3 scripts/generate_toc.py

validate-links: install
	@echo "Validating links..."
	python3 scripts/validate_links.py

all: optimize-images generate-toc
	@echo "All optimizations complete!"

clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
