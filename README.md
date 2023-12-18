### Introduction

### Learning Platform Backend Application

This repository houses the backend application for a comprehensive learning platform designed to facilitate the exchange of teaching materials among educators and students. The system also tracks learning progress to enhance the educational experience.

### Technical Overview

The backend is developed using FastAPI, a Python framework, to create a robust and RESTful API. The API manages courses, lessons, and user profiles, enabling seamless interaction and data management.

### Key Components

- **API Development:** Utilizes FastAPI to build endpoints for course management, lesson creation, and user profile handling.
  
- **Database Schema:** Employs a PostgreSQL database schema to organize and store data related to courses, lessons, and user profiles.

- **Containerization with Docker:** Utilizes Docker containers managed via Docker Compose to encapsulate and run the API and PostgreSQL database efficiently.

- **Testing Framework:** Implements test cases using pytest to ensure the reliability and functionality of the application.

- **Monitoring and Logging:** Integrates loguru for robust logging, providing essential insights into application operations.

### Additional Features

- **Rate Limiting:** Implements request limitations to ensure controlled access and efficient resource utilization.

- **Caching Mechanisms:** Develops caching functionalities for improved performance in data retrieval and access.

### Submission and Documentation

The codebase is available in this GitHub repository, showcasing a well-structured and documented backend application. The repository encompasses comprehensive documentation and clean formatting.

### Installation
- Clone the repository.
- Navigate to the project directory.

### Running the Application
1. Create a file named `.env` in the root directory and populate it as described in `.env.example`.
2. Start the application using Docker Compose:
   ```
   docker-compose up --build
   ```

> Note: If Docker Compose is not installed, run `sudo apt install docker-compose` to install it.

### Testing
To run tests, follow these steps:

1. Access the container's shell using:
   ```
   docker exec -it <container_name> bash
   ```
2. Execute the test suite using Pytest:
   ```
   pytest
   ```

### Monitoring
To see logging message, follow these steps

1. Access the container's shell using:
   ```
   docker exec -it <container_name> bash
   ```
2. Go to the monitoring directory:
   ```
   cd monitoring
   ```
3. Open the log file:
   ```
   cat app.log
   ```

### Using API Endpoints
Below are examples of `curl` commands to interact with the API endpoints:

#### Create Course
```bash
curl -X POST -H "Content-Type: application/json" -d '{data}' http://0.0.0.0:8000/courses/
```

#### Get Courses
```bash
curl http://0.0.0.0:8000/courses/
```

> Repeat the above format for each API endpoint, customizing the `curl` commands based on the respective HTTP methods and endpoints.

### Database Design
This backend system is structured around five key models that encapsulate the core entities within the learning platform:

- **Course Model:** Represents a course offering within the platform. It holds essential attributes such as `id`, `name`, and `teacher_id`. This model maintains relationships with `Teacher`, `Lesson`, and `Enrollment`.

- **Teacher Model:** Represents the educators associated with courses. It encompasses attributes like `id` and `name` and maintains a relationship with the `Course` model.

- **Lesson Model:** Represents individual lessons or units within a course. It contains attributes such as `id`, `title`, and `course_id`, establishing a relationship with the `Course` model.

- **Student Model:** Represents the learners using the platform. It includes attributes like `id` and `username` and is associated with the `Enrollment` model.

- **Enrollment Model:** Acts as an intermediary to map students to courses. It contains attributes such as `id`, `student_id`, and `course_id` and establishes relationships with both `Student` and `Course` models.

- **Course**
  - Attributes: `id`, `name`, `teacher_id`
  - Relationships: `Teacher`, `Lesson`, `Enrollment`

- **Teacher**
  - Attributes: `id`, `name`
  - Relationships: `Course`

- **Lesson**
  - Attributes: `id`, `title`, `course_id`
  - Relationships: `Course`

- **Student**
  - Attributes: `id`, `username`
  - Relationships: `Enrollment`

- **Enrollment**
  - Attributes: `id`, `student_id`, `course_id`
  - Relationships: `Student`, `Course`
