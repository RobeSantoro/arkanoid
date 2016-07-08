import math
from unittest import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import pygame

from arkanoid.sprites.paddle import Paddle


class TestPaddle(TestCase):

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_initialise(self, mock_pygame, mock_load_png):
        mock_screen, mock_area, mock_image, mock_rect = (
            Mock(), Mock(), Mock(), Mock())
        mock_screen.left = 0
        mock_screen.height = 650
        mock_screen.width = 600
        mock_rect.height = 10
        mock_pygame.Rect.return_value = mock_area
        mock_area.center = 'area center'
        mock_pygame.display.get_surface.return_value.get_rect.return_value = \
            mock_screen
        mock_load_png.return_value = mock_image, mock_rect

        paddle = Paddle(left_offset=10, right_offset=10, bottom_offset=20)

        self.assertEqual(paddle.image, mock_image)
        self.assertEqual(paddle.rect, mock_rect)
        self.assertIs(paddle.visible, True)
        mock_pygame.Rect.assert_called_once_with(10, 630, 580, 10)
        self.assertEqual(paddle.rect.center, 'area center')

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_update_moves_when_in_area(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area, mock_new_rect = (
            Mock(), Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_rect.move.return_value = mock_new_rect
        mock_area.contains.return_value = True

        paddle = Paddle()
        paddle.update()

        self.assertEqual(paddle.rect, mock_new_rect)

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_update_not_move_when_not_in_area(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area, mock_new_rect = (
            Mock(), Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_rect.move.return_value = mock_new_rect
        mock_area.contains.return_value = False

        paddle = Paddle()
        paddle.update()

        self.assertEqual(paddle.rect, mock_rect)

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_move_left(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area = (Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_area.contains.return_value = True

        paddle = Paddle()
        paddle.move_left()
        paddle.update()

        mock_rect.move.assert_called_once_with(-10, 0)

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_move_right(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area = (Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_area.contains.return_value = True

        paddle = Paddle(speed=15)
        paddle.move_right()
        paddle.update()

        mock_rect.move.assert_called_once_with(15, 0)

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_stop(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area = (Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_area.contains.return_value = True

        paddle = Paddle()
        paddle.stop()
        paddle.update()

        mock_rect.move.assert_called_once_with(0, 0)

    @patch('arkanoid.sprites.paddle.load_png')
    @patch('arkanoid.sprites.paddle.pygame')
    def test_reset(self, mock_pygame, mock_load_png):
        mock_image, mock_rect, mock_area = (Mock(), Mock(), Mock())
        mock_load_png.return_value = mock_image, mock_rect
        mock_pygame.Rect.return_value = mock_area
        mock_area.contains.return_value = True
        mock_area.center = 'the centre'

        paddle = Paddle()
        paddle.reset()
        paddle.update()

        self.assertEqual(mock_rect.center, 'the centre')

    def test_bounce_strategy(self):
        angles = []
        paddle = pygame.Rect(100, 600, 60, 15)

        for i in range(103, 163, 10):
            ball = pygame.Rect(i, 602, 5, 5)
            angle = Paddle.bounce_strategy(paddle, ball)
            angles.append(int(math.degrees(angle)))

        self.assertTrue(angles[0], -130)
        self.assertTrue(angles[1], -115)
        self.assertTrue(angles[2], -100)
        self.assertTrue(angles[3], -80)
        self.assertTrue(angles[4], -65)
        self.assertTrue(angles[5], -50)
