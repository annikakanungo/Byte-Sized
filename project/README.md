# Byte-sized

#### Video Demo: <put the URL once recorded>

#### About

Byte-Sized is a web-based flashcard application built with Flask and SQLite that lets users create their own study cards, quiz themselves, and track how well they're learning each card over time. The idea behind the project was to build something useful for studying — not just a static list of questions and answers, but a tool that adapts to show you what you actually need to review, based on your own performance history.

The core workflow is simple: a user adds a flashcard by typing a question and an answer, which gets saved to a SQLite database. From there, they can go to the Study page, where the app picks a random card from their collection, hides the answer until they're ready to reveal it, and then asks them to self-report whether they got it right or wrong. That response updates a running count of correct and incorrect attempts for that specific card. Over time, this builds up a picture of which cards are being mastered and which ones need more attention — visible on the Stats page, which lists every card sorted by how often it's been missed, so the cards you're struggling with most rise to the top.

Beyond the study loop, the app supports full CRUD functionality. Users can edit a card if they made a typo or want to reword a question, and delete cards they no longer need. This was an intentional design decision — many simple flashcard tools only let you add cards, with no way to clean up mistakes, which makes the tool frustrating to actually use over time.

## File Structure

**app.py** contains all of the application's backend logic, structured around Flask routes:
- `/` (GET) displays the home page, listing all saved cards and providing the "Add a Card" form.
- `/add` (POST) handles new card submissions, validating that both a question and answer were provided before inserting into the database.
- `/study` (GET) selects a random card from the database and displays it on the study page. If there are no cards yet, it redirects back to the home page rather than showing a broken page.
- `/answer` (POST) records whether the user got a card right or wrong by incrementing the appropriate counter column in the database, then sends the user to another random card, creating a continuous quiz loop.
- `/stats` (GET) queries all cards sorted by incorrect count in descending order, so the most-missed cards are the most visible.
- `/edit/<card_id>` (GET and POST) shows a pre-filled form for editing an existing card, and processes the update when submitted.
- `/delete/<card_id>` (POST) removes a card from the database entirely.

A small `get_db()` helper function centralizes the SQLite connection logic and sets `row_factory` to `sqlite3.Row`, which allows database rows to be accessed by column name (e.g. `card["question"]`) rather than by numeric index, making the template code far more readable.

**templates/** contains the four Jinja2 HTML templates that make up the user interface: `index.html` (home page with the add-card form and card list), `study.html` (the quiz interface), `stats.html` (the performance table), and `edit.html` (the card-editing form). Each template links to a shared stylesheet, so navigation between pages feels consistent.

**static/styles.css** holds all of the application's CSS, giving the otherwise plain HTML a clean, modern look — card-style list items, a consistent color palette, styled buttons and forms, and a readable typography scale.

**flashcards.db** is the SQLite database file containing a single `cards` table with columns for `id`, `question`, `answer`, `correct_count`, and `incorrect_count`.

## Design Decisions

One design choice was keeping the app single-user with no login system. Early in development, I considered adding authentication so multiple people could keep separate card decks, but decided against it for this version in order to focus development time on getting the core study loop — quizzing, tracking, and reviewing — working well and thoroughly tested, rather than spreading effort across features that weren't essential to the app's central purpose.

Another decision was using self-reported correctness (the user clicking "I got it right" or "I got it wrong") rather than trying to programmatically check answer text against user input. Flashcard answers are often free-form and subjective (e.g. accepting "USA" and "United States" as equally correct), so self-assessment was both simpler to implement and more honest to how people actually use flashcards to study.

## AI Assistance

Portions of this project's code and structure were developed with assistance from Claude (Anthropic), including debugging help, Flask routing patterns, and CSS styling. All logic was reviewed, tested, and understood before inclusion. This is also noted in a comment at the top of app.py. 
