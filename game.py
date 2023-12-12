import pandas as pd
from thefuzz import fuzz
from rich import print as r_print

def load_data():
    jeopardy_df = pd.read_csv("data/jeopardy.csv")

    for col in jeopardy_df.columns:
        new_col = col.strip().lower().replace(" ", "_")
        jeopardy_df.rename(columns={col: new_col}, inplace=True)
    return jeopardy_df

def get_active_questions(jeopardy_df):
    active_questions = jeopardy_df.sample(5)
    active_questions.reset_index(inplace=True)
    return active_questions

def display_questions(active_questions):
    i = 1
    for active_question in active_questions.itertuples():
        print(f'{i}. Value: {active_question.value}, Category: {active_question.category}')
        i += 1

def check_answer(user_answer, correct_answer):
    if fuzz.ratio(user_answer, correct_answer) > 80:
        r_print(f'[bold green]Correct![/bold green] The answer was: {correct_answer}')
        return True
    else:
        r_print(f'[bold red]Incorrect.[/bold red] The correct answer was: {correct_answer}')
        return False

def get_score(answer_status, old_score, answer_value):
    if answer_status == True:
        return old_score + answer_value
    else:
        return old_score - answer_value

def get_quiz(number_of_rounds):
    score = 0
    jeopardy_df = load_data()
    for round in range(0, number_of_rounds):
        if score < 0:
            print("You have a negative score. Game over!")
            return score
        
        active_questions = get_active_questions(jeopardy_df)
        print("Choose your question:")
        display_questions(active_questions)
        
        chosen_one = input("Enter the number of the question you want to answer:")
        chosen_one = int(chosen_one) - 1
        print(f'The question is: {active_questions.iloc[chosen_one].question}')

        user_answer = input("Enter your answer: ")
        answer_status = check_answer(user_answer, active_questions.iloc[chosen_one].answer)
        score = get_score(answer_status, score, int(active_questions.iloc[chosen_one].value.replace('$', '')))
        
        print(f'Your score is: {score}')
    
    return score

if __name__ == "__main__":
    print(f'Your final score is: {get_quiz(2)}')