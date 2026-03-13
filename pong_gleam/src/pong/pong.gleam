import gleam/io
import pong/game

pub fn main() -> Nil {
  io.println("Hello from pong!")
  let _ = game.init_game()
  Nil
}
