# Gemini Code Review

This document provides an overview of the simple banking application, how to run it, and how it works.

## Project Overview

This is a simple banking application built with FastAPI and a plain JavaScript frontend. It allows users to view account balances and transfer funds between accounts.

## How to Run

1.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the application:**
    ```bash
    uvicorn main:app --reload
    ```
3.  **Open a web browser** to `http://127.0.0.1:8000`.

## How it Works

*   The backend is a FastAPI server that provides an API for getting account data and performing transfers.
*   The database is a simple SQLite file (`bank.db`) that is automatically created and seeded with sample data on the first run.
*   The frontend is a single HTML page that uses JavaScript to communicate with the backend API and update the view dynamically.
*   Fund transfers are handled in a transaction to ensure data consistency.

## How to Test

*   Run the test suite with the command:
    ```bash
    pytest
    ```
