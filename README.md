# Microservice4-Composite-Service
The Composite Microservice orchestrates the communication between the User, Product, and Order microservices. It provides a single point of access for clients, handling API requests, aggregating data, and rendering the frontend interface. This microservice enhances scalability and maintainability by decoupling the frontend from individual backend services.

## Feature
- Unified API Gateway
- Frontend Interface
- User Authentication and Authorization
- Product Browsing and Search
- Order Placement and Tracking
- Microservices Communication Management
- GraphQL implementation

### GraphQL Implementaion
The GraphQL API is implemented in the Composite_service/schema.py file and provides flexible querying capabilities. It allows you to query a restaurant by its name and retrieve details such as its menu.

#### Example Query
To test the GraphQL API, visit the endpoint `/graphql/` and use a query like the following:
```graphql
query {
  restaurantDetails(restaurantName: "Restaurant Name") {
    name
    menu
  }
}
```
### API Endpoints
GraphQL API
- URL: ```GET /graphql/```
- Description: Provides a GraphQL interface to query combined data from the microservices.
- Input Argument: restaurant name for querying the restaurant.

### REST Endpoints
The Composite Microservice also exposes RESTful endpoints to interact with individual microservices, such as:

#### Admin Dashboard
- URL: ```GET /admin/```
- Description: Provides access to the Django admin interface for managing database records.
#### Restaurant API
- URL: ```GET /api/restaurant/```
- Description: Integrates the Restaurant microservice for restaurant-related operations.
#### User Login
- URL: ```POST /api/user/login/```
- Description: Handles user authentication via the User microservice.
#### User Signup
- URL: ```POST /api/user/signup/```
- Description: Creates a new user account via the User microservice.
#### Orders API
- URL: ```GET /api/orders/```
- Description: Retrieves order data from the Order microservice.

## How to Run
1. Install Dependencies: Install the required libraries using the requirements.txt file:

```
pip install -r requirements.txt
```

2. Start the Server: Launch the Django server:

```
python manage.py runserver
```

## Access Endpoints:
- GraphQL API: http://127.0.0.1:8000/graphql/
- Admin Dashboard: http://127.0.0.1:8000/admin/

## Technologies Used
Python: Backend language.
Django: Web framework for building the microservice.
Graphene-Django: GraphQL integration for Django.
Django REST Framework: RESTful API implementation.

## Architecture
The Composite Microservice follows a modular architecture, where each component interacts with the others through well-defined interfaces. Here's a high-level overview:
- Frontend (React): A web interface built with React for an interactive user experience.
- Backend Gateway (Django): A Django application that handles API requests, communicates with underlying microservices, and aggregates data.
- Microservices Communication: Utilizes RESTful APIs to interact with the User, Product, and Order microservices.


