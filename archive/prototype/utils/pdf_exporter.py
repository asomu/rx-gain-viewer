"""
PDF export utilities
Combines multiple images into a single PDF report
"""

from pathlib import Path
from typing import List, Optional
from PIL import Image
from datetime import datetime


class PDFExporter:
    """
    PDF export utility for combining multiple chart images
    """

    @staticmethod
    def images_to_pdf(
        image_paths: List[Path],
        output_pdf: Path,
        title: str = "RF S-parameter Analysis Report",
        page_size: tuple = None,  # None = keep original size
        high_quality: bool = True
    ) -> None:
        """
        Combine multiple images into a single PDF

        Args:
            image_paths: List of image file paths (PNG/JPG)
            output_pdf: Output PDF file path
            title: PDF document title
            page_size: (width, height) in pixels, None to keep original
            high_quality: Use high quality settings (default: True)

        Note:
            Requires: pip install pillow
        """
        if not image_paths:
            raise ValueError("No images provided")

        # Convert all images to RGB (required for PDF)
        images = []

        for img_path in image_paths:
            if not img_path.exists():
                print(f"[WARNING] Image not found: {img_path}")
                continue

            try:
                img = Image.open(img_path)

                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')

                # Resize only if page_size is specified
                if page_size:
                    img = img.resize(page_size, Image.Resampling.LANCZOS)

                images.append(img)

            except Exception as e:
                print(f"[ERROR] Failed to load {img_path}: {e}")

        if not images:
            raise ValueError("No valid images to export")

        # Save as PDF with high quality settings
        dpi = 300 if high_quality else 100  # 300 DPI for high quality

        images[0].save(
            output_pdf,
            save_all=True,
            append_images=images[1:],
            resolution=dpi,
            quality=95,  # High JPEG quality
            optimize=False,  # Don't optimize, keep quality
            title=title,
            author="RF Analyzer"
        )

        print(f"[OK] PDF created: {output_pdf}")
        print(f"  Pages: {len(images)}")
        print(f"  File size: {output_pdf.stat().st_size / (1024*1024):.1f} MB")

    @staticmethod
    def create_report_from_directory(
        image_dir: Path,
        output_pdf: Path,
        pattern: str = "*.png",
        sort_by_name: bool = True
    ) -> None:
        """
        Create PDF report from all images in a directory

        Args:
            image_dir: Directory containing images
            output_pdf: Output PDF file path
            pattern: File pattern (e.g., "*.png", "B41_*.png")
            sort_by_name: Sort images by filename
        """
        if not image_dir.exists():
            raise ValueError(f"Directory not found: {image_dir}")

        # Find all matching images
        image_paths = list(image_dir.glob(pattern))

        if not image_paths:
            raise ValueError(f"No images found matching pattern: {pattern}")

        # Sort by filename
        if sort_by_name:
            image_paths.sort()

        print(f"Found {len(image_paths)} images in {image_dir}")
        print(f"Creating PDF report...")

        PDFExporter.images_to_pdf(
            image_paths=image_paths,
            output_pdf=output_pdf,
            title=f"RF Analysis Report - {datetime.now().strftime('%Y-%m-%d')}"
        )

    @staticmethod
    def create_filtered_report(
        image_dir: Path,
        output_pdf: Path,
        band: Optional[str] = None,
        lna_state: Optional[str] = None,
        input_port: Optional[str] = None
    ) -> None:
        """
        Create PDF report with filtered images

        Args:
            image_dir: Directory containing images
            output_pdf: Output PDF file path
            band: Filter by band (e.g., "B41")
            lna_state: Filter by LNA state (e.g., "G0_H")
            input_port: Filter by input port (e.g., "ANT1")
        """
        # Build pattern
        parts = []
        if band:
            parts.append(band)
        else:
            parts.append("*")

        if lna_state:
            parts.append(lna_state)
        else:
            parts.append("*")

        if input_port:
            parts.append(input_port)
        else:
            parts.append("*")

        pattern = "_".join(parts) + ".png"

        PDFExporter.create_report_from_directory(
            image_dir=image_dir,
            output_pdf=output_pdf,
            pattern=pattern
        )


def main():
    """Example usage"""
    import argparse

    parser = argparse.ArgumentParser(description="Create PDF report from images")
    parser.add_argument('input_dir', type=str, help='Input directory with images')
    parser.add_argument('output_pdf', type=str, help='Output PDF file path')
    parser.add_argument('--pattern', '-p', type=str, default='*.png', help='File pattern')
    parser.add_argument('--band', '-b', type=str, help='Filter by band')
    parser.add_argument('--lna', '-l', type=str, help='Filter by LNA state')
    parser.add_argument('--port', '-P', type=str, help='Filter by input port')

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_pdf = Path(args.output_pdf)

    if args.band or args.lna or args.port:
        PDFExporter.create_filtered_report(
            image_dir=input_dir,
            output_pdf=output_pdf,
            band=args.band,
            lna_state=args.lna,
            input_port=args.port
        )
    else:
        PDFExporter.create_report_from_directory(
            image_dir=input_dir,
            output_pdf=output_pdf,
            pattern=args.pattern
        )


if __name__ == "__main__":
    main()
