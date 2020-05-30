# Isaac Burmingham

import unittest
from blackjack3 import Hand,Strategy

class UnitTestBlackjack(unittest.TestCase):

    def test_score(self):
        # testing the scores from the assignment
        hand1 = Hand([3,12])
        hand2 = Hand([5,5,10])
        hand3 = Hand([11,10,1])
        hand4 = Hand([1,5])
        hand5 = Hand([1,1,5])
        hand6 = Hand([1,1,1,7])
        hand7 = Hand([7,8,10])
        # adding a few
        hand8 = Hand([1,1])
        hand9 = Hand([1,1,1])

        # test _init_ that empty list can be passed
        empty = Hand([])
        self.assertTrue(len(empty.cards) == 0)

        # test score
        self.assertEqual(hand1.score(),(13,0))
        self.assertEqual(hand2.score(),(20,0))
        self.assertEqual(hand3.score(),(21,0))
        self.assertEqual(hand4.score(),(16,1))
        self.assertEqual(hand5.score(),(17,1))
        self.assertEqual(hand6.score(),(20,1))
        self.assertEqual(hand7.score(),(25,0))
        self.assertEqual(hand8.score(),(12,1))
        self.assertEqual(hand9.score(),(13,1))
        self.assertTrue(hand9.score()[1] <= 1) # check that soft count cannot be greater than 1

        # test add_card
        hand10 = Hand()
        hand10.add_card()
        hand10.add_card()
        self.assertTrue(len(hand10.cards) >= 2)

        # test is blackjack (Ace & 10,11,12,13)
        bj1 = Hand([1,10])
        bj2 = Hand([1,11])
        bj3 = Hand([1,12])
        bj4 = Hand([1,13])
        bj5 = Hand([10,10]) # not blackjack

        self.assertTrue(bj1.is_blackjack())
        self.assertTrue(bj2.is_blackjack())
        self.assertTrue(bj3.is_blackjack())
        self.assertTrue(bj4.is_blackjack())
        self.assertFalse(bj5.is_blackjack())

        # test bust
        bust1 = Hand([10,10,5])
        bust2 = Hand([1,1,11,12])
        bust3 = Hand([1,10,11]) # not a bust

        self.assertTrue(bust1.is_bust())
        self.assertTrue(bust2.is_bust())
        self.assertFalse(bust3.is_bust())


    # test Strategy

    def test_stand(self):

        hand1 = Strategy(17,True).stand(Hand([6,1])) # (17,1)
        hand2 = Strategy(17,True).stand(Hand([10,11])) # (20,0)
        hand3 = Strategy(13,True).stand(Hand([1,1])) # (12,1)
        hand4 = Strategy(17,True).stand(Hand([1,1,5])) # (17,1)
        hand5 = Strategy(16,True).stand(Hand([5,5])) #(10,0)
        hand6 = Strategy(17,True).stand(Hand([10,7])) # (17,0)
        # using the same hands but now stand on hard
        hand7 = Strategy(17,False).stand(Hand([6,1])) # (17,1)
        hand8 = Strategy(17,False).stand(Hand([10,11])) # (20,0)
        hand9 = Strategy(13,False).stand(Hand([1,1])) # (12,1)
        hand10 = Strategy(17,False).stand(Hand([1,1,5])) # (17,1)
        hand11 = Strategy(16,False).stand(Hand([5,5])) #(10,0)
        hand12 = Strategy(17,False).stand(Hand([10,7])) # (17,0)

        #first block
        self.assertTrue(hand1[0])
        self.assertTrue(hand2[0])
        self.assertFalse(hand3[0])
        self.assertTrue(hand4[0])
        self.assertFalse(hand5[0])
        self.assertTrue(hand6[0])

        #second block
        self.assertFalse(hand7[0])
        self.assertTrue(hand8[0])
        self.assertFalse(hand9[0])
        self.assertFalse(hand10[0])
        self.assertFalse(hand11[0])
        self.assertTrue(hand12[0])


    def test_play_hand(self):
        hand1 = Strategy(13,True).play()
        hand2 = Strategy(20,True).play()
        hand3 = Strategy(13,False).play()
        hand4 = Strategy(20,False).play()

        # check that the scores are bounded by the stand value
        self.assertTrue(hand1.score()[0] >= 13)
        self.assertTrue(hand2.score()[0] >= 20)
        self.assertTrue(hand3.score()[0] >= 13)
        self.assertTrue(hand4.score()[0] >= 20)


if __name__ == "__main__":
    unittest.main()
