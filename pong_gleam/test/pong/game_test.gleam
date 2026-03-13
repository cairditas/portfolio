import gleeunit/should
import pong/game

// Tests for game state management and core game logic
// Covers game initialization, state transitions, and score management

pub fn game_initialization_test() {
  let game = game.init_game()

  // Test initial state
  game.state |> should.equal(game.Playing)

  // Test initial scores
  game.player_score |> should.equal(0)
  game.ai_score |> should.equal(0)

  // Test initial ball position
  game.ball.x |> should.equal(400.0)
  game.ball.y |> should.equal(200.0)
  game.ball.vx |> should.equal(5.0)
  game.ball.vy |> should.equal(3.0)
  game.ball.radius |> should.equal(8.0)

  // Test initial paddle positions
  game.player_paddle.x |> should.equal(30.0)
  game.player_paddle.y |> should.equal(150.0)
  game.player_paddle.width |> should.equal(15.0)
  game.player_paddle.height |> should.equal(100.0)
  game.player_paddle.speed |> should.equal(8.0)

  game.ai_paddle.x |> should.equal(755.0)
  game.ai_paddle.y |> should.equal(150.0)
  game.ai_paddle.width |> should.equal(15.0)
  game.ai_paddle.height |> should.equal(100.0)
  game.ai_paddle.speed |> should.equal(6.0)
}

pub fn game_state_types_test() {
  // Test that we can create different game states
  let playing_state = game.Playing
  let paused_state = game.Paused
  let game_over_state = game.GameOver

  // These should be different values
  playing_state |> should.not_equal(paused_state)
  paused_state |> should.not_equal(game_over_state)
  game_over_state |> should.not_equal(playing_state)
}

pub fn restart_game_test() {
  // Create a game with different state
  let original_game = game.init_game()
  let _modified_game =
    game.Game(
      ..original_game,
      player_score: 3,
      ai_score: 4,
      state: game.GameOver,
    )

  // Restart should reset to initial state
  let restarted_game = game.restart_game()

  restarted_game.state |> should.equal(game.Playing)
  restarted_game.player_score |> should.equal(0)
  restarted_game.ai_score |> should.equal(0)
  restarted_game.ball.x |> should.equal(400.0)
  restarted_game.ball.y |> should.equal(200.0)
}

pub fn update_ball_position_test() {
  let ball = game.Ball(x: 100.0, y: 200.0, vx: 5.0, vy: -3.0, radius: 8.0)
  let updated_ball = game.update_ball_position(ball)

  // Ball should move by its velocity
  updated_ball.x |> should.equal(105.0)
  // 100.0 + 5.0
  updated_ball.y |> should.equal(197.0)
  // 200.0 + (-3.0)
  updated_ball.vx |> should.equal(5.0)
  // Velocity unchanged
  updated_ball.vy |> should.equal(-3.0)
  // Velocity unchanged
  updated_ball.radius |> should.equal(8.0)
  // Radius unchanged
}

pub fn check_wall_collision_top_test() {
  // Ball hitting top wall
  let ball = game.Ball(x: 400.0, y: 8.0, vx: 5.0, vy: -3.0, radius: 8.0)
  let canvas_height = 400.0

  let bounced_ball = game.check_wall_collision(ball, canvas_height)

  // Y velocity should be positive (bouncing down)
  bounced_ball.vy |> should.equal(3.0)
  // Absolute value of -3.0
  bounced_ball.x |> should.equal(400.0)
  // X unchanged
  bounced_ball.y |> should.equal(8.0)
  // Y unchanged
}

pub fn check_wall_collision_bottom_test() {
  // Ball hitting bottom wall
  let ball = game.Ball(x: 400.0, y: 392.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let canvas_height = 400.0

  let bounced_ball = game.check_wall_collision(ball, canvas_height)

  // Y velocity should be negative (bouncing up)
  bounced_ball.vy |> should.equal(-3.0)
  // Negative absolute value
  bounced_ball.x |> should.equal(400.0)
  // X unchanged
  bounced_ball.y |> should.equal(392.0)
  // Y unchanged
}

pub fn check_wall_collision_no_collision_test() {
  // Ball in middle of canvas
  let ball = game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 3.0, radius: 8.0)
  let canvas_height = 400.0

  let unchanged_ball = game.check_wall_collision(ball, canvas_height)

  // No change when not hitting walls
  unchanged_ball.vx |> should.equal(5.0)
  unchanged_ball.vy |> should.equal(3.0)
  unchanged_ball.x |> should.equal(400.0)
  unchanged_ball.y |> should.equal(200.0)
}

pub fn move_paddle_test() {
  let paddle =
    game.Paddle(x: 30.0, y: 150.0, width: 15.0, height: 100.0, speed: 8.0)

  // Move up
  let moved_up = game.move_paddle(paddle, -1.0)
  moved_up.y |> should.equal(142.0)
  // 150.0 + 8.0 * (-1.0)

  // Move down
  let moved_down = game.move_paddle(paddle, 1.0)
  moved_down.y |> should.equal(158.0)
  // 150.0 + 8.0 * 1.0

  // No movement
  let no_movement = game.move_paddle(paddle, 0.0)
  no_movement.y |> should.equal(150.0)
}

pub fn check_game_over_player_wins_test() {
  let game = game.init_game()
  let game_with_player_win = game.Game(..game, player_score: 5, ai_score: 2)

  let game_over = game.check_game_over(game_with_player_win)

  game_over.state |> should.equal(game.GameOver)
  game_over.player_score |> should.equal(5)
  game_over.ai_score |> should.equal(2)
}

pub fn check_game_over_ai_wins_test() {
  let game = game.init_game()
  let game_with_ai_win = game.Game(..game, player_score: 2, ai_score: 5)

  let game_over = game.check_game_over(game_with_ai_win)

  game_over.state |> should.equal(game.GameOver)
  game_over.player_score |> should.equal(2)
  game_over.ai_score |> should.equal(5)
}

pub fn check_game_over_not_over_test() {
  let game = game.init_game()
  let ongoing_game = game.Game(..game, player_score: 3, ai_score: 2)

  let not_over = game.check_game_over(ongoing_game)

  not_over.state |> should.equal(game.Playing)
  not_over.player_score |> should.equal(3)
  not_over.ai_score |> should.equal(2)
}
