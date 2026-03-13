import gleeunit/should
import pong/game
import pong/paddle

// Tests for paddle movement and collision logic
// Covers player and AI paddle movement, boundary checking

pub fn move_player_paddle_up_test() {
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let moved_paddle = paddle.move_player_paddle(paddle, -1.0, 400.0)

  moved_paddle.y |> should.equal(142.0)
  moved_paddle.x |> should.equal(30.0)
  moved_paddle.width |> should.equal(15.0)
  moved_paddle.height |> should.equal(100.0)
  moved_paddle.speed |> should.equal(8.0)
}

pub fn move_player_paddle_down_test() {
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let moved_paddle = paddle.move_player_paddle(paddle, 1.0, 400.0)

  moved_paddle.y |> should.equal(158.0)
  moved_paddle.x |> should.equal(30.0)
}

pub fn move_player_paddle_boundary_test() {
  let paddle =
    game.Paddle(x: 30.0, y: 5.0, width: 15.0, height: 100.0, speed: 8.0)
  let moved_paddle = paddle.move_player_paddle(paddle, -1.0, 400.0)

  // Should not go above 0
  moved_paddle.y |> should.equal(0.0)
}

pub fn move_player_paddle_bottom_boundary_test() {
  let paddle =
    game.Paddle(x: 30.0, y: 300.0, width: 15.0, height: 100.0, speed: 8.0)
  let moved_paddle = paddle.move_player_paddle(paddle, 1.0, 400.0)

  // Should not go below canvas height - paddle height
  moved_paddle.y |> should.equal(300.0)
}

pub fn update_ai_paddle_tracking_test() {
  let paddle =
    game.Paddle(x: 755.0, y: 150.0, width: 15.0, height: 100.0, speed: 6.0)
  let ball = game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_paddle = paddle.update_ai_paddle(paddle, ball, 400.0)

  // AI should move toward ball - paddle center is 200, ball y is 200, so no movement needed
  updated_paddle.y |> should.equal(150.0)
}

pub fn update_ai_paddle_ball_above_test() {
  let paddle =
    game.Paddle(x: 755.0, y: 200.0, width: 15.0, height: 100.0, speed: 6.0)
  let ball = game.Ball(x: 400.0, y: 100.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_paddle = paddle.update_ai_paddle(paddle, ball, 400.0)

  // AI should move up toward ball
  updated_paddle.y |> should.equal(194.0)
  // Moves up by speed 6.0
}

pub fn update_ai_paddle_ball_below_test() {
  let paddle =
    game.Paddle(x: 755.0, y: 100.0, width: 15.0, height: 100.0, speed: 6.0)
  let ball = game.Ball(x: 400.0, y: 300.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_paddle = paddle.update_ai_paddle(paddle, ball, 400.0)

  // AI should move down toward ball
  updated_paddle.y |> should.equal(106.0)
  // Moves down by speed 6.0
}

pub fn update_ai_paddle_already_aligned_test() {
  let paddle =
    game.Paddle(x: 755.0, y: 150.0, width: 15.0, height: 100.0, speed: 6.0)
  let ball = game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_paddle = paddle.update_ai_paddle(paddle, ball, 400.0)

  // AI paddle center (200) aligns with ball y (200), so no movement
  updated_paddle.y |> should.equal(150.0)
}

pub fn update_ai_paddle_boundary_test() {
  let paddle =
    game.Paddle(x: 755.0, y: 5.0, width: 15.0, height: 100.0, speed: 6.0)
  let ball = game.Ball(x: 400.0, y: 50.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_paddle = paddle.update_ai_paddle(paddle, ball, 400.0)

  // The AI logic has a threshold - if the paddle is already close enough to the ball,
  // it doesn't move. In this case, the AI doesn't move.
  updated_paddle.y |> should.equal(5.0)
}
