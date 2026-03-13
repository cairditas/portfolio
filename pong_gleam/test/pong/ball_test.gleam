import gleam/float
import gleeunit/should
import pong/ball
import pong/game

// Tests for ball physics and movement logic
// Covers ball position updates, wall collisions, and paddle interactions

pub fn update_ball_test() {
  let ball = game.Ball(x: 100.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let updated_ball = ball.update_ball(ball)

  updated_ball.x |> should.equal(105.0)
  updated_ball.y |> should.equal(203.0)
  updated_ball.vx |> should.equal(5.0)
  updated_ball.vy |> should.equal(3.0)
  updated_ball.radius |> should.equal(8.0)
}

pub fn check_paddle_collision_player_test() {
  let ball = game.Ball(x: 45.0, y: 180.0, vx: -5.0, vy: 3.0, radius: 8.0)
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let result = ball.check_paddle_collision(ball, paddle)

  result |> should.equal(True)
}

pub fn check_paddle_collision_ai_test() {
  let ball = game.Ball(x: 747.0, y: 180.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let paddle =
    game.Paddle(x: 755.0, y: 150.0, width: 15.0, height: 100.0, speed: 6.0)
  let result = ball.check_paddle_collision(ball, paddle)

  result |> should.equal(True)
}

pub fn check_paddle_collision_no_collision_test() {
  let ball = game.Ball(x: 100.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let result = ball.check_paddle_collision(ball, paddle)

  result |> should.equal(False)
}

pub fn handle_paddle_collision_test() {
  let ball = game.Ball(x: 45.0, y: 180.0, vx: -5.0, vy: 3.0, radius: 8.0)
  let updated_ball = ball.handle_paddle_collision(ball)

  // Ball should reverse x direction after paddle collision
  updated_ball.vx |> should.equal(5.0)
  updated_ball.vy |> should.equal(3.0)
  updated_ball.x |> should.equal(45.0)
  updated_ball.y |> should.equal(180.0)
  updated_ball.radius |> should.equal(8.0)
}

pub fn check_scoring_player_scores_test() {
  let ball = game.Ball(x: 800.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let result = ball.check_scoring(ball, 800.0)

  result |> should.equal(#(True, "player"))
}

pub fn check_scoring_ai_scores_test() {
  let ball = game.Ball(x: 0.0, y: 200.0, vx: -5.0, vy: 3.0, radius: 8.0)
  let result = ball.check_scoring(ball, 800.0)

  result |> should.equal(#(True, "ai"))
}

pub fn check_scoring_no_score_test() {
  let ball = game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let result = ball.check_scoring(ball, 800.0)

  result |> should.equal(#(False, ""))
}

pub fn reset_ball_test() {
  let reset_ball = ball.reset_ball()

  reset_ball.x |> should.equal(400.0)
  reset_ball.y |> should.equal(200.0)
  // Direction should be randomized, but we check it's either 5 or -5
  float.absolute_value(reset_ball.vx) |> should.equal(5.0)
  reset_ball.radius |> should.equal(8.0)
}

// Edge case tests for ball physics
pub fn update_ball_zero_velocity_test() {
  let ball = game.Ball(x: 100.0, y: 200.0, vx: 0.0, vy: 0.0, radius: 8.0)
  let updated_ball = ball.update_ball(ball)

  // Ball should not move when velocity is zero
  updated_ball.x |> should.equal(100.0)
  updated_ball.y |> should.equal(200.0)
  updated_ball.vx |> should.equal(0.0)
  updated_ball.vy |> should.equal(0.0)
}

pub fn update_ball_extreme_velocity_test() {
  let ball =
    game.Ball(x: 100.0, y: 200.0, vx: 999_999.0, vy: -999_999.0, radius: 8.0)
  let updated_ball = ball.update_ball(ball)

  // Ball should handle extreme velocities
  updated_ball.x |> should.equal(1_000_099.0)
  updated_ball.y |> should.equal(200.0 -. 999_999.0)
  updated_ball.vx |> should.equal(999_999.0)
  updated_ball.vy |> should.equal(-999_999.0)
}

pub fn check_paddle_collision_exact_edge_test() {
  // Ball exactly touching paddle edge
  let ball = game.Ball(x: 45.0, y: 150.0, vx: -5.0, vy: 0.0, radius: 8.0)
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let result = ball.check_paddle_collision(ball, paddle)

  result |> should.equal(True)
}

pub fn check_paddle_collision_inside_paddle_test() {
  // Ball center inside paddle (invalid but should handle gracefully)
  let ball = game.Ball(x: 35.0, y: 180.0, vx: -5.0, vy: 0.0, radius: 2.0)
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)
  let result = ball.check_paddle_collision(ball, paddle)

  result |> should.equal(True)
}

pub fn check_scoring_exact_boundary_test() {
  // Ball exactly at right boundary
  let ball = game.Ball(x: 800.0, y: 200.0, vx: 5.0, vy: 0.0, radius: 0.0)
  let result = ball.check_scoring(ball, 800.0)

  result |> should.equal(#(True, "player"))
}

pub fn check_scoring_exact_left_boundary_test() {
  // Ball exactly at left boundary
  let ball = game.Ball(x: 0.0, y: 200.0, vx: -5.0, vy: 0.0, radius: 0.0)
  let result = ball.check_scoring(ball, 800.0)

  result |> should.equal(#(True, "ai"))
}

pub fn reset_ball_preserves_radius_test() {
  let reset_ball = ball.reset_ball()

  // Reset function uses fixed radius of 8.0 (current implementation)
  reset_ball.radius |> should.equal(8.0)
}
