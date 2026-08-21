"""
Database Manager Module - SQLite Database for Photo Catalog
Manages photo metadata, tags, ratings, and search functionality
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import logging


class PhotoDatabase:
    """
    SQLite database manager for photo cataloging and search
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file. If None, uses default location.
        """
        if db_path is None:
            db_dir = os.path.join(os.path.expanduser("~"), ".sd_organizer")
            os.makedirs(db_dir, exist_ok=True)
            db_path = os.path.join(db_dir, "photo_catalog.db")
        
        self.db_path = db_path
        self.logger = logging.getLogger("PhotoDatabase")
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Photos table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS photos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filepath TEXT UNIQUE NOT NULL,
                filename TEXT NOT NULL,
                file_extension TEXT,
                file_size INTEGER,
                import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- EXIF Data
                date_taken TIMESTAMP,
                camera_make TEXT,
                camera_model TEXT,
                lens_model TEXT,
                iso INTEGER,
                aperture TEXT,
                shutter_speed TEXT,
                focal_length TEXT,
                
                -- GPS Data
                gps_latitude REAL,
                gps_longitude REAL,
                gps_altitude REAL,
                
                -- Image Properties
                width INTEGER,
                height INTEGER,
                orientation INTEGER,
                
                -- User Metadata
                rating INTEGER DEFAULT 0,
                color_flag TEXT,
                event_name TEXT,
                description TEXT,
                
                -- Additional EXIF
                exif_json TEXT
            )
        """)
        
        # Tags table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tag_name TEXT UNIQUE NOT NULL,
                tag_category TEXT,
                created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Photo-Tags relationship (many-to-many)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS photo_tags (
                photo_id INTEGER,
                tag_id INTEGER,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (photo_id, tag_id),
                FOREIGN KEY (photo_id) REFERENCES photos(id) ON DELETE CASCADE,
                FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
            )
        """)
        
        # Import Sessions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS import_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_name TEXT,
                import_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                source_path TEXT,
                destination_path TEXT,
                files_imported INTEGER,
                total_size INTEGER,
                camera_brand TEXT
            )
        """)
        
        # Create indexes for better search performance
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_filepath ON photos(filepath)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date_taken ON photos(date_taken)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_camera_model ON photos(camera_model)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_rating ON photos(rating)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_event_name ON photos(event_name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_tag_name ON tags(tag_name)")
        
        conn.commit()
        conn.close()
        self.logger.info(f"Database initialized at {self.db_path}")
    
    def add_photo(self, photo_data: Dict) -> int:
        """
        Add photo to database
        
        Args:
            photo_data: Dictionary with photo information
            
        Returns:
            Photo ID in database
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO photos (
                    filepath, filename, file_extension, file_size,
                    date_taken, camera_make, camera_model, lens_model,
                    iso, aperture, shutter_speed, focal_length,
                    gps_latitude, gps_longitude, gps_altitude,
                    width, height, orientation,
                    rating, color_flag, event_name, description, exif_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                photo_data.get('filepath'),
                photo_data.get('filename'),
                photo_data.get('file_extension'),
                photo_data.get('file_size'),
                photo_data.get('date_taken'),
                photo_data.get('camera_make'),
                photo_data.get('camera_model'),
                photo_data.get('lens_model'),
                photo_data.get('iso'),
                photo_data.get('aperture'),
                photo_data.get('shutter_speed'),
                photo_data.get('focal_length'),
                photo_data.get('gps_latitude'),
                photo_data.get('gps_longitude'),
                photo_data.get('gps_altitude'),
                photo_data.get('width'),
                photo_data.get('height'),
                photo_data.get('orientation'),
                photo_data.get('rating', 0),
                photo_data.get('color_flag'),
                photo_data.get('event_name'),
                photo_data.get('description'),
                json.dumps(photo_data.get('exif_json', {}))
            ))
            
            photo_id = cursor.lastrowid
            conn.commit()
            self.logger.debug(f"Added photo: {photo_data.get('filename')} (ID: {photo_id})")
            return photo_id
            
        except Exception as e:
            self.logger.error(f"Error adding photo: {e}")
            conn.rollback()
            return -1
        finally:
            conn.close()
    
    def add_tag(self, tag_name: str, tag_category: str = None) -> int:
        """
        Add tag to database
        
        Args:
            tag_name: Tag name
            tag_category: Optional category (people, place, event, etc.)
            
        Returns:
            Tag ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO tags (tag_name, tag_category)
                VALUES (?, ?)
            """, (tag_name.lower(), tag_category))
            
            if cursor.lastrowid == 0:
                # Tag already exists, get its ID
                cursor.execute("SELECT id FROM tags WHERE tag_name = ?", (tag_name.lower(),))
                tag_id = cursor.fetchone()[0]
            else:
                tag_id = cursor.lastrowid
            
            conn.commit()
            return tag_id
            
        except Exception as e:
            self.logger.error(f"Error adding tag: {e}")
            return -1
        finally:
            conn.close()
    
    def tag_photo(self, photo_id: int, tag_names: List[str]):
        """
        Tag a photo with one or more tags
        
        Args:
            photo_id: Photo ID
            tag_names: List of tag names
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for tag_name in tag_names:
                # Get or create tag
                tag_id = self.add_tag(tag_name)
                
                # Link photo and tag
                cursor.execute("""
                    INSERT OR IGNORE INTO photo_tags (photo_id, tag_id)
                    VALUES (?, ?)
                """, (photo_id, tag_id))
            
            conn.commit()
            self.logger.debug(f"Tagged photo {photo_id} with {len(tag_names)} tags")
            
        except Exception as e:
            self.logger.error(f"Error tagging photo: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def update_photo_rating(self, photo_id: int, rating: int):
        """Update photo rating (0-5 stars)"""
        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE photos SET rating = ? WHERE id = ?", (rating, photo_id))
        conn.commit()
        conn.close()
    
    def update_photo_color_flag(self, photo_id: int, color: str):
        """Update photo color flag (red, green, yellow, blue, purple, none)"""
        valid_colors = ['red', 'green', 'yellow', 'blue', 'purple', 'none', None]
        if color not in valid_colors:
            raise ValueError(f"Invalid color flag: {color}")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE photos SET color_flag = ? WHERE id = ?", (color, photo_id))
        conn.commit()
        conn.close()
    
    def search_photos(self, 
                     date_from: str = None,
                     date_to: str = None,
                     camera_model: str = None,
                     lens_model: str = None,
                     iso_min: int = None,
                     iso_max: int = None,
                     rating_min: int = None,
                     tags: List[str] = None,
                     event_name: str = None,
                     has_gps: bool = None,
                     limit: int = 1000) -> List[Dict]:
        """
        Advanced photo search
        
        Args:
            date_from: Start date (YYYY-MM-DD)
            date_to: End date (YYYY-MM-DD)
            camera_model: Camera model filter
            lens_model: Lens model filter
            iso_min: Minimum ISO
            iso_max: Maximum ISO
            rating_min: Minimum rating (0-5)
            tags: List of tags to filter by
            event_name: Event name filter
            has_gps: Filter photos with/without GPS
            limit: Maximum results to return
            
        Returns:
            List of photo dictionaries
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        query = "SELECT * FROM photos WHERE 1=1"
        params = []
        
        if date_from:
            query += " AND date_taken >= ?"
            params.append(date_from)
        
        if date_to:
            query += " AND date_taken <= ?"
            params.append(date_to)
        
        if camera_model:
            query += " AND camera_model LIKE ?"
            params.append(f"%{camera_model}%")
        
        if lens_model:
            query += " AND lens_model LIKE ?"
            params.append(f"%{lens_model}%")
        
        if iso_min is not None:
            query += " AND iso >= ?"
            params.append(iso_min)
        
        if iso_max is not None:
            query += " AND iso <= ?"
            params.append(iso_max)
        
        if rating_min is not None:
            query += " AND rating >= ?"
            params.append(rating_min)
        
        if event_name:
            query += " AND event_name LIKE ?"
            params.append(f"%{event_name}%")
        
        if has_gps is not None:
            if has_gps:
                query += " AND gps_latitude IS NOT NULL AND gps_longitude IS NOT NULL"
            else:
                query += " AND (gps_latitude IS NULL OR gps_longitude IS NULL)"
        
        # Filter by tags if specified
        if tags:
            tag_placeholders = ','.join('?' * len(tags))
            query += f"""
                AND id IN (
                    SELECT photo_id FROM photo_tags
                    JOIN tags ON photo_tags.tag_id = tags.id
                    WHERE tags.tag_name IN ({tag_placeholders})
                    GROUP BY photo_id
                    HAVING COUNT(DISTINCT tags.id) = ?
                )
            """
            params.extend([tag.lower() for tag in tags])
            params.append(len(tags))
        
        query += f" ORDER BY date_taken DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return results
    
    def get_photo_tags(self, photo_id: int) -> List[str]:
        """Get all tags for a photo"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tags.tag_name
            FROM tags
            JOIN photo_tags ON tags.id = photo_tags.tag_id
            WHERE photo_tags.photo_id = ?
        """, (photo_id,))
        
        tags = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tags
    
    def get_all_tags(self) -> List[Dict]:
        """Get all available tags with usage count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT tags.id, tags.tag_name, tags.tag_category, COUNT(photo_tags.photo_id) as usage_count
            FROM tags
            LEFT JOIN photo_tags ON tags.id = photo_tags.tag_id
            GROUP BY tags.id
            ORDER BY usage_count DESC, tags.tag_name
        """)
        
        tags = [
            {
                'id': row[0],
                'name': row[1],
                'category': row[2],
                'usage_count': row[3]
            }
            for row in cursor.fetchall()
        ]
        conn.close()
        return tags
    
    def get_statistics(self) -> Dict:
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total photos
        cursor.execute("SELECT COUNT(*) FROM photos")
        total_photos = cursor.fetchone()[0]
        
        # Total size
        cursor.execute("SELECT SUM(file_size) FROM photos")
        total_size = cursor.fetchone()[0] or 0
        
        # Camera distribution
        cursor.execute("""
            SELECT camera_model, COUNT(*) as count
            FROM photos
            WHERE camera_model IS NOT NULL
            GROUP BY camera_model
            ORDER BY count DESC
            LIMIT 10
        """)
        camera_stats = [{'model': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # ISO distribution
        cursor.execute("""
            SELECT iso, COUNT(*) as count
            FROM photos
            WHERE iso IS NOT NULL
            GROUP BY iso
            ORDER BY iso
        """)
        iso_stats = [{'iso': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Rating distribution
        cursor.execute("""
            SELECT rating, COUNT(*) as count
            FROM photos
            GROUP BY rating
            ORDER BY rating DESC
        """)
        rating_stats = [{'rating': row[0], 'count': row[1]} for row in cursor.fetchall()]
        
        # Photos with GPS
        cursor.execute("""
            SELECT COUNT(*) FROM photos
            WHERE gps_latitude IS NOT NULL AND gps_longitude IS NOT NULL
        """)
        photos_with_gps = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_photos': total_photos,
            'total_size_gb': round(total_size / (1024**3), 2),
            'camera_stats': camera_stats,
            'iso_stats': iso_stats,
            'rating_stats': rating_stats,
            'photos_with_gps': photos_with_gps
        }
    
    def add_import_session(self, session_data: Dict) -> int:
        """Record import session details"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO import_sessions (
                session_name, source_path, destination_path,
                files_imported, total_size, camera_brand
            ) VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session_data.get('session_name'),
            session_data.get('source_path'),
            session_data.get('destination_path'),
            session_data.get('files_imported', 0),
            session_data.get('total_size', 0),
            session_data.get('camera_brand')
        ))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id
    
    def get_photo_by_filepath(self, filepath: str) -> Optional[Dict]:
        """Get photo data by filepath"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM photos WHERE filepath = ?", (filepath,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
