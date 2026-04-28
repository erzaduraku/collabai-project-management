# CollabAI Backend Architecture

## 1. Project Structure

The backend follows a modular Django structure:

- models → database models
- serializers → data validation and transformation
- views → API endpoints
- services → business logic
- permissions → access control
- mixins → reusable logic
- utils → helper functions

---

## 2. OOP Principles

The project follows Object-Oriented Programming principles:

- Inheritance → BaseModel is used by all models
- Abstraction → BaseAPIView provides a base for all API views
- Encapsulation → business logic is placed in services
- Polymorphism → methods can be overridden in subclasses

---

## 3. DRF Guidelines

- Serializers handle validation only
- Views handle request/response logic
- Services handle business logic
- APIs follow REST conventions

---

## 4. Naming Conventions

- Models → PascalCase (User, Project, Task)
- Serializers → ModelNameSerializer
- Views → ModelNameAPIView
- Endpoints → /api/resource/

---

## 5. Permissions & Authentication

- Role-based access control (RBAC)
- Custom permissions (e.g., IsOwner)
- JWT authentication (planned)

---

## 6. Middleware Strategy

- Logging middleware for tracking requests
- Authentication middleware for user validation

---

## 7. Architecture Overview

Frontend (React)
↓
API Layer (DRF Views)
↓
Service Layer (Business Logic)
↓
Database Layer (Models)

---

## 8. Reusability

- BaseModel for shared fields
- BaseAPIView for common API behavior
- Mixins for reusable components