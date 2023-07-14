import math
def main():
    ##TODO: Correct for player who is rated but has played 8 or fewer games
    ##TODO: Correct the provisional rating system for perfect scores; ultimately implement the whole weirdly complicated thing
    ##TODO: Add a performance rating function
    #Brief line of prompts to determine whether to use a provisional rating system or the rating system for non-provisional players; Won't be necessary in the webpage form. Technically outdated as a concept, since the USCF has changed how they approach provisional ratings
    while True:
        israted = input("Do you already have a USCF rating? Please answer Y / N: ")
        if israted.upper() == "Y" or israted.upper() == "N":
            break
    if israted.upper() == "Y": #If they are already rated, get their current rating
        while True:
            current_rating = input("Please enter your current rating: ")
            if is_valid(current_rating) == True:
                current_rating = int(current_rating)
                break
        return(established_rating(current_rating))
    else:
        return(provisional_rating())


def is_valid(rating): #Since I'm asking for a lot of ratings, I made a helper function to check them
    try:
        rating = int(rating)
        if rating >= 100 and rating <= 3000:
            return True
        else:
            print("Invalid rating entered. Rating must be between 100 and 3000.")
            return False
    except ValueError:
        print("Invalid entry. Please enter a valid, numeric rating.")
        return False


def provisional_rating():
    #Get number of rounds in tournament
    while True:
        rounds = input("How many rounds was the tournament? ")
        try:
            rounds = int(rounds)
            if rounds < 0:
                print("Invalid entry. Number of rounds must be positive")
                continue
            break
        except ValueError:
            print("Invalid entry. Please enter a positive integer.")


    #Get each opps rating by round, then average them
    opponent_ratings = 0
    for round_number in range(1, (rounds+1)):
        while True:
            temp_opp_rating = input(f"What was your opponent's rating in round {round_number}? ")
            if is_valid(temp_opp_rating) == True:
                opponent_ratings += (int(temp_opp_rating))
                break
    opponent_ratings = opponent_ratings / rounds


    #Get player score
    while True:
        score = input("What was your total score? Treat a win as 1 point, draw as 0.5 points, and a loss as 0 points. ")
        try:
            score = float(score)
            if score < 0 or (score * 2).is_integer() == False:
                print("Invalid entry. Please enter a positive number, with a .5 if needed (e.g. 1.5)")
                continue
            if score > rounds:
                print("Invalid entry. Score cannot be greater than total rounds played.")
                continue
            break
        except ValueError:
            print("Invalid entry. Please enter a positive number, with a .5 if needed (e.g. 1.5)")


    #Lastly, plug in the score, rounds, and average opponent rating to spit out the new rating
    new_rating = round(opponent_ratings + (((score * 2) - rounds) * 400) / rounds)
    if new_rating < 100:
        new_rating = 100
    if new_rating > 2700:
        new_rating = 2700
    print(f"Your rating is {new_rating}")


def established_rating(current_rating):
    #Get number of rounds in tournament
    while True:
        rounds = input("How many rounds was the tournament? ")
        try:
            rounds = int(rounds)
            if rounds <= 0:
                print("Invalid entry. Number of rounds must be positive")
                continue
            break
        except ValueError:
            print("Invalid entry. Please enter a positive integer.")


    #Take each opponents rating, generate the win probability against this opponent from the user's given rating, and add together to get a total expected score. The win probability formula defined in win_expectancy was devised by the USCF for their rating system
    expected_score = 0
    for round_number in range(1, (rounds+1)):
        while True:
            temp_opp_rating = input(f"What was your opponent's rating in round {round_number}? ")
            if is_valid(temp_opp_rating) == True:
                expected_score += (win_expectancy(float(current_rating), float(temp_opp_rating)))
                break


    ##The K factor used to be a static number based on the player's pre-event rating, but in researching this project, I learned it is now calculated based on the number of games the player has played in their career. Unfortunately, this means another user input prompt in this form of the program, which is beginning to get rather tedious. Fortunately in the webpage this will be less obnoxious. There's also a different formula depending on the time control of the event, which for now I'm ignoring; too many prompts
    while True:
        game_total = input(f"Roughly how many rated games had you played before this tournament? ")
        try:
            game_total = int(game_total)
            if game_total <= 0:
                print("Invalid entry. Number of games must be positive")
                continue
            break
        except ValueError:
            print("Invalid entry. Please enter a positive integer.")
    if current_rating > 2355:
        effective_games = min(game_total, 50)
    else:
        effective_games = min(game_total, (50 / (math.sqrt(.662 + 0.00000739 * (2569 - current_rating) ** 2))))
    K = 800/(effective_games + rounds)

    while True:
        score = input("What was your total score? Treat a win as 1 point, draw as 0.5 points, and a loss as 0 points. ")
        try:
            score = float(score)
            if score < 0 or (score * 2).is_integer() == False:
                print("Invalid entry. Please enter a positive number, with a .5 if needed (e.g. 1.5)")
                continue
            if score > rounds:
                print("Invalid entry. Score cannot be greater than total rounds played.")
                continue
            break
        except ValueError:
            print("Invalid entry. Please enter a positive number, with a .5 if needed (e.g. 1.5)")

    #I compared to the uscf calculator and noticed I was a few points off on some calcs. After tinkering with my bonus, I determined the reason is that, for some reason, they round the math.sqrt(rounds) before even multiplying by 14, much less finishing the bonus calculation or the whole new rating calculation. I honestly might email Glickman to ask if that's what he intended, because that just seems so stupid to me that it can't be right
    bonus = max(0, K * (score - expected_score) - 14 * (math.sqrt(float(rounds))))
    new_rating = round(current_rating + (K * (score - expected_score) + bonus))
    print(f"Your new rating is {new_rating}")

def win_expectancy(rating, opp_rating):
    return(1/(1+(10**(-(rating - opp_rating)/400))))

if __name__ == "__main__":
    main()
