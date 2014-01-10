Da Vyncy Challenge
==================

https://www.codeeval.com/open_challenges/77/

The challenge involves string matching and proper indexing. The solution isn't optimized, but it gets the job done. It runs through each fragment and checks its overlap score with the fragments ahead of it. Overlap must occur on the start / end of either string. That is, if the match starts on the end of one string, it must go to the start of another.

This is repeated until no overlaps remain between the fragments. Ties are broken arbitrarily as the input does not require a specific method. However, situations may arise when a deciding factor is needed. An example of such a factor could implement a greedy approach and choose the overlapping strings that result in the largest fragment.
