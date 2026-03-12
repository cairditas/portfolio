import gleam/float
import pong/game

pub fn move_player_paddle(
  paddle: game.Paddle,
  direction: Float,
  canvas_height: Float,
) -> game.Paddle {
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

  game.Paddle(..paddle, y: clamped_y)
}

pub fn update_ai_paddle(
  paddle: game.Paddle,
  ball: game.Ball,
  canvas_height: Float,
) -> game.Paddle {
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
