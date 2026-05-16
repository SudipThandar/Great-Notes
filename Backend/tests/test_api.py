"""
Automated API Testing Script for Great Notes Backend
Run this script to test all API endpoints systematically.

Prerequisites:
- Backend server running on http://localhost:8000
- Database migration executed in Supabase
- Valid JWT token (set as environment variable or pass as argument)

Usage:
    python tests/test_api.py --token YOUR_JWT_TOKEN
    or
    set TOKEN=YOUR_JWT_TOKEN
    python tests/test_api.py
"""

import requests
import json
import sys
import os
from typing import Optional, Dict, Any
import argparse


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


class APITester:
    def __init__(self, base_url: str, token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.headers = {}
        if token:
            self.headers['Authorization'] = f'Bearer {token}'
        
        self.passed = 0
        self.failed = 0
        self.test_data = {}  # Store created resources for cleanup
    
    def print_header(self, text: str):
        """Print section header"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")
    
    def print_test(self, name: str, passed: bool, details: str = ""):
        """Print test result"""
        status = f"{Colors.GREEN}✓ PASS{Colors.RESET}" if passed else f"{Colors.RED}✗ FAIL{Colors.RESET}"
        print(f"{status} - {name}")
        if details:
            print(f"  {Colors.YELLOW}{details}{Colors.RESET}")
        
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def test_health_check(self):
        """Test health check endpoint"""
        self.print_header("1. Health Check Tests")
        
        try:
            response = requests.get(f"{self.base_url}/health")
            passed = response.status_code == 200 and response.json().get('status') == 'healthy'
            self.print_test(
                "GET /health returns 200 and healthy status",
                passed,
                f"Status: {response.status_code}, Response: {response.json()}"
            )
        except Exception as e:
            self.print_test("GET /health returns 200 and healthy status", False, str(e))
    
    def test_authentication(self):
        """Test authentication endpoints"""
        self.print_header("2. Authentication Tests")
        
        # Test with valid token
        if self.token:
            try:
                response = requests.get(
                    f"{self.base_url}/api/auth/me",
                    headers=self.headers
                )
                passed = response.status_code == 200 and 'id' in response.json()
                self.print_test(
                    "GET /api/auth/me with valid token returns user info",
                    passed,
                    f"Status: {response.status_code}, User ID: {response.json().get('id', 'N/A')}"
                )
                
                # Store user_id for later tests
                if passed:
                    self.test_data['user_id'] = response.json()['id']
            except Exception as e:
                self.print_test("GET /api/auth/me with valid token returns user info", False, str(e))
        else:
            self.print_test("GET /api/auth/me with valid token returns user info", False, "No token provided")
        
        # Test without token
        try:
            response = requests.get(f"{self.base_url}/api/auth/me")
            passed = response.status_code == 401
            self.print_test(
                "GET /api/auth/me without token returns 401",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("GET /api/auth/me without token returns 401", False, str(e))
        
        # Test with invalid token
        try:
            response = requests.get(
                f"{self.base_url}/api/auth/me",
                headers={'Authorization': 'Bearer invalid_token_12345'}
            )
            passed = response.status_code == 401
            self.print_test(
                "GET /api/auth/me with invalid token returns 401",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("GET /api/auth/me with invalid token returns 401", False, str(e))
        
        # Test logout
        if self.token:
            try:
                response = requests.post(
                    f"{self.base_url}/api/auth/logout",
                    headers=self.headers
                )
                passed = response.status_code == 204
                self.print_test(
                    "POST /api/auth/logout returns 204",
                    passed,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.print_test("POST /api/auth/logout returns 204", False, str(e))
    
    def test_notes_crud(self):
        """Test notes CRUD operations"""
        self.print_header("3. Notes CRUD Tests")
        
        if not self.token:
            self.print_test("Notes CRUD tests", False, "No token provided - skipping")
            return
        
        # Create a note
        try:
            note_data = {
                "title": "Test Note",
                "content": "This is a test note content",
                "is_favorite": False
            }
            response = requests.post(
                f"{self.base_url}/api/notes",
                headers=self.headers,
                json=note_data
            )
            passed = response.status_code == 201 and 'id' in response.json()
            self.print_test(
                "POST /api/notes creates note successfully",
                passed,
                f"Status: {response.status_code}, Note ID: {response.json().get('id', 'N/A')}"
            )
            
            if passed:
                self.test_data['note_id'] = response.json()['id']
        except Exception as e:
            self.print_test("POST /api/notes creates note successfully", False, str(e))
        
        # Get all notes
        try:
            response = requests.get(
                f"{self.base_url}/api/notes",
                headers=self.headers
            )
            passed = response.status_code == 200 and isinstance(response.json(), list)
            self.print_test(
                "GET /api/notes returns list of notes",
                passed,
                f"Status: {response.status_code}, Count: {len(response.json()) if passed else 0}"
            )
        except Exception as e:
            self.print_test("GET /api/notes returns list of notes", False, str(e))
        
        # Get single note
        if 'note_id' in self.test_data:
            try:
                response = requests.get(
                    f"{self.base_url}/api/notes/{self.test_data['note_id']}",
                    headers=self.headers
                )
                passed = response.status_code == 200 and response.json()['id'] == self.test_data['note_id']
                self.print_test(
                    "GET /api/notes/:id returns note if owned",
                    passed,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.print_test("GET /api/notes/:id returns note if owned", False, str(e))
        
        # Update note
        if 'note_id' in self.test_data:
            try:
                update_data = {
                    "title": "Updated Test Note",
                    "content": "Updated content",
                    "is_favorite": True
                }
                response = requests.put(
                    f"{self.base_url}/api/notes/{self.test_data['note_id']}",
                    headers=self.headers,
                    json=update_data
                )
                passed = response.status_code == 200 and response.json()['title'] == "Updated Test Note"
                self.print_test(
                    "PUT /api/notes/:id updates note successfully",
                    passed,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.print_test("PUT /api/notes/:id updates note successfully", False, str(e))
        
        # Test 404 for non-existent note
        try:
            response = requests.get(
                f"{self.base_url}/api/notes/00000000-0000-0000-0000-000000000000",
                headers=self.headers
            )
            passed = response.status_code == 404
            self.print_test(
                "GET /api/notes/:id returns 404 for non-existent note",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("GET /api/notes/:id returns 404 for non-existent note", False, str(e))
    
    def test_search_and_filter(self):
        """Test search and filter functionality"""
        self.print_header("4. Search and Filter Tests")
        
        if not self.token:
            self.print_test("Search and filter tests", False, "No token provided - skipping")
            return
        
        # Create test notes for search
        try:
            # Create a note with "search" in title
            requests.post(
                f"{self.base_url}/api/notes",
                headers=self.headers,
                json={"title": "Searchable Note", "content": "Content", "is_favorite": False}
            )
            
            # Create a favorite note
            requests.post(
                f"{self.base_url}/api/notes",
                headers=self.headers,
                json={"title": "Favorite Note", "content": "Content", "is_favorite": True}
            )
        except:
            pass
        
        # Test search
        try:
            response = requests.get(
                f"{self.base_url}/api/notes?search=search",
                headers=self.headers
            )
            passed = response.status_code == 200
            notes = response.json() if passed else []
            has_search_term = any('search' in note['title'].lower() for note in notes)
            self.print_test(
                "GET /api/notes?search=search filters by title",
                passed and has_search_term,
                f"Status: {response.status_code}, Found: {len(notes)} notes"
            )
        except Exception as e:
            self.print_test("GET /api/notes?search=search filters by title", False, str(e))
        
        # Test favorites filter
        try:
            response = requests.get(
                f"{self.base_url}/api/notes?favorites=true",
                headers=self.headers
            )
            passed = response.status_code == 200
            notes = response.json() if passed else []
            all_favorites = all(note['is_favorite'] for note in notes) if notes else True
            self.print_test(
                "GET /api/notes?favorites=true returns only favorites",
                passed and all_favorites,
                f"Status: {response.status_code}, Found: {len(notes)} favorites"
            )
        except Exception as e:
            self.print_test("GET /api/notes?favorites=true returns only favorites", False, str(e))
    
    def test_trash_operations(self):
        """Test trash and restore functionality"""
        self.print_header("5. Trash Operations Tests")
        
        if not self.token or 'note_id' not in self.test_data:
            self.print_test("Trash operations tests", False, "No token or note_id - skipping")
            return
        
        # Soft delete note
        try:
            response = requests.delete(
                f"{self.base_url}/api/notes/{self.test_data['note_id']}",
                headers=self.headers
            )
            passed = response.status_code == 204
            self.print_test(
                "DELETE /api/notes/:id soft deletes note",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("DELETE /api/notes/:id soft deletes note", False, str(e))
        
        # Get trash notes
        try:
            response = requests.get(
                f"{self.base_url}/api/notes/trash",
                headers=self.headers
            )
            passed = response.status_code == 200 and isinstance(response.json(), list)
            self.print_test(
                "GET /api/notes/trash returns deleted notes",
                passed,
                f"Status: {response.status_code}, Count: {len(response.json()) if passed else 0}"
            )
        except Exception as e:
            self.print_test("GET /api/notes/trash returns deleted notes", False, str(e))
        
        # Restore note
        try:
            response = requests.post(
                f"{self.base_url}/api/notes/{self.test_data['note_id']}/restore",
                headers=self.headers
            )
            passed = response.status_code == 200
            self.print_test(
                "POST /api/notes/:id/restore restores note from trash",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("POST /api/notes/:id/restore restores note from trash", False, str(e))
        
        # Delete again for permanent delete test
        try:
            requests.delete(
                f"{self.base_url}/api/notes/{self.test_data['note_id']}",
                headers=self.headers
            )
        except:
            pass
        
        # Permanent delete
        try:
            response = requests.delete(
                f"{self.base_url}/api/notes/{self.test_data['note_id']}/permanent",
                headers=self.headers
            )
            passed = response.status_code == 204
            self.print_test(
                "DELETE /api/notes/:id/permanent removes from database",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("DELETE /api/notes/:id/permanent removes from database", False, str(e))
    
    def test_sharing(self):
        """Test note sharing functionality"""
        self.print_header("6. Sharing Tests")
        
        if not self.token:
            self.print_test("Sharing tests", False, "No token provided - skipping")
            return
        
        # Create a note for sharing
        try:
            response = requests.post(
                f"{self.base_url}/api/notes",
                headers=self.headers,
                json={"title": "Shared Note", "content": "This will be shared", "is_favorite": False}
            )
            if response.status_code == 201:
                share_note_id = response.json()['id']
                self.test_data['share_note_id'] = share_note_id
        except:
            pass
        
        if 'share_note_id' not in self.test_data:
            self.print_test("Sharing tests", False, "Failed to create note for sharing")
            return
        
        # Generate share link
        try:
            response = requests.post(
                f"{self.base_url}/api/notes/{self.test_data['share_note_id']}/share",
                headers=self.headers
            )
            passed = response.status_code == 200 and 'share_token' in response.json()
            if passed:
                self.test_data['share_token'] = response.json()['share_token']
            self.print_test(
                "POST /api/notes/:id/share generates share link",
                passed,
                f"Status: {response.status_code}, Token: {response.json().get('share_token', 'N/A')}"
            )
        except Exception as e:
            self.print_test("POST /api/notes/:id/share generates share link", False, str(e))
        
        # Get shared note (no auth)
        if 'share_token' in self.test_data:
            try:
                response = requests.get(
                    f"{self.base_url}/api/share/{self.test_data['share_token']}"
                )
                passed = response.status_code == 200 and 'title' in response.json()
                self.print_test(
                    "GET /api/share/:token returns note without auth",
                    passed,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.print_test("GET /api/share/:token returns note without auth", False, str(e))
        
        # Revoke share
        if 'share_note_id' in self.test_data:
            try:
                response = requests.delete(
                    f"{self.base_url}/api/notes/{self.test_data['share_note_id']}/share",
                    headers=self.headers
                )
                passed = response.status_code == 204
                self.print_test(
                    "DELETE /api/notes/:id/share revokes share access",
                    passed,
                    f"Status: {response.status_code}"
                )
            except Exception as e:
                self.print_test("DELETE /api/notes/:id/share revokes share access", False, str(e))
        
        # Test 404 for invalid share token
        try:
            response = requests.get(
                f"{self.base_url}/api/share/invalid_token_12345"
            )
            passed = response.status_code == 404
            self.print_test(
                "GET /api/share/:token returns 404 for invalid token",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("GET /api/share/:token returns 404 for invalid token", False, str(e))
        
        # Cleanup: delete the shared note
        if 'share_note_id' in self.test_data:
            try:
                requests.delete(
                    f"{self.base_url}/api/notes/{self.test_data['share_note_id']}",
                    headers=self.headers
                )
                requests.delete(
                    f"{self.base_url}/api/notes/{self.test_data['share_note_id']}/permanent",
                    headers=self.headers
                )
            except:
                pass
    
    def test_error_handling(self):
        """Test error handling"""
        self.print_header("7. Error Handling Tests")
        
        if not self.token:
            self.print_test("Error handling tests", False, "No token provided - skipping")
            return
        
        # Test invalid JSON
        try:
            response = requests.post(
                f"{self.base_url}/api/notes",
                headers={**self.headers, 'Content-Type': 'application/json'},
                data="invalid json"
            )
            passed = response.status_code == 422
            self.print_test(
                "Invalid JSON returns 422",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("Invalid JSON returns 422", False, str(e))
        
        # Test invalid UUID
        try:
            response = requests.get(
                f"{self.base_url}/api/notes/not-a-uuid",
                headers=self.headers
            )
            passed = response.status_code in [400, 422, 500]  # Different frameworks handle this differently
            self.print_test(
                "Invalid UUID returns error",
                passed,
                f"Status: {response.status_code}"
            )
        except Exception as e:
            self.print_test("Invalid UUID returns error", False, str(e))
    
    def print_summary(self):
        """Print test summary"""
        self.print_header("Test Summary")
        
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"{Colors.GREEN}Passed: {self.passed}{Colors.RESET}")
        print(f"{Colors.RED}Failed: {self.failed}{Colors.RESET}")
        print(f"Pass Rate: {pass_rate:.1f}%\n")
        
        if self.failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ All tests passed!{Colors.RESET}\n")
        else:
            print(f"{Colors.RED}{Colors.BOLD}✗ Some tests failed. Please review the output above.{Colors.RESET}\n")
    
    def run_all_tests(self):
        """Run all test suites"""
        print(f"\n{Colors.BOLD}Great Notes Backend API Test Suite{Colors.RESET}")
        print(f"Testing: {self.base_url}\n")
        
        self.test_health_check()
        self.test_authentication()
        self.test_notes_crud()
        self.test_search_and_filter()
        self.test_trash_operations()
        self.test_sharing()
        self.test_error_handling()
        
        self.print_summary()
        
        return self.failed == 0


def main():
    parser = argparse.ArgumentParser(description='Test Great Notes Backend API')
    parser.add_argument('--token', type=str, help='JWT authentication token')
    parser.add_argument('--url', type=str, default='http://localhost:8000', help='Base URL of the API')
    
    args = parser.parse_args()
    
    # Get token from args or environment
    token = args.token or os.environ.get('TOKEN')
    
    if not token:
        print(f"{Colors.YELLOW}Warning: No authentication token provided.{Colors.RESET}")
        print(f"{Colors.YELLOW}Some tests will be skipped.{Colors.RESET}")
        print(f"{Colors.YELLOW}Set TOKEN environment variable or use --token argument.{Colors.RESET}\n")
    
    tester = APITester(args.url, token)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
