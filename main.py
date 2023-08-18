import random
import time
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

COLORS = ['red', 'blue', 'green', 'yellow']
SEQUENCE_LENGTH = 5

def generate_sequence(length):
    """Generate a random sequence of colors."""
    return [random.choice(COLORS) for _ in range(length)]

def display_sequence(sequence):
    """Display the Simon Says sequence."""
    print("\nSimon says:")
    for color in sequence:
        print(color)
        time.sleep(1)

async def get_player_sequence(request: Request):
    """Get the player's sequence input from the form."""
    player_sequence = []
    for _ in range(SEQUENCE_LENGTH):
        selected_color = await request.form()
        player_sequence.append(selected_color['selected_color'].lower())
    return player_sequence

def check_sequence(player_sequence, sequence):
    """Check if the player's sequence matches the generated sequence."""
    return player_sequence == sequence

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Display the game interface and Simon Says sequence."""
    sequence = generate_sequence(SEQUENCE_LENGTH)
    display_sequence(sequence)
    return templates.TemplateResponse("simon.html", {"request": request, "sequence": sequence})

@app.post("/check")
async def check(request: Request, selected_color: str = Form(...)):
    """Check the player's sequence against the generated sequence."""
    sequence = generate_sequence(SEQUENCE_LENGTH)
    player_sequence = [selected_color]
    player_sequence.extend(await get_player_sequence(request))
    
    if check_sequence(player_sequence, sequence):
        result = "Congratulations! You repeated the sequence correctly."
    else:
        result = "Oops! You made a mistake. Try again."

    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
