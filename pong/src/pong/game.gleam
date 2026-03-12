import gleam/float
import pong/input

pub type GameState {
  Playing
  Paused
  GameOver
}

pub type Game {
  Game(
    state: GameState,
    player_score: Int,
    ai_score: Int,
    ball: Ball,
    player_paddle: Paddle,
    ai_paddle: Paddle,
  )
}

pub type Ball {
  Ball(x: Float, y: Float, vx: Float, vy: Float, radius: Float)
}

pub type Paddle {
  Paddle(x: Float, y: Float, width: Float, height: Float, speed: Float)
}

pub fn init_game() -> Game {
  Game(
    state: Playing,
    player_score: 0,
    ai_score: 0,
    ball: Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0),
    player_paddle: Paddle(
      x: 30.0,
      y: 150.0,
      width: 15.0,
      height: 100.0,
      speed: 8.0,
    ),
    ai_paddle: Paddle(
      x: 755.0,
      y: 150.0,
      width: 15.0,
      height: 100.0,
      speed: 6.0,
    ),
  )
}

pub fn update_game(
  game: Game,
  input_state: input.InputState,
  canvas_width: Float,
  canvas_height: Float,
) -> Game {
  case game.state {
    Playing -> {
      // Move paddles based on input
      let player_direction = input.get_player_direction(input_state)
      let updated_player_paddle =
        move_player_paddle(game.player_paddle, player_direction, canvas_height)
      let updated_ai_paddle =
        update_ai_paddle(game.ai_paddle, game.ball, canvas_height)

      // Update ball position
      let updated_ball = update_ball_position(game.ball)

      // Check wall collisions
      let ball_after_wall_collision =
        check_wall_collision(updated_ball, canvas_height)

      // Check paddle collisions
      let ball_after_paddle_collision = case
        check_paddle_collision(ball_after_wall_collision, updated_player_paddle)
      {
        True -> handle_paddle_collision(ball_after_wall_collision)
        False ->
          case
            check_paddle_collision(ball_after_wall_collision, updated_ai_paddle)
          {
            True -> handle_paddle_collision(ball_after_wall_collision)
            False -> ball_after_wall_collision
          }
      }

      // Check for scoring
      let #(scored, scorer) =
        check_scoring(ball_after_paddle_collision, canvas_width)
      case scored {
        True -> {
          let new_game = case scorer {
            "player" ->
              Game(
                ..game,
                player_score: game.player_score + 1,
                ball: reset_ball(),
              )
            "ai" ->
              Game(..game, ai_score: game.ai_score + 1, ball: reset_ball())
            _ -> game
          }
          let final_game =
            Game(
              ..new_game,
              player_paddle: updated_player_paddle,
              ai_paddle: updated_ai_paddle,
            )
          check_game_over(final_game)
        }
        False -> {
          Game(
            ..game,
            ball: ball_after_paddle_collision,
            player_paddle: updated_player_paddle,
            ai_paddle: updated_ai_paddle,
          )
        }
      }
    }
    _ -> game
  }
}

// Ball functions moved here to break circular dependency
pub fn update_ball_position(ball: Ball) -> Ball {
  Ball(..ball, x: ball.x +. ball.vx, y: ball.y +. ball.vy)
}

pub fn check_wall_collision(ball: Ball, canvas_height: Float) -> Ball {
  let top_wall = ball.radius
  let bottom_wall = canvas_height -. ball.radius

  case ball.y <=. top_wall {
    True -> Ball(..ball, vy: float.absolute_value(ball.vy))
    False ->
      case ball.y >=. bottom_wall {
        True -> Ball(..ball, vy: float.negate(float.absolute_value(ball.vy)))
        False -> ball
      }
  }
}

pub fn move_paddle(paddle: Paddle, direction: Float) -> Paddle {
  Paddle(..paddle, y: paddle.y +. paddle.speed *. direction)
}

fn check_paddle_collision(ball: Ball, paddle: Paddle) -> Bool {
  let ball_left = ball.x -. ball.radius
  let ball_right = ball.x +. ball.radius
  let ball_top = ball.y -. ball.radius
  let ball_bottom = ball.y +. ball.radius

  let paddle_left = paddle.x
  let paddle_right = paddle.x +. paddle.width
  let paddle_top = paddle.y
  let paddle_bottom = paddle.y +. paddle.height

  ball_right >=. paddle_left
  && ball_left <=. paddle_right
  && ball_bottom >=. paddle_top
  && ball_top <=. paddle_bottom
}

fn handle_paddle_collision(ball: Ball) -> Ball {
  Ball(..ball, vx: float.negate(ball.vx))
}

fn check_scoring(ball: Ball, canvas_width: Float) -> #(Bool, String) {
  case ball.x <=. 0.0 {
    True -> #(True, "ai")
    False ->
      case ball.x >=. canvas_width {
        True -> #(True, "player")
        False -> #(False, "")
      }
  }
}

fn reset_ball() -> Ball {
  // For now, always serve to the right (in real implementation would be random)
  Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
}

// Paddle functions moved here to break circular dependency
fn move_player_paddle(
  paddle: Paddle,
  direction: Float,
  canvas_height: Float,
) -> Paddle {
  let new_y = paddle.y +. paddle.speed *. direction
  let max_y = canvas_height -. paddle.height

  let clamped_y = case new_y <=. 0.0 {
    True -> 0.0
    False ->
      case new_y >=. max_y {
        True -> max_y
        False -> new_y
      }
  }

  Paddle(..paddle, y: clamped_y)
}

fn update_ai_paddle(paddle: Paddle, ball: Ball, canvas_height: Float) -> Paddle {
  let paddle_center = paddle.y +. paddle.height /. 2.0
  let ball_y = ball.y
  let diff = ball_y -. paddle_center

  // Only move if ball is moving toward AI and difference is significant
  let should_move = ball.vx >. 0.0 && float.absolute_value(diff) >. 5.0

  case should_move {
    True -> {
      let direction = case diff >. 0.0 {
        True -> 1.0
        // Move down
        False -> -1.0
        // Move up
      }
      move_player_paddle(paddle, direction, canvas_height)
    }
    False -> paddle
  }
}

pub fn check_game_over(game: Game) -> Game {
  case game.player_score >= 5 || game.ai_score >= 5 {
    True -> Game(..game, state: GameOver)
    False -> game
  }
}

pub fn restart_game() -> Game {
  init_game()
}
