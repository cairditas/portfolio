# Pong

A classic Pong game implemented in Gleam that compiles to JavaScript and runs in the browser. This implementation features player vs AI gameplay with smooth animations and responsive controls.

## Game Description

Pong is a two-dimensional sports game that simulates table tennis. The player controls a paddle on the left side of the screen and competes against an AI-controlled paddle on the right. The objective is to hit a ball back and forth, scoring points when the opponent fails to return the ball.

### Features
- **Player vs AI**: Compete against an intelligent AI opponent
- **Smooth Gameplay**: 60 FPS rendering with fluid animations
- **Responsive Controls**: Real-time paddle movement using keyboard input
- **Score Tracking**: Automatic score keeping for both player and AI
- **Modern Web Technology**: Built with Gleam and compiled to JavaScript

### Controls
- **Up Arrow**: Move paddle up
- **Down Arrow**: Move paddle down
- **Space**: Pause/resume game (if implemented)

## Running Locally

### Prerequisites
- Gleam compiler (install from https://gleam.run/)
- Node.js (for JavaScript compilation and testing)
- npm (for JavaScript dependencies)

### Setup and Run

1. **Clone and navigate to the project**:
   ```sh
   cd pong
   ```

2. **Install dependencies**:
   ```sh
   # Install Gleam dependencies
   gleam deps download
   
   # Install Node.js dependencies
   npm install
   ```

3. **Build the project**:
   ```node
   npm run build
   ```

4. **Open in browser**:
   Open `index.html` in your web browser to play the game.

   Alternatively, you can serve the files locally:
   ```sh
   # Using Python (if available)
   python -m http.server 8000
   
   # Using Node.js serve (if available)
   npx serve .
   
   # Then open http://localhost:8000 in your browser
   ```

### Development Mode

For development with hot reloading:
```sh
gleam run   # Run the project
```

## Test Coverage and Quality Analysis

This project includes comprehensive test coverage and SonarQube integration for code quality analysis.

### Coverage Requirements
- **Lines**: ≥90%
- **Functions**: ≥90%
- **Branches**: ≥80%
- **Statements**: ≥90%

### Running Tests Locally

#### Gleam Tests
```sh
gleam test
```

#### Gleam Tests with JavaScript Coverage
```sh
# Run Gleam tests (JavaScript target)
npm test

# Run tests with coverage report
npm run test:coverage

# Build for JavaScript
npm run build
```

#### Coverage Reports
Coverage reports are generated in multiple formats:
- **Console**: Text summary in terminal
- **HTML**: Detailed interactive report at `coverage/lcov-report/index.html`
- **LCOV**: For CI/CD integration at `coverage/lcov.info`
- **SonarQube**: For SonarQube analysis

### Test Structure

#### Gleam Tests (74 tests)
- `test/pong/ball_test.gleam` - Ball physics and collision detection
- `test/pong/paddle_test.gleam` - Paddle movement and mechanics
- `test/pong/game_test.gleam` - Game logic and state management
- `test/pong/input_test.gleam` - Input handling and keyboard events
- `test/pong/render_test.gleam` - Canvas rendering functions
- `test/pong/game_integration_test.gleam` - End-to-end gameplay scenarios

#### Generated JavaScript Tests
Gleam automatically compiles tests to JavaScript in `build/dev/javascript/pong/`:
- `pong_test.mjs` - Main test runner
- `ball_test.mjs` - Ball physics tests
- `paddle_test.mjs` - Paddle mechanics tests
- `game_test.mjs` - Game logic tests
- `input_test.mjs` - Input handling tests
- `render_test.mjs` - Rendering tests
- `game_integration_test.mjs` - Integration tests

### SonarQube Integration

#### CI/CD Pipeline
The project includes automated SonarQube analysis via GitHub Actions:

- **Trigger**: Push to main/master branches and pull requests
- **Analysis**: JavaScript coverage and code quality metrics
- **Quality Gates**: Enforces coverage thresholds
- **PR Comments**: Automatic coverage summary on pull requests

#### Required Secrets
To enable SonarQube analysis, configure these repository secrets:
- `SONAR_TOKEN`: SonarQube authentication token
- `SONAR_HOST_URL`: SonarQube server URL (optional for SonarCloud)
- `SONAR_ORGANIZATION`: SonarQube organization (optional for SonarCloud)

#### Local SonarQube Analysis
```sh
# Run local SonarQube analysis
npm run sonar:local
```

### Coverage Configuration

#### Gleam JavaScript Coverage
Coverage is collected from Gleam-generated JavaScript files:
- Collects coverage from `build/dev/javascript/**/*.mjs`
- Excludes build artifacts and dependencies
- Generates multiple report formats via c8

#### c8 Configuration
Coverage thresholds are enforced by c8:
- Lines: 90%
- Branches: 80%
- Functions: 90%
- Statements: 90%

#### SonarQube Configuration
Project analysis is configured in `sonar-project.properties`:
- Maps coverage reports to source files
- Excludes generated code and dependencies
- Sets quality gate thresholds

## Running Tests

The project includes comprehensive unit tests for all game components:

### Run All Tests
```sh
gleam test
```

### Test Coverage
Tests are organized by component:
- **Ball physics**: Movement, collision detection, and boundary checks
- **Paddle mechanics**: Movement, positioning, and collision logic
- **Game state**: Score tracking, game over conditions, and state transitions
- **Input handling**: Keyboard input processing and paddle control
- **Rendering**: Canvas drawing and visual updates
- **Integration tests**: End-to-end gameplay scenarios

### Individual Test Files
- `test/pong/ball_test.gleam` - Ball movement and collision tests
- `test/pong/paddle_test.gleam` - Paddle behavior tests
- `test/pong/game_test.gleam` - Game logic and state management
- `test/pong/input_test.gleam` - Input handling tests
- `test/pong/render_test.gleam` - Rendering function tests
- `test/pong/game_integration_test.gleam` - Full gameplay integration tests

## Project Structure

```
pong/
├── src/pong/           # Source code
│   ├── pong.gleam      # Main entry point
│   ├── game.gleam      # Game logic and state
│   ├── ball.gleam      # Ball physics
│   ├── paddle.gleam    # Paddle mechanics
│   ├── input.gleam     # Input handling
│   └── render.gleam    # Canvas rendering
├── test/pong/          # Test files
├── dist/               # Compiled JavaScript
├── index.html          # Game HTML page
├── canvas_ffi.mjs      # Canvas JavaScript bindings
└── gleam.toml          # Project configuration
```

## Technology Stack

- **Gleam**: Type-safe functional programming language
- **JavaScript**: Compilation target for web deployment
- **HTML5 Canvas**: Game rendering and graphics
- **Gleeunit**: Testing framework for Gleam
- **c8**: JavaScript coverage tool
- **SonarQube**: Code quality analysis platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run all tests to ensure quality:
   ```sh
   gleam test          # Run Gleam tests
   npm run test:coverage  # Run JavaScript tests with coverage
   ```
6. Ensure coverage thresholds are met (≥90% lines, ≥80% branches)
7. Submit a pull request

### Quality Standards
- All new code must have test coverage
- Coverage thresholds must be maintained
- Code must pass SonarQube quality gates
- Follow existing code style and patterns
