This is a small, hacky script for playing around with Wordle patterns/art:

Given a target solution and a sequence of Wordle color patterns (gray/yellow/green), it checks whether those patterns are even possible, and then tries to find an actual sequence of guesses that would produce them. While doing so, it enforces that each guess must reduce the remaining pool of valid solutions.

It follows the real Wordle scoring rules, brute-forces a lot of things, and is mostly meant for experimentation and curiosity—not speed or cleanliness.
