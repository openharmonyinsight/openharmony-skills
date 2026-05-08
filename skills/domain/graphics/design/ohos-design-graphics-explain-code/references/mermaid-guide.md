# Mermaid Diagram Reference

Quick reference for creating mermaid diagrams in code documentation.

## Class Diagram

Shows the structure of the code with classes, interfaces, and their relationships.

### Basic Syntax

```mermaid
classDiagram
    class ClassName {
        +publicProperty
        -privateProperty
        +publicMethod()
        -privateMethod()
    }
```

### Relationships

- `-->` : Association (uses)
- `--|>` : Inheritance (extends)
- `..|>` : Implementation (implements)
- `-->` : Composition
- `..>` : Dependency

### Example

```mermaid
classDiagram
    class UserService {
        -userRepository: UserRepository
        -emailService: EmailService
        +register(email, password)
        +login(email, password)
        +resetToken(userId)
    }
    class UserRepository {
        +findByEmail(email)
        +save(user)
    }
    class EmailService {
        +sendWelcomeEmail(user)
        +sendResetToken(email, token)
    }

    UserService --> UserRepository : uses
    UserService --> EmailService : uses
```

## Sequence Diagram

Shows the interaction between components over time.

### Basic Syntax

```mermaid
sequenceDiagram
    actor Actor
    participant Participant
    Actor->>Participant: Message
    Participant-->>Actor: Response
```

### Activation Boxes

```mermaid
sequenceDiagram
    actor User
    participant Server
    participant Database

    User->>Server: Request
    activate Server
    Server->>Database: Query
    activate Database
    Database-->>Server: Result
    deactivate Database
    Server-->>User: Response
    deactivate Server
```

### Loops and Alt Blocks

```mermaid
sequenceDiagram
    actor User
    participant API

    User->>API: Request
    loop Retry
        API->>API: Process
        alt Success
            API-->>User: Response
        else Failure
            API->>API: Log Error
        end
    end
```

### Example

```mermaid
sequenceDiagram
    actor Client
    participant API
    participant Service
    participant Database

    Client->>API: POST /api/users
    activate API
    API->>Service: createUser(data)
    activate Service
    Service->>Database: save(user)
    activate Database
    Database-->>Service: userId
    deactivate Database
    Service-->>API: userId
    deactivate Service
    API-->>Client: 201 Created {userId}
    deactivate API
```

## Flowchart

Shows logic flow and decision trees.

### Example

```mermaid
flowchart TD
    Start([Start]) --> Input{Has input?}
    Input -->|Yes| Process[Process data]
    Input -->|No| End([End])
    Process --> Error{Error?}
    Error -->|Yes| Log[Log error]
    Error -->|No| Save[Save result]
    Log --> End
    Save --> End
```

## Tips for Code Documentation

1. **Class diagrams**: Focus on the main classes and their relationships. Don't include every method - include only important ones that show the architecture.

2. **Sequence diagrams**: Show the happy path first. Use alt/loop blocks for error handling or repeated operations.

3. **Keep it readable**: Don't create overly complex diagrams with 20+ components. Break into multiple diagrams if needed.

4. **Use meaningful names**: Component names should match the actual code names (class names, service names, etc.).
