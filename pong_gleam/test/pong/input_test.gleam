import gleeunit/should
import pong/input

// Tests for input handling and keyboard event processing
// Covers paddle movement controls and input validation

pub fn input_state_test() {
  let input_state = input.init_input()

  input_state.up_pressed |> should.equal(False)
  input_state.down_pressed |> should.equal(False)
  input_state.space_pressed |> should.equal(False)
}

pub fn handle_key_down_up_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, "ArrowUp")

  updated_state.up_pressed |> should.equal(True)
  updated_state.down_pressed |> should.equal(False)
  updated_state.space_pressed |> should.equal(False)
}

pub fn handle_key_down_down_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, "ArrowDown")

  updated_state.up_pressed |> should.equal(False)
  updated_state.down_pressed |> should.equal(True)
  updated_state.space_pressed |> should.equal(False)
}

pub fn handle_key_down_w_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, "w")

  updated_state.up_pressed |> should.equal(True)
  updated_state.down_pressed |> should.equal(False)
  updated_state.space_pressed |> should.equal(False)
}

pub fn handle_key_down_s_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, "s")

  updated_state.up_pressed |> should.equal(False)
  updated_state.down_pressed |> should.equal(True)
  updated_state.space_pressed |> should.equal(False)
}

pub fn handle_key_down_space_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, " ")

  updated_state.up_pressed |> should.equal(False)
  updated_state.down_pressed |> should.equal(False)
  updated_state.space_pressed |> should.equal(True)
}

pub fn handle_key_down_unknown_test() {
  let input_state = input.init_input()
  let updated_state = input.handle_key_down(input_state, "x")

  // Unknown key should not change state
  updated_state.up_pressed |> should.equal(False)
  updated_state.down_pressed |> should.equal(False)
  updated_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_up_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, "ArrowUp")
  let released_state = input.handle_key_up(pressed_state, "ArrowUp")

  released_state.up_pressed |> should.equal(False)
  released_state.down_pressed |> should.equal(False)
  released_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_down_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, "ArrowDown")
  let released_state = input.handle_key_up(pressed_state, "ArrowDown")

  released_state.up_pressed |> should.equal(False)
  released_state.down_pressed |> should.equal(False)
  released_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_w_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, "w")
  let released_state = input.handle_key_up(pressed_state, "w")

  released_state.up_pressed |> should.equal(False)
  released_state.down_pressed |> should.equal(False)
  released_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_s_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, "s")
  let released_state = input.handle_key_up(pressed_state, "s")

  released_state.up_pressed |> should.equal(False)
  released_state.down_pressed |> should.equal(False)
  released_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_space_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, " ")
  let released_state = input.handle_key_up(pressed_state, " ")

  released_state.up_pressed |> should.equal(False)
  released_state.down_pressed |> should.equal(False)
  released_state.space_pressed |> should.equal(False)
}

pub fn handle_key_up_unknown_test() {
  let input_state = input.init_input()
  let pressed_state = input.handle_key_down(input_state, "ArrowUp")
  let unchanged_state = input.handle_key_up(pressed_state, "x")

  // Unknown key release should not change state
  unchanged_state.up_pressed |> should.equal(True)
  unchanged_state.down_pressed |> should.equal(False)
  unchanged_state.space_pressed |> should.equal(False)
}

pub fn get_player_direction_up_test() {
  let input_state =
    input.InputState(
      up_pressed: True,
      down_pressed: False,
      space_pressed: False,
    )
  let direction = input.get_player_direction(input_state)

  direction |> should.equal(-1.0)
}

pub fn get_player_direction_down_test() {
  let input_state =
    input.InputState(
      up_pressed: False,
      down_pressed: True,
      space_pressed: False,
    )
  let direction = input.get_player_direction(input_state)

  direction |> should.equal(1.0)
}

pub fn get_player_direction_both_pressed_test() {
  let input_state =
    input.InputState(up_pressed: True, down_pressed: True, space_pressed: False)
  let direction = input.get_player_direction(input_state)

  // When both pressed, no movement (cancel out)
  direction |> should.equal(0.0)
}

pub fn get_player_direction_none_pressed_test() {
  let input_state =
    input.InputState(
      up_pressed: False,
      down_pressed: False,
      space_pressed: False,
    )
  let direction = input.get_player_direction(input_state)

  direction |> should.equal(0.0)
}

pub fn get_player_direction_space_pressed_test() {
  let input_state =
    input.InputState(
      up_pressed: False,
      down_pressed: False,
      space_pressed: True,
    )
  let direction = input.get_player_direction(input_state)

  // Space should not affect paddle direction
  direction |> should.equal(0.0)
}

pub fn multiple_key_sequence_test() {
  let initial = input.init_input()

  // Press up
  let up_pressed = input.handle_key_down(initial, "ArrowUp")
  up_pressed.up_pressed |> should.equal(True)

  // Press down while up is still pressed
  let both_pressed = input.handle_key_down(up_pressed, "ArrowDown")
  both_pressed.up_pressed |> should.equal(True)
  both_pressed.down_pressed |> should.equal(True)

  // Release up
  let up_released = input.handle_key_up(both_pressed, "ArrowUp")
  up_released.up_pressed |> should.equal(False)
  up_released.down_pressed |> should.equal(True)

  // Release down
  let all_released = input.handle_key_up(up_released, "ArrowDown")
  all_released.up_pressed |> should.equal(False)
  all_released.down_pressed |> should.equal(False)
}
