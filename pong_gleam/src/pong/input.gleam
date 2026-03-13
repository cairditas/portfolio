pub type InputState {
  InputState(up_pressed: Bool, down_pressed: Bool, space_pressed: Bool)
}

pub fn init_input() -> InputState {
  InputState(up_pressed: False, down_pressed: False, space_pressed: False)
}

pub fn handle_key_down(input_state: InputState, key: String) -> InputState {
  case key {
    "ArrowUp" -> InputState(..input_state, up_pressed: True)
    "w" -> InputState(..input_state, up_pressed: True)
    "ArrowDown" -> InputState(..input_state, down_pressed: True)
    "s" -> InputState(..input_state, down_pressed: True)
    " " -> InputState(..input_state, space_pressed: True)
    _ -> input_state
  }
}

pub fn handle_key_up(input_state: InputState, key: String) -> InputState {
  case key {
    "ArrowUp" -> InputState(..input_state, up_pressed: False)
    "w" -> InputState(..input_state, up_pressed: False)
    "ArrowDown" -> InputState(..input_state, down_pressed: False)
    "s" -> InputState(..input_state, down_pressed: False)
    " " -> InputState(..input_state, space_pressed: False)
    _ -> input_state
  }
}

pub fn get_player_direction(input_state: InputState) -> Float {
  case input_state.up_pressed, input_state.down_pressed {
    True, False -> -1.0
    False, True -> 1.0
    _, _ -> 0.0
  }
}
