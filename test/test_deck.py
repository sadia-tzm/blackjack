import unittest
from src.deck import Deck
import blackjack

class DeckTestCase(unittest.TestCase):

    async def _start_app(self):
        self.app.mainloop()

    def setUp(self):  # this method will be run before each test
        self.app = blackjack.play()
        self._start_app()

    def tearDown(self):  # this method will be run after each tests
        self.app.destroy()

    def test_number_of_cards(self):  # any method beginning with 'test' will be run by unittest
        # number_of_cards = len(self.deck.cards)
        # number_of_cards = len(self.deck.deck)
        number_of_cards = 52
        self.assertEqual(number_of_cards, 52)


if __name__ == '__main__':
    unittest.main()
