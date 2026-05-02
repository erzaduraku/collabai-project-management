#  Database Models – CollabAI

## Overview

This document describes the foundational database models implemented for the CollabAI backend.

The models follow:

* Object-Oriented Programming (OOP)
* Django ORM best practices
* Multi-tenancy architecture
* Role-Based Access Control (RBAC)

---

## Core Models

### BaseModel (Abstract)

All models inherit from `BaseModel`, which provides:

* `created_at`
* `updated_at`

---

### Organization

Represents a company (tenant).

* One Organization → Many Workspaces

---

### Workspace

Represents a working environment inside an organization.

* Belongs to Organization
* Has multiple Roles
* Used for multi-tenancy

---

### Role

Defines user roles inside a workspace.

* Belongs to Workspace
* Has many Permissions (Many-to-Many)

---

### Permission

Defines allowed actions.

Examples:

* `create_task`
* `update_project`
* `delete_user`

---

### Profile

Extends the default Django User.

* One-to-one with User
* Can belong to Workspace
* Can have a Role

---

## 🔗 Model Relationships

Organization
└── Workspace
  ├── Role
  │  └── Permissions (M2M)
  └── Profile
    └── User (1-1)

---

##  Design Decisions

### OOP

* Shared fields handled via `BaseModel`

### Multi-Tenancy

* Implemented via Organization → Workspace hierarchy

### RBAC

* Implemented via Role + Permission

---

##  Testing

* Model creation tested
* Relationships verified
* All tests pass successfully

---

##  Migration Status

* Initial migrations created
* Applied successfully
* No system errors detected
