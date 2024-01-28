# Catcher
## Task
Utilize a phrase database provided below. The desired functionality is to:
1. Receive a sentence and provide a corresponding response mapping for it.
The phrases will be of the format:

    | catch phrase | keyword |
    |--------------|---------|
    | (0,2) block me (0,1) | BLOCK |
    | (0,1) kill myself | KILL |
    | (0,1) can you (0,1) me (0,1) joke (0,0) | JOKE |
    | Love me | LOVE |


    (0,3) means it can allow 0 up to 3 words in the sentence.

    (0,2) are you doing (0, 1) should be able to catch sentences like “Hey what are you doing tonight?”, “What are you doing?” “Hi what are you doing after?” 

2. Add phrases to the database (by reading from a csv file), delete, edit the mapping answer for it.

## Solution
The project has been built on FastAPI. The following assumptions have been made;
1. The words in a regex will be valid regex words. i.e `[A-Za-z0-9_]+`
2. The words in the sentences may only be followed by 1 punctuation mark in the set `(, . : ; ! ?)`. As such, `hi, how are you doing today?` is a valid sentence, but `hi,, how are you doing today?` is not for the input phrase: `(0,2) are you doing (0,1)`.

### How matches happen
On creation of a `CatchPhrase` object, the `(minWords, maxWords)` segments substituted by a regex and persisted to the Database. When you request to match a particular sentence, the sentence is split into its individual words, and, using the `IN` operator in `SQL` a subset of `CatchPhrase`s objects are retrieved from the database. A full regex match is then performed against the records in these subset. The first record to return a full match will be returned as the mapping answer.

### Running it
The following environment variable is available;
- `DB_URL`: set it to a valid connection string for a DB you want to connect to. If not provided, it will default to using a SQLLite database in the project directory.

#### 1. Docker
Using Docker, you can run the project using the following command:
```
docker run -p 8000:8000 ghcr.io/ianminash/catcher:main
```

#### 2. Python
- Install the project dependencies from the `requirements.txt` file using `pip` or `pipenv` if using a virtual environment.
- Run the project using `uvicorn`:
    ```
    uvicorn main:app
    ```
    This will bring up the service on port `8000`.