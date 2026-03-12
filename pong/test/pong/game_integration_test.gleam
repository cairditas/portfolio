import gleeunit
import gleeunit/should
import pong/game
import pong/input

pub fn main() {
  gleeunit.main()
}

pub fn update_game_playing_test() {
  let game_state = game.init_game()
  let input_state = input.init_input()
  let updated_game = game.update_game(game_state, input_state, 800.0, 400.0)

  // Game should still be playing
  updated_game.state |> should.equal(game.Playing)

  // Ball should have moved
  updated_game.ball.x |> should.equal(405.0)
  updated_game.ball.y |> should.equal(203.0)

  // Scores should be unchanged
  updated_game.player_score |> should.equal(0)
  updated_game.ai_score |> should.equal(0)
}

pub fn update_game_with_player_input_test() {
  let game_state = game.init_game()
  let input_state =
    input.InputState(
      up_pressed: True,
      down_pressed: False,
      space_pressed: False,
    )
  let updated_game = game.update_game(game_state, input_state, 800.0, 400.0)

  // Player paddle should have moved up
  updated_game.player_paddle.y |> should.equal(142.0)

  // AI paddle should not move since ball is moving away from AI (vx=5.0 means toward player)
  updated_game.ai_paddle.y |> should.equal(150.0)
}

pub fn handle_scoring_player_scores_test() {
  let game_state =
    game.Game(
      state: game.Playing,
      player_score: 0,
      ai_score: 0,
      ball: game.Ball(x: 795.0, y: 200.0, vx: 5.0, vy: 0.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let input_state = input.init_input()
  let updated_game = game.update_game(game_state, input_state, 800.0, 400.0)

  // Player should have scored
  updated_game.player_score |> should.equal(1)
  updated_game.ai_score |> should.equal(0)

  // Ball should be reset
  updated_game.ball.x |> should.equal(400.0)
  updated_game.ball.y |> should.equal(200.0)
}

pub fn handle_scoring_ai_scores_test() {
  let game_state =
    game.Game(
      state: game.Playing,
      player_score: 0,
      ai_score: 0,
      ball: game.Ball(x: 5.0, y: 200.0, vx: -5.0, vy: 0.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let input_state = input.init_input()
  let updated_game = game.update_game(game_state, input_state, 800.0, 400.0)

  // AI should have scored
  updated_game.player_score |> should.equal(0)
  updated_game.ai_score |> should.equal(1)

  // Ball should be reset
  updated_game.ball.x |> should.equal(400.0)
  updated_game.ball.y |> should.equal(200.0)
}

pub fn check_game_over_player_wins_test() {
  let game_state =
    game.Game(
      state: game.Playing,
      player_score: 5,
      ai_score: 0,
      ball: game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 0.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let updated_game = game.check_game_over(game_state)

  updated_game.state |> should.equal(game.GameOver)
}

pub fn check_game_over_ai_wins_test() {
  let game_state =
    game.Game(
      state: game.Playing,
      player_score: 0,
      ai_score: 5,
      ball: game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 0.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let updated_game = game.check_game_over(game_state)

  updated_game.state |> should.equal(game.GameOver)
}

pub fn check_game_over_not_over_test() {
  let game_state =
    game.Game(
      state: game.Playing,
      player_score: 2,
      ai_score: 3,
      ball: game.Ball(x: 400.0, y: 200.0, vx: 5.0, vy: 0.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 150.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let updated_game = game.check_game_over(game_state)

  updated_game.state |> should.equal(game.Playing)
}

pub fn restart_game_test() {
  let _game_over_state =
    game.Game(
      state: game.GameOver,
      player_score: 3,
      ai_score: 5,
      ball: game.Ball(x: 100.0, y: 100.0, vx: -3.0, vy: 2.0, radius: 8.0),
      player_paddle: game.Paddle(
        x: 30.0,
        y: 200.0,
        width: 15.0,
        height: 100.0,
        speed: 8.0,
      ),
      ai_paddle: game.Paddle(
        x: 755.0,
        y: 50.0,
        width: 15.0,
        height: 100.0,
        speed: 6.0,
      ),
    )
  let restarted_game = game.restart_game()

  restarted_game.state |> should.equal(game.Playing)
  restarted_game.player_score |> should.equal(0)
  restarted_game.ai_score |> should.equal(0)
  restarted_game.ball.x |> should.equal(400.0)
  restarted_game.ball.y |> should.equal(200.0)
  restarted_game.player_paddle.y |> should.equal(150.0)
  restarted_game.ai_paddle.y |> should.equal(150.0)
}
