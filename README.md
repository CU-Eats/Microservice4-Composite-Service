# Microservice4-Composite-Service
The Composite Microservice orchestrates the communication between the User, Product, and Order microservices. It provides a single point of access for clients, handling API requests, aggregating data, and rendering the frontend interface. This microservice enhances scalability and maintainability by decoupling the frontend from individual backend services.

## Feature
- Unified API Gateway
- Frontend Interface
- User Authentication and Authorization
- Product Browsing and Search
- Order Placement and Tracking
- Microservices Communication Management

## Architecture
The Composite Microservice follows a modular architecture, where each component interacts with the others through well-defined interfaces. Here's a high-level overview:
- Frontend (React): A web interface built with React for an interactive user experience.
- Backend Gateway (Django): A Django application that handles API requests, communicates with underlying microservices, and aggregates data.
- Microservices Communication: Utilizes RESTful APIs to interact with the User, Product, and Order microservices.
