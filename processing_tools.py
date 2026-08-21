"""
Processing Tools Module - Image Processing Utilities
Auto-rotate, RAW conversion, resize, watermark, batch rename
"""
import os
import shutil
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from PIL.ExifTags import TAGS

# RAW processing - optional dependency
try:
    import rawpy
    import imageio
    RAW_SUPPORT = True
except ImportError:
    RAW_SUPPORT = False
    print("Warning: rawpy/imageio not installed. RAW conversion disabled.")
    print("Install with: pip install rawpy imageio")

from typing import List, Dict, Optional, Tuple
import logging


class ImageProcessor:
    """
    Image processing toolkit for basic operations
    """
    
    def __init__(self):
        self.logger = logging.getLogger("ImageProcessor")
    
    def auto_rotate_from_exif(self, image_path: str, output_path: str = None) -> bool:
        """
        Auto-rotate image based on EXIF orientation
        
        Args:
            image_path: Path to source image
            output_path: Path to save rotated image (if None, overwrites source)
            
        Returns:
            True if rotation was applied
        """
        try:
            img = Image.open(image_path)
            
            # Get EXIF orientation
            exif = img.getexif()
            orientation = exif.get(274)  # 274 is the orientation tag
            
            if orientation:
                rotations = {
                    3: 180,
                    6: 270,
                    8: 90
                }
                
                if orientation in rotations:
                    img = img.rotate(rotations[orientation], expand=True)
                    
                    # Save
                    if output_path is None:
                        output_path = image_path
                    
                    img.save(output_path, quality=95, optimize=True)
                    self.logger.info(f"Auto-rotated: {os.path.basename(image_path)}")
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error auto-rotating {image_path}: {e}")
            return False
    
    def convert_raw_to_jpeg(self, 
                           raw_path: str, 
                           output_path: str = None,
                           quality: int = 95,
                           resize: Tuple[int, int] = None) -> Optional[str]:
        """
        Convert RAW file to JPEG
        
        Args:
            raw_path: Path to RAW file
            output_path: Output JPEG path (if None, uses same name with .jpg)
            quality: JPEG quality (1-100)
            resize: Optional (width, height) tuple for resizing
            
        Returns:
            Path to created JPEG or None if failed
        """
        if not RAW_SUPPORT:
            self.logger.error("RAW conversion not available. Install rawpy and imageio.")
            return None
        
        try:
            # Read RAW file
            with rawpy.imread(raw_path) as raw:
                # Convert to RGB array
                rgb = raw.postprocess(
                    use_camera_wb=True,
                    half_size=False,
                    no_auto_bright=False,
                    output_bps=8
                )
            
            # Convert to PIL Image
            img = Image.fromarray(rgb)
            
            # Resize if requested
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)
            
            # Determine output path
            if output_path is None:
                base = os.path.splitext(raw_path)[0]
                output_path = f"{base}.jpg"
            
            # Save JPEG
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
            self.logger.info(f"Converted RAW to JPEG: {os.path.basename(output_path)}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error converting RAW {raw_path}: {e}")
            return None
    
    def resize_image(self, 
                    image_path: str,
                    output_path: str = None,
                    max_width: int = None,
                    max_height: int = None,
                    quality: int = 90) -> Optional[str]:
        """
        Resize image maintaining aspect ratio
        
        Args:
            image_path: Source image path
            output_path: Output path (if None, overwrites source)
            max_width: Maximum width
            max_height: Maximum height
            quality: JPEG quality
            
        Returns:
            Path to resized image
        """
        try:
            img = Image.open(image_path)
            original_width, original_height = img.size
            
            # Calculate new dimensions
            if max_width and max_height:
                # Fit within box
                ratio = min(max_width / original_width, max_height / original_height)
            elif max_width:
                ratio = max_width / original_width
            elif max_height:
                ratio = max_height / original_height
            else:
                return image_path  # No resizing needed
            
            if ratio >= 1.0:
                return image_path  # Don't upscale
            
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            # Resize
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Determine output
            if output_path is None:
                base, ext = os.path.splitext(image_path)
                output_path = f"{base}_resized{ext}"
            
            # Save
            img_resized.save(output_path, quality=quality, optimize=True)
            self.logger.info(f"Resized: {os.path.basename(image_path)} to {new_width}x{new_height}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error resizing {image_path}: {e}")
            return None
    
    def add_watermark(self,
                     image_path: str,
                     watermark_text: str,
                     output_path: str = None,
                     position: str = 'bottom-right',
                     opacity: float = 0.5,
                     font_size: int = None) -> Optional[str]:
        """
        Add text watermark to image
        
        Args:
            image_path: Source image path
            watermark_text: Text to add
            output_path: Output path (if None, overwrites source)
            position: Position (bottom-right, bottom-left, top-right, top-left, center)
            opacity: Watermark opacity (0.0 to 1.0)
            font_size: Font size (if None, calculated based on image size)
            
        Returns:
            Path to watermarked image
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # Create transparent overlay
            overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(overlay)
            
            # Calculate font size if not specified
            if font_size is None:
                font_size = int(height * 0.03)  # 3% of image height
            
            # Try to load a nice font, fallback to default
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size)
            except:
                try:
                    font = ImageFont.truetype("arial.ttf", font_size)
                except:
                    font = ImageFont.load_default()
            
            # Get text bounding box
            bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position
            margin = int(height * 0.02)  # 2% margin
            
            positions = {
                'bottom-right': (width - text_width - margin, height - text_height - margin),
                'bottom-left': (margin, height - text_height - margin),
                'top-right': (width - text_width - margin, margin),
                'top-left': (margin, margin),
                'center': ((width - text_width) // 2, (height - text_height) // 2)
            }
            
            xy = positions.get(position, positions['bottom-right'])
            
            # Draw text with opacity
            alpha = int(255 * opacity)
            draw.text(xy, watermark_text, fill=(255, 255, 255, alpha), font=font)
            
            # Composite images
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            watermarked = Image.alpha_composite(img, overlay)
            
            # Convert back to RGB for JPEG
            if watermarked.mode == 'RGBA':
                background = Image.new('RGB', watermarked.size, (255, 255, 255))
                background.paste(watermarked, mask=watermarked.split()[3])
                watermarked = background
            
            # Save
            if output_path is None:
                base, ext = os.path.splitext(image_path)
                output_path = f"{base}_watermarked{ext}"
            
            watermarked.save(output_path, quality=95, optimize=True)
            self.logger.info(f"Watermarked: {os.path.basename(image_path)}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error watermarking {image_path}: {e}")
            return None
    
    def batch_rename(self,
                    files: List[str],
                    template: str,
                    start_number: int = 1,
                    dry_run: bool = False) -> List[Dict[str, str]]:
        """
        Batch rename files with template
        
        Args:
            files: List of file paths
            template: Naming template with variables:
                      {name} - original name
                      {date} - YYYY-MM-DD from EXIF
                      {time} - HHMMSS from EXIF
                      {camera} - camera model
                      {num} - sequential number
                      {num:04d} - zero-padded number
            start_number: Starting number for sequential numbering
            dry_run: If True, only simulate renaming
            
        Returns:
            List of dictionaries with 'old_path' and 'new_path'
        """
        renames = []
        counter = start_number
        
        for file_path in files:
            try:
                directory = os.path.dirname(file_path)
                original_name = os.path.splitext(os.path.basename(file_path))[0]
                extension = os.path.splitext(file_path)[1]
                
                # Get EXIF data if available
                date_str = ""
                time_str = ""
                camera_str = ""
                
                try:
                    img = Image.open(file_path)
                    exif = img.getexif()
                    
                    # Date taken
                    date_taken = exif.get(36867) or exif.get(306)  # DateTimeOriginal or DateTime
                    if date_taken:
                        parts = date_taken.split(' ')
                        if len(parts) == 2:
                            date_str = parts[0].replace(':', '-')
                            time_str = parts[1].replace(':', '')
                    
                    # Camera model
                    camera_str = exif.get(272, "") or exif.get(271, "")  # Model or Make
                    camera_str = camera_str.replace(' ', '_')
                    
                except:
                    pass
                
                # Build new filename
                new_name = template
                new_name = new_name.replace('{name}', original_name)
                new_name = new_name.replace('{date}', date_str)
                new_name = new_name.replace('{time}', time_str)
                new_name = new_name.replace('{camera}', camera_str)
                
                # Handle numbered formats
                if '{num' in new_name:
                    # Check for format specifier like {num:04d}
                    import re
                    num_pattern = r'\{num(?::(\d+)d)?\}'
                    match = re.search(num_pattern, new_name)
                    if match:
                        if match.group(1):
                            # Zero-padded
                            width = int(match.group(1))
                            new_name = re.sub(num_pattern, str(counter).zfill(width), new_name)
                        else:
                            # No padding
                            new_name = new_name.replace('{num}', str(counter))
                
                new_name = new_name + extension
                new_path = os.path.join(directory, new_name)
                
                # Avoid conflicts
                if os.path.exists(new_path) and new_path != file_path:
                    base, ext = os.path.splitext(new_path)
                    suffix = 1
                    while os.path.exists(f"{base}_{suffix}{ext}"):
                        suffix += 1
                    new_path = f"{base}_{suffix}{ext}"
                
                renames.append({
                    'old_path': file_path,
                    'new_path': new_path,
                    'old_name': os.path.basename(file_path),
                    'new_name': os.path.basename(new_path)
                })
                
                # Perform rename if not dry run
                if not dry_run and file_path != new_path:
                    os.rename(file_path, new_path)
                    self.logger.info(f"Renamed: {os.path.basename(file_path)} → {os.path.basename(new_path)}")
                
                counter += 1
                
            except Exception as e:
                self.logger.error(f"Error renaming {file_path}: {e}")
        
        return renames
    
    def create_web_version(self,
                          image_path: str,
                          output_dir: str,
                          max_dimension: int = 1920,
                          quality: int = 85) -> Optional[str]:
        """
        Create web-optimized version of image
        
        Args:
            image_path: Source image
            output_dir: Output directory
            max_dimension: Maximum width or height
            quality: JPEG quality
            
        Returns:
            Path to web version
        """
        try:
            img = Image.open(image_path)
            width, height = img.size
            
            # Calculate new size
            if width > height:
                if width > max_dimension:
                    new_width = max_dimension
                    new_height = int(height * (max_dimension / width))
                else:
                    return None  # Already small enough
            else:
                if height > max_dimension:
                    new_height = max_dimension
                    new_width = int(width * (max_dimension / height))
                else:
                    return None  # Already small enough
            
            # Resize
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save
            filename = os.path.basename(image_path)
            base, _ = os.path.splitext(filename)
            output_path = os.path.join(output_dir, f"{base}_web.jpg")
            
            # Convert to RGB if needed
            if img_resized.mode != 'RGB':
                img_resized = img_resized.convert('RGB')
            
            img_resized.save(output_path, 'JPEG', quality=quality, optimize=True)
            self.logger.info(f"Created web version: {os.path.basename(output_path)}")
            
            return output_path
            
        except Exception as e:
            self.logger.error(f"Error creating web version {image_path}: {e}")
            return None


class BatchProcessor:
    """
    Batch processing coordinator
    """
    
    def __init__(self):
        self.processor = ImageProcessor()
        self.logger = logging.getLogger("BatchProcessor")
    
    def process_batch(self,
                     files: List[str],
                     operations: List[Dict],
                     progress_callback=None) -> Dict:
        """
        Process multiple files with multiple operations
        
        Args:
            files: List of file paths
            operations: List of operation dicts with:
                       {'type': 'auto_rotate', ...}
                       {'type': 'convert_raw', 'quality': 95}
                       {'type': 'resize', 'max_width': 1920}
                       {'type': 'watermark', 'text': '© 2025', 'position': 'bottom-right'}
                       {'type': 'rename', 'template': '{date}_{num:04d}'}
            progress_callback: Optional callback(current, total, filename)
            
        Returns:
            Statistics dictionary
        """
        stats = {
            'total': len(files),
            'processed': 0,
            'failed': 0,
            'operations': {op['type']: 0 for op in operations}
        }
        
        for idx, file_path in enumerate(files):
            try:
                current_file = file_path
                
                for operation in operations:
                    op_type = operation['type']
                    
                    if op_type == 'auto_rotate':
                        self.processor.auto_rotate_from_exif(current_file)
                        stats['operations']['auto_rotate'] += 1
                    
                    elif op_type == 'convert_raw':
                        quality = operation.get('quality', 95)
                        result = self.processor.convert_raw_to_jpeg(
                            current_file,
                            quality=quality
                        )
                        if result:
                            current_file = result
                            stats['operations']['convert_raw'] += 1
                    
                    elif op_type == 'resize':
                        max_width = operation.get('max_width')
                        max_height = operation.get('max_height')
                        quality = operation.get('quality', 90)
                        result = self.processor.resize_image(
                            current_file,
                            max_width=max_width,
                            max_height=max_height,
                            quality=quality
                        )
                        if result:
                            stats['operations']['resize'] += 1
                    
                    elif op_type == 'watermark':
                        text = operation.get('text', '© 2025')
                        position = operation.get('position', 'bottom-right')
                        opacity = operation.get('opacity', 0.5)
                        result = self.processor.add_watermark(
                            current_file,
                            text,
                            position=position,
                            opacity=opacity
                        )
                        if result:
                            stats['operations']['watermark'] += 1
                    
                    elif op_type == 'web_version':
                        output_dir = operation.get('output_dir')
                        max_dim = operation.get('max_dimension', 1920)
                        quality = operation.get('quality', 85)
                        result = self.processor.create_web_version(
                            current_file,
                            output_dir,
                            max_dim,
                            quality
                        )
                        if result:
                            stats['operations']['web_version'] += 1
                
                stats['processed'] += 1
                
                if progress_callback:
                    progress_callback(idx + 1, len(files), os.path.basename(file_path))
                
            except Exception as e:
                self.logger.error(f"Error processing {file_path}: {e}")
                stats['failed'] += 1
        
        return stats
