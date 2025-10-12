"""
Google Books API service for fetching book information.
"""

import logging
from datetime import datetime
from typing import List, Dict, Optional
import requests

logger = logging.getLogger(__name__)


class GoogleBooksService:
    """Service class for interacting with Google Books API."""

    BASE_URL = "https://www.googleapis.com/books/v1"

    @classmethod
    def search_books(
        cls, title: str, author: str = None, max_results: int = 10
    ) -> List[Dict]:
        """
        Search for books using title and optionally author.

        Args:
            title: Book title to search for
            author: Optional author name
            max_results: Maximum number of results to return (1-40)

        Returns:
            List of book dictionaries with standardized fields
        """
        try:
            # Construct search query
            query = f'intitle:"{title}"'
            if author:
                query += f'+inauthor:"{author}"'

            params = {
                "q": query,
                "maxResults": min(max_results, 40),  # API limit is 40
                "printType": "books",
            }

            response = requests.get(
                f"{cls.BASE_URL}/volumes", params=params, timeout=10
            )
            response.raise_for_status()

            data = response.json()
            books = []

            if "items" in data:
                for item in data["items"]:
                    book_data = cls._format_book_data(item)
                    if book_data:  # Only add if we got valid data
                        books.append(book_data)

            return books

        except requests.exceptions.Timeout:
            logger.error("Google Books API request timed out")
            return []
        except requests.exceptions.RequestException as e:
            logger.error("Error calling Google Books API: %s", e)
            return []
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Data formatting error in search_books: %s", e)
            return []

    @classmethod
    def get_book_by_id(cls, google_books_id: str) -> Optional[Dict]:
        """
        Get detailed book information by Google Books ID.

        Args:
            google_books_id: The Google Books volume ID

        Returns:
            Book dictionary with standardized fields or None if not found
        """
        try:
            response = requests.get(
                f"{cls.BASE_URL}/volumes/{google_books_id}", timeout=10
            )
            response.raise_for_status()
            data = response.json()
            return cls._format_book_data(data)

        except requests.exceptions.RequestException as e:
            logger.error("Error fetching book by ID %s: %s", google_books_id, e)
            return None
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Data formatting error in get_book_by_id: %s", e)
            return None

    @classmethod
    def _format_book_data(cls, item: Dict) -> Optional[Dict]:
        """
        Format raw Google Books API response into standardized book data.

        Args:
            item: Raw book item from Google Books API

        Returns:
            Formatted book dictionary or None if required fields missing
        """
        try:
            volume_info = item.get("volumeInfo", {})

            # Required fields
            title = volume_info.get("title")
            if not title:
                return None

            # Extract authors
            authors = volume_info.get("authors", [])
            author = ", ".join(authors) if authors else "Unknown Author"

            # Extract publication date
            published_date = volume_info.get("publishedDate")
            parsed_date = None
            if published_date:
                try:
                    # Try different date formats
                    for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
                        try:
                            parsed_date = datetime.strptime(published_date, fmt).date()
                            break
                        except ValueError:
                            continue
                except ValueError:
                    pass

            # Extract cover image
            image_links = volume_info.get("imageLinks", {})
            cover_url = (
                image_links.get("extraLarge")
                or image_links.get("large")
                or image_links.get("medium")
                or image_links.get("small")
                or image_links.get("thumbnail")
            )

            # Extract genres/categories
            categories = volume_info.get("categories", [])
            genres = ", ".join(categories) if categories else ""

            # Extract description
            description = volume_info.get("description", "")

            # Extract other useful info (commented out for simplified version)
            # page_count = volume_info.get('pageCount')
            # publisher = volume_info.get('publisher', '')
            # isbn_list = volume_info.get('industryIdentifiers', [])
            # isbn = None
            # for identifier in isbn_list:
            #     if identifier.get('type') in ['ISBN_13', 'ISBN_10']:
            #         isbn = identifier.get('identifier')
            #         break

            return {
                # 'google_books_id': item.get('id'),
                "title": title,
                "author": author,
                "published": parsed_date.isoformat() if parsed_date else None,
                "description": description,
                "genres": genres,
                "cover_url": cover_url,
                # 'publisher': publisher,
                # 'page_count': page_count,
                # 'isbn': isbn,
                "preview_link": volume_info.get("previewLink", ""),
                "info_link": volume_info.get("infoLink", ""),
                "subtitle": volume_info.get("subtitle", ""),
                "language": volume_info.get("language", "en"),
            }

        except (ValueError, KeyError, TypeError) as e:
            logger.error("Error formatting book data: %s", e)
            return None
