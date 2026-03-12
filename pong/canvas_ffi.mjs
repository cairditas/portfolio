// Canvas FFI functions for Gleam Pong game

export function clear_canvas(context, width, height) {
  context.fillStyle = '#000';
  context.fillRect(0, 0, width, height);
}

export function draw_ball(context, ball) {
  context.fillStyle = '#fff';
  context.beginPath();
  context.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  context.fill();
}

export function draw_paddle(context, paddle) {
  context.fillStyle = '#fff';
  context.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
}

export function draw_score(context, player_score, ai_score) {
  context.fillStyle = '#fff';
  context.font = '48px monospace';
  context.fillText(player_score.toString(), 300, 60);
  context.fillText(ai_score.toString(), 460, 60);
}

export function draw_game_over(context, player_score, ai_score) {
  context.fillStyle = '#fff';
  context.font = '48px monospace';
  context.textAlign = 'center';
  
  if (player_score > ai_score) {
    context.fillText('YOU WIN!', 400, 150);
  } else {
    context.fillText('YOU LOSE!', 400, 150);
  }
  
  context.font = '24px monospace';
  context.fillText(`Final Score: ${player_score} - ${ai_score}`, 400, 200);
  context.fillText('Press SPACE to play again', 400, 250);
  
  context.textAlign = 'left';
}
