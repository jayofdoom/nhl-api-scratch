import requests
import random

def fetch_random_team():
    """
    Fetch a random NHL team and return its name and id.
    """
    response = requests.get("https://statsapi.web.nhl.com/api/v1/teams")
    response.raise_for_status()
    teams = response.json()['teams']
    team = random.choice(teams)
    return team['name'], team['id']

def fetch_team_stats(team_id):
    """
    Fetch statistics for a given team.
    """
    url = f"https://statsapi.web.nhl.com/api/v1/teams/{team_id}/stats"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['stats'][0]['splits'][0]['stat']

def formulate_question(team_name, stats):
    """
    Generate a trivia question based on team statistics.
    """
    questions = [
        f"How many games did the {team_name} win in the latest season?",
        f"How many points did the {team_name} score in the latest season?",
        f"How many goals against did the {team_name} have in the latest season?"
    ]
    answers = [
        stats['wins'],
        stats['pts'],
        # stats['goalsAgainst'] ## This was originally the line from ChatGPT.
        float(stats['goalsAgainstPerGame']) * int(stats['gamesPlayed'])
    ]
    
    idx = random.randint(0, len(questions) - 1)
    return questions[idx], answers[idx]

def main():
    team_name, team_id = fetch_random_team()
    stats = fetch_team_stats(team_id)
    question, answer = formulate_question(team_name, stats)
    print(question)
    user_answer = int(input("Your answer: "))
    if user_answer == answer:
        print("Correct!")
    else:
        print(f"Wrong! The correct answer is {answer}.")

if __name__ == "__main__":
    main()
