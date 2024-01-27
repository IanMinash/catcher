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