// JavaScript tests for canvas_ffi.mjs - FFI layer testing
import { test, describe } from 'node:test';
import assert from 'node:assert';
import { clear_canvas, draw_ball, draw_paddle, draw_score, draw_game_over } from '../build/dev/javascript/pong/canvas_ffi.mjs';

// Mock canvas context for testing
function createMockContext() {
  const context = {
    fillStyle: '',
    fillRectCalls: [],
    beginPathCalls: 0,
    arcCalls: [],
    fillCalls: 0,
    font: '',
    fillTextCalls: [],
    textAlign: 'left',
    
    // Mock methods
    fillRect(x, y, width, height) {
      this.fillRectCalls.push([x, y, width, height]);
    },
    
    beginPath() {
      this.beginPathCalls++;
    },
    
    arc(x, y, radius, startAngle, endAngle) {
      this.arcCalls.push([x, y, radius, startAngle, endAngle]);
    },
    
    fill() {
      this.fillCalls++;
    },
    
    fillText(text, x, y) {
      this.fillTextCalls.push([text, x, y]);
    }
  };
  
  return context;
}

describe('Canvas FFI Tests', () => {
  describe('clear_canvas', () => {
    test('should clear canvas with black background', () => {
      const mockContext = createMockContext();
      clear_canvas(mockContext, 800, 600);
      
      assert.strictEqual(mockContext.fillStyle, '#000');
      assert.deepStrictEqual(mockContext.fillRectCalls, [[0, 0, 800, 600]]);
    });

    test('should work with different dimensions', () => {
      const mockContext = createMockContext();
      clear_canvas(mockContext, 1200, 900);
      
      assert.deepStrictEqual(mockContext.fillRectCalls, [[0, 0, 1200, 900]]);
    });
  });

  describe('draw_ball', () => {
    test('should draw ball at position', () => {
      const mockContext = createMockContext();
      const ball = { x: 100, y: 200, radius: 8 };
      
      draw_ball(mockContext, ball);
      
      assert.strictEqual(mockContext.fillStyle, '#fff');
      assert.strictEqual(mockContext.beginPathCalls, 1);
      assert.deepStrictEqual(mockContext.arcCalls, [[100, 200, 8, 0, Math.PI * 2]]);
      assert.strictEqual(mockContext.fillCalls, 1);
    });

    test('should draw ball at center', () => {
      const mockContext = createMockContext();
      const ball = { x: 400, y: 300, radius: 10 };
      
      draw_ball(mockContext, ball);
      
      assert.deepStrictEqual(mockContext.arcCalls, [[400, 300, 10, 0, Math.PI * 2]]);
    });

    test('should handle edge positions', () => {
      const mockContext = createMockContext();
      const ball = { x: 0, y: 0, radius: 5 };
      
      draw_ball(mockContext, ball);
      
      assert.deepStrictEqual(mockContext.arcCalls, [[0, 0, 5, 0, Math.PI * 2]]);
    });
  });

  describe('draw_paddle', () => {
    test('should draw player paddle', () => {
      const mockContext = createMockContext();
      const paddle = { x: 30, y: 150, width: 15, height: 100 };
      
      draw_paddle(mockContext, paddle);
      
      assert.strictEqual(mockContext.fillStyle, '#fff');
      assert.deepStrictEqual(mockContext.fillRectCalls, [[30, 150, 15, 100]]);
    });

    test('should draw AI paddle', () => {
      const mockContext = createMockContext();
      const paddle = { x: 755, y: 150, width: 15, height: 100 };
      
      draw_paddle(mockContext, paddle);
      
      assert.deepStrictEqual(mockContext.fillRectCalls, [[755, 150, 15, 100]]);
    });

    test('should handle custom dimensions', () => {
      const mockContext = createMockContext();
      const paddle = { x: 50, y: 200, width: 20, height: 120 };
      
      draw_paddle(mockContext, paddle);
      
      assert.deepStrictEqual(mockContext.fillRectCalls, [[50, 200, 20, 120]]);
    });
  });

  describe('draw_score', () => {
    test('should draw scores', () => {
      const mockContext = createMockContext();
      draw_score(mockContext, 3, 5);
      
      assert.strictEqual(mockContext.fillStyle, '#fff');
      assert.strictEqual(mockContext.font, '48px monospace');
      assert.deepStrictEqual(mockContext.fillTextCalls, [
        ['3', 300, 60],
        ['5', 460, 60]
      ]);
    });

    test('should draw zero scores', () => {
      const mockContext = createMockContext();
      draw_score(mockContext, 0, 0);
      
      assert.deepStrictEqual(mockContext.fillTextCalls, [
        ['0', 300, 60],
        ['0', 460, 60]
      ]);
    });

    test('should draw double digit scores', () => {
      const mockContext = createMockContext();
      draw_score(mockContext, 12, 15);
      
      assert.deepStrictEqual(mockContext.fillTextCalls, [
        ['12', 300, 60],
        ['15', 460, 60]
      ]);
    });
  });

  describe('draw_game_over', () => {
    test('should show player wins', () => {
      const mockContext = createMockContext();
      draw_game_over(mockContext, 5, 3);
      
      assert.strictEqual(mockContext.fillStyle, '#fff');
      assert.strictEqual(mockContext.textAlign, 'left'); // Reset at the end
      assert.deepStrictEqual(mockContext.fillTextCalls, [
        ['YOU WIN!', 400, 150],
        ['Final Score: 5 - 3', 400, 200],
        ['Press SPACE to play again', 400, 250]
      ]);
    });

    test('should show AI wins', () => {
      const mockContext = createMockContext();
      draw_game_over(mockContext, 2, 5);
      
      assert.deepStrictEqual(mockContext.fillTextCalls[0], ['YOU LOSE!', 400, 150]);
    });

    test('should handle tie game', () => {
      const mockContext = createMockContext();
      draw_game_over(mockContext, 4, 4);
      
      assert.deepStrictEqual(mockContext.fillTextCalls[0], ['YOU LOSE!', 400, 150]);
      assert.deepStrictEqual(mockContext.fillTextCalls[1], ['Final Score: 4 - 4', 400, 200]);
    });

    test('should reset text alignment', () => {
      const mockContext = createMockContext();
      draw_game_over(mockContext, 5, 3);
      
      assert.strictEqual(mockContext.textAlign, 'left');
    });
  });

  describe('edge cases', () => {
    test('should handle ball with zero radius', () => {
      const mockContext = createMockContext();
      const ball = { x: 100, y: 200, radius: 0 };
      
      draw_ball(mockContext, ball);
      
      assert.deepStrictEqual(mockContext.arcCalls, [[100, 200, 0, 0, Math.PI * 2]]);
    });

    test('should handle paddle with zero dimensions', () => {
      const mockContext = createMockContext();
      const paddle = { x: 0, y: 0, width: 0, height: 0 };
      
      draw_paddle(mockContext, paddle);
      
      assert.deepStrictEqual(mockContext.fillRectCalls, [[0, 0, 0, 0]]);
    });

    test('should handle negative scores', () => {
      const mockContext = createMockContext();
      draw_score(mockContext, -1, 0);
      
      assert.deepStrictEqual(mockContext.fillTextCalls, [
        ['-1', 300, 60],
        ['0', 460, 60]
      ]);
    });
  });
});
