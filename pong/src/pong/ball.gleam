import gleam/float
import gleam/int
import pong/game

pub fn update_ball(ball: game.Ball) -> game.Ball {
  game.Ball(..ball, x: ball.x +. ball.vx, y: ball.y +. ball.vy)
}

pub fn check_paddle_collision(ball: game.Ball, paddle: game.Paddle) -> Bool {
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

pub fn handle_paddle_collision(ball: game.Ball) -> game.Ball {
  game.Ball(..ball, vx: float.negate(ball.vx))
}

pub fn check_scoring(ball: game.Ball, canvas_width: Float) -> #(Bool, String) {
  case ball.x <=. 0.0 {
    True -> #(True, "ai")
    False ->
      case ball.x >=. canvas_width {
        True -> #(True, "player")
        False -> #(False, "")
      }
  }
}

pub fn reset_ball() -> game.Ball {
  // Randomize ball direction: 50% chance to serve left or right
  let random_int = int.random(2)
  // Returns 0 or 1
  let ball_vx = case random_int {
    0 -> -5.0
    // Serve to the left
    _ -> 5.0
    // Serve to the right
  }

  game.Ball(x: 400.0, y: 200.0, vx: ball_vx, vy: 3.0, radius: 8.0)
}
