import os
import cv2
from pathlib import Path
from augraphy import *


class EntropyEngine:
    """Applies realistic degradation effects to clean document images."""

    def __init__(self, intensity="medium"):
        """
        Initialize the entropy engine with a degradation pipeline.

        Args:
            intensity: Degradation level - 'light', 'medium', or 'heavy'
        """
        self.intensity = intensity
        self.pipeline = self._build_pipeline(intensity)

    def _build_pipeline(self, intensity):
        """
        Build an Augraphy pipeline with appropriate degradation effects.

        The pipeline simulates real-world document scanning artifacts:
        - Ink phase: bleeding, low ink
        - Paper phase: texture, dirt, scanner lines
        - Post phase: rotation, compression
        """
        if intensity == "light":
            ink_phase = [
                InkBleed(
                    intensity_range=(0.1, 0.2),
                    kernel_size=(3, 3),
                    severity=(0.2, 0.4),
                    p=0.3
                )
            ]
            paper_phase = [
                NoiseTexturize(
                    sigma_range=(3, 7),
                    turbulence_range=(2, 4),
                    p=0.5
                )
            ]
            post_phase = [
                Geometric(
                    rotate_range=(-2, 2),
                    p=0.6
                )
            ]

        elif intensity == "heavy":
            ink_phase = [
                InkBleed(
                    intensity_range=(0.3, 0.5),
                    kernel_size=(5, 5),
                    severity=(0.5, 0.8),
                    p=0.7
                ),
                LowInkPeriodicLines(
                    count_range=(3, 6),
                    p=0.4
                )
            ]
            paper_phase = [
                NoiseTexturize(
                    sigma_range=(7, 15),
                    turbulence_range=(4, 8),
                    p=0.8
                ),
                DirtyRollers(
                    line_width_range=(2, 6),
                    p=0.6
                )
            ]
            post_phase = [
                Geometric(
                    rotate_range=(-5, 5),
                    p=0.9
                ),
                Jpeg(
                    quality_range=(40, 70),
                    p=0.7
                )
            ]

        else:  # medium (default)
            ink_phase = [
                InkBleed(
                    intensity_range=(0.15, 0.3),
                    kernel_size=(3, 5),
                    severity=(0.3, 0.6),
                    p=0.5
                )
            ]
            paper_phase = [
                NoiseTexturize(
                    sigma_range=(5, 10),
                    turbulence_range=(3, 6),
                    p=0.6
                ),
                DirtyRollers(
                    line_width_range=(1, 4),
                    p=0.4
                )
            ]
            post_phase = [
                Geometric(
                    rotate_range=(-3, 3),
                    p=0.7
                ),
                Jpeg(
                    quality_range=(60, 85),
                    p=0.5
                )
            ]

        return AugraphyPipeline(
            ink_phase=ink_phase,
            paper_phase=paper_phase,
            post_phase=post_phase
        )

    def degrade_image(
        self,
        image_path: str,
        output_dir="output/images_degraded"
    ) -> str:
        """
        Apply degradation effects to a clean image.

        Args:
            image_path: Path to the clean image
            output_dir: Directory to save the degraded image

        Returns:
            Path to the degraded image
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        # Load image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image: {image_path}")

        # Apply degradation pipeline
        degraded_image = self.pipeline.augment(image)["output"]

        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Generate output path (preserve filename)
        filename = Path(image_path).name
        output_path = os.path.join(output_dir, filename)

        # Save degraded image
        cv2.imwrite(output_path, degraded_image)

        return output_path

    def batch_degrade(
        self,
        image_dir="output/images_clean",
        output_dir="output/images_degraded"
    ):
        """
        Degrade all images in a directory.

        Args:
            image_dir: Directory containing clean images
            output_dir: Directory to save degraded images

        Returns:
            List of degraded image paths
        """
        image_path = Path(image_dir)
        if not image_path.exists():
            raise FileNotFoundError(f"Image directory not found: {image_dir}")

        # Support both PNG and JPEG
        image_files = list(image_path.glob("*.png")) + list(image_path.glob("*.jpg"))
        if not image_files:
            print(f"No image files found in {image_dir}")
            return []

        degraded_paths = []
        for img_file in image_files:
            try:
                deg_path = self.degrade_image(str(img_file), output_dir)
                degraded_paths.append(deg_path)
                print(f"Degraded: {img_file.name}")
            except Exception as e:
                print(f"Error degrading {img_file.name}: {e}")

        return degraded_paths


# Quick test if run directly
if __name__ == "__main__":
    print("Testing entropy engine...")
    engine = EntropyEngine(intensity="medium")

    # Degrade existing clean images
    images = engine.batch_degrade()
    print(f"\nDegraded {len(images)} image(s)")

    if images:
        print(f"First degraded image: {images[0]}")
