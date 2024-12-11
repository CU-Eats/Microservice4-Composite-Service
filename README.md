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
The GraphQL API is implemented in the `Composite_service` folder, specifically in the `schema.py` file. It offers a flexible and efficient way to query data from the underlying microservices. The GraphQL schema is designed using **Graphene-Django** and is fully extensible for future needs. The `/graphql/` endpoint supports the key feature of querying a restaurant by its name and display its menu.

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
## Architecture
The Composite Microservice follows a modular architecture, where each component interacts with the others through well-defined interfaces. Here's a high-level overview:
- Frontend (React): A web interface built with React for an interactive user experience.
- Backend Gateway (Django): A Django application that handles API requests, communicates with underlying microservices, and aggregates data.
- Microservices Communication: Utilizes RESTful APIs to interact with the User, Product, and Order microservices.


