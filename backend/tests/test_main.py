
"""
Test suite for the TODO application API endpoints.
Production-ready tests with proper coverage and edge cases.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import InMemoryTodoStorage

client = TestClient(app)


class TestTodoAPI:
    """Test class for TODO API endpoints."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "app_name" in data
        assert "version" in data
    
    def test_get_empty_todos(self):
        """Test getting todos when none exist."""
        response = client.get("/api/todos")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_todo(self):
        """Test creating a new todo."""
        todo_data = {"title": "Test todo"}
        response = client.post("/api/todos", json=todo_data)
        
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Test todo"
        assert data["completed"] is False
        assert "id" in data
        assert "created_at" in data
    
    def test_create_todo_validation_error(self):
        """Test creating todo with invalid data."""
        # Empty title
        response = client.post("/api/todos", json={"title": ""})
        assert response.status_code == 400
        
        # Missing title
        response = client.post("/api/todos", json={})
        assert response.status_code == 422
    
    def test_get_todo_by_id(self):
        """Test getting a specific todo by ID."""
        # Create a todo first
        todo_data = {"title": "Test todo for retrieval"}
        create_response = client.post("/api/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Get the todo
        response = client.get(f"/api/todos/{todo_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test todo for retrieval"
    
    def test_get_nonexistent_todo(self):
        """Test getting a todo that doesn't exist."""
        response = client.get("/api/todos/999")
        assert response.status_code == 404
    
    def test_update_todo(self):
        """Test updating a todo."""
        # Create a todo first
        todo_data = {"title": "Todo to update"}
        create_response = client.post("/api/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Update the todo
        update_data = {"completed": True}
        response = client.put(f"/api/todos/{todo_id}", json=update_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["completed"] is True
        assert data["title"] == "Todo to update"
    
    def test_delete_todo(self):
        """Test deleting a todo."""
        # Create a todo first
        todo_data = {"title": "Todo to delete"}
        create_response = client.post("/api/todos", json=todo_data)
        todo_id = create_response.json()["id"]
        
        # Delete the todo
        response = client.delete(f"/api/todos/{todo_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/todos/{todo_id}")
        assert get_response.status_code == 404
    
    def test_bulk_operations(self):
        """Test bulk operations on todos."""
        # Create multiple todos
        for i in range(3):
            client.post("/api/todos", json={"title": f"Todo {i}"})
        
        # Mark all complete
        response = client.post("/api/todos/bulk/mark-complete")
        assert response.status_code == 200
        data = response.json()
        assert data["affected_count"] == 3
        
        # Delete completed todos
        response = client.delete("/api/todos/bulk/completed")
        assert response.status_code == 200
        data = response.json()
        assert data["affected_count"] == 3
        
        # Verify all are deleted
        response = client.get("/api/todos")
        assert response.json() == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])