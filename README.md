# Rating-Estimator
This is my attempt at creating a USCF rating estimator. The end goal is to create a version of this that I can run on my website, but for the time being I just wanted
to create a functional product in an environment I'm more comfortable with before I try to make it more user friendly. Still a couple of things to iron out for now
before I get to that point.

The program currently is designed to split into two different paths based on whether or not the player currently has a rating, store the rating if the player has one, and then get the rating of the player's opponents in each round.
If using the provisional formula, it simply averages the opponents ratings, and uses this alongside the USCF's formula to spit out a new, provisional rating.

If using the "standard" formula, for players with an established rating, it first determines the player's win probability for each opponent based on the difference between their ratings. It then finds the number of "effective games" the player has played, which is used to determine the rating uncertainty, aka the "K" factor. This is then used to determine the new rating and the bonus, if applicable. Generally, the player will earn a bonus if they have an "impressive" performance for their rating, i.e. a score substantially higher than their expected score, as determined by the bonus formula.

♥
