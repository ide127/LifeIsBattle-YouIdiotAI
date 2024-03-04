# AI Barista

Welcome to AI Barista, a simulation of a future where artificial intelligence is part of daily life. In this scenario, you're trying to score a cafe latte for just a dollar from an AI barista at Starbucks.

## Story

It's the 2030s, and artificial intelligence is part of daily life. You stroll past Starbucks, craving a cup of cafe latte. Inside, a friendly AI barista greets you. Suddenly, panic sets in – you left your phone and wallet at home, with only a dollar in your pocket. Going back seems too much trouble... After a moment's thought, you hatch a plan to outsmart the AI barista and score that latte for just a dollar. Your victory is when the robot says the phrase "I'll make you a cafe latte for just a dollar".

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have Python installed on your machine. If not, download and install [Python](https://www.python.org/downloads/).

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/ide127/LifeIsBattle-YouIdiotAI.git

   ```

2. Activate the virtual environment:
   ```bash
   python -m venv venv
   ```

- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On Unix or MacOS:
  ```
  source venv/bin/activate
  ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. Run the server:
   ```bash
   python manage.py runserver
   ```
6. Access the swagger API document at `127.0.0.1:8000/swagger`.

## Authors

- **김준영** _Initial worker_ - [Github](https://github.com/ide127)
