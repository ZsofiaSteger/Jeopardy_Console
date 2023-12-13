import pandas as pd
from thefuzz import fuzz
from rich.console import Console
from rich.panel import Panel
from rich import box

LARGE_PANEL_WIDTH = 90
SMALL_PANEL_WIDTH = 60

console = Console()

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
        console.print(Panel(f'[bold cyan]{active_question.value}[/bold cyan], [bold bright_green]Category: {active_question.category}[/bold bright_green]', title=f'Question {i}', title_align='left', width=SMALL_PANEL_WIDTH))
        i += 1

def check_answer(user_answer, correct_answer):
    if fuzz.ratio(user_answer, correct_answer) > 80:
        console.print(f'[bold green]Correct![/bold green] The answer was: {correct_answer}')
        return True
    else:
        console.print(f'[bold red]Incorrect.[/bold red] The correct answer was: {correct_answer}')
        return False

def get_score(answer_status, old_score, answer_value):
    if answer_status == True:
        return old_score + answer_value
    else:
        return old_score - answer_value

def get_quiz(number_of_rounds):
    score = 1000
    jeopardy_df = load_data()
    for round in range(0, number_of_rounds):
        if score < 0:
            print("You have a negative score. Game over!")
            return score
        
        active_questions = get_active_questions(jeopardy_df)
        print("Choose your question:")
        display_questions(active_questions)
        
        chosen_one = input("Enter the number of the question you want to answer: ")
        chosen_one = int(chosen_one) - 1
        console.print(Panel(f'[bold magenta]{active_questions.iloc[chosen_one].question}[/bold magenta]', title='The question is:', title_align='left', width=LARGE_PANEL_WIDTH))

        user_answer = input("Enter your answer: ")
        answer_status = check_answer(user_answer, active_questions.iloc[chosen_one].answer)
        score = get_score(answer_status, score, int(active_questions.iloc[chosen_one].value.replace('$', '').replace(',', '')))
        console.print(Panel(f'[bold yellow]Your score is: {score}[/bold yellow]', width=SMALL_PANEL_WIDTH))
    
    return score

if __name__ == "__main__":
    print(f'Your final score is: {get_quiz(5)}')