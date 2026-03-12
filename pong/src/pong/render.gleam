import pong/game

// External JavaScript types
pub type CanvasContext

// External JavaScript functions
@external(javascript, "../canvas_ffi.mjs", "clear_canvas")
pub fn clear_canvas(context: CanvasContext, width: Float, height: Float) -> Nil

@external(javascript, "../canvas_ffi.mjs", "draw_ball")
pub fn draw_ball(context: CanvasContext, ball: game.Ball) -> Nil

@external(javascript, "../canvas_ffi.mjs", "draw_paddle")
pub fn draw_paddle(context: CanvasContext, paddle: game.Paddle) -> Nil

@external(javascript, "../canvas_ffi.mjs", "draw_score")
pub fn draw_score(
  context: CanvasContext,
  player_score: Int,
  ai_score: Int,
) -> Nil

@external(javascript, "../canvas_ffi.mjs", "draw_game_over")
pub fn draw_game_over(
  context: CanvasContext,
  player_score: Int,
  ai_score: Int,
) -> Nil

// Mock context for testing
pub type MockContext {
  MockContext
}

pub fn get_mock_context() -> MockContext {
  MockContext
}
