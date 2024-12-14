# Welcome to Columbia Eats
Columbia Eats is a comprehensive platform designed to enhance the dining experience on campus by connecting students and restaurants. With a user-friendly interface and efficient backend, the service allows users to easily sign up, log in, browse restaurant menus, and place batch orders for food items across multiple restaurants. For restaurant owners, Columbia Eats offers tools to manage menus and add new food items dynamically. We aim to use our service to help our campus dining enviroment for both students and restaurants

## Team Members
- Liang Yang
- Daixi Shen
- Jiacheng Liu
- Yili Yu
- Chih-Hsin Chen
- Weiheng Yang

## Microservice4-Composite-Service
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

## User Interface on Cloud
Link to our User Interface: http://18.218.176.54:80

### Default Page:
Provided option for user and restaurant
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/5a64b2c6-db3c-4870-9845-c22227248c39" />

### User Page:
Provided 3 features of sign up, log in and get menu
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/a135421b-8e91-401a-9fd8-c785c41bdb1b" />
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/b7b1a7a8-7e09-4983-805b-42f6675e6256" />
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/50d13d57-feea-4c70-a787-c74418344aa5" />
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/4db6dee4-0f27-4cd3-af85-7d32268dd2a6" />


Our UI would redirect our user to order page after successful log in:
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/2350e4fa-f7b2-4b61-b70e-1e41c6333a2a" />

## Restuarant Page
Provided option of updating menu
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/19eaeb11-0f23-4855-a2c0-94f6eae4ce50" />
<img width="1440" alt="image" src="https://github.com/user-attachments/assets/b963b0a9-4022-4748-814c-8cc3991a0441" />





## Local Access:
- GraphQL API: http://127.0.0.1:8000/graphql/
- Admin Dashboard: http://127.0.0.1:8000/admin/

## Technologies Used
- Python: Backend language.
- Django: Web framework for building the microservice.
- Graphene-Django: GraphQL integration for Django.
- Django REST Framework: RESTful API implementation.
- User Interface: HTML/CSS and Javascript

## Architecture
The Composite Microservice follows a modular architecture, where each component interacts with the others through well-defined interfaces. Here's a high-level overview:
- Frontend (React): A web interface built with HTML/CSS and Javascript for an interactive user experience.
- Backend Gateway (Django): A Django application that handles API requests, communicates with underlying microservices, and aggregates data.
- Microservices Communication: Utilizes RESTful APIs to interact with the User, Product, and Order microservices.


