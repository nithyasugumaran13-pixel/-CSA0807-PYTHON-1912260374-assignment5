# A5 – AI Application Design

## Introduction

The air-quality monitoring system receives thousands of citizen complaints describing pollution-related problems. These complaints may contain information about smoke, dust, vehicle emissions, bad smells, and health-related discomfort.

Three simple AI-related applications can be designed to understand and process these complaints:

1. Sentiment Analysis
2. Extractive Text Summarisation
3. Rule-Based Chatbot

## A5.1 Sentiment Analysis Using a Lexicon-Based Approach

### Objective

Sentiment analysis identifies whether a citizen complaint expresses a positive, negative, or neutral opinion about air quality.

### Proposed Method

A lexicon-based approach uses predefined lists of positive and negative words.

**Positive words:**
- clean
- fresh
- improved
- better
- healthy

**Negative words:**
- pollution
- smoke
- dust
- harmful
- terrible
- unhealthy
- bad

### Algorithm

1. Receive a citizen complaint.
2. Convert the complaint into lowercase.
3. Split the complaint into individual words.
4. Compare each word with the positive and negative word lists.
5. Assign a positive score for positive words and a negative score for negative words.
6. Check for negation words such as "not", "no", and "never".
7. Reverse the sentiment contribution of a word when it is directly affected by negation.
8. Calculate the final sentiment score.
9. If the score is positive, classify the complaint as Positive.
10. If the score is negative, classify the complaint as Negative.
11. If the score is zero, classify the complaint as Neutral.

### Pseudocode

```text
ALGORITHM SENTIMENT_ANALYSIS(complaint)

BEGIN
    positive_words ← ["clean", "fresh", "better", "healthy"]
    negative_words ← ["pollution", "smoke", "dust", "harmful", "bad"]

    complaint ← CONVERT_TO_LOWERCASE(complaint)
    words ← SPLIT(complaint)
    score ← 0

    FOR each word at position i IN words DO
        IF word IS IN positive_words THEN
            contribution ← 1
        ELSE IF word IS IN negative_words THEN
            contribution ← -1
        ELSE
            contribution ← 0
        END IF

        IF i > 0 AND words[i - 1] IS IN ["not", "no", "never"] THEN
            contribution ← -contribution
        END IF

        score ← score + contribution
    END FOR

    IF score > 0 THEN
        sentiment ← "Positive"
    ELSE IF score < 0 THEN
        sentiment ← "Negative"
    ELSE
        sentiment ← "Neutral"
    END IF

    RETURN sentiment, score
END
```

### Example

Input complaint: "The air is not clean and contains harmful smoke."

The words "clean", "harmful", and "smoke" are identified. The word "clean" is affected by the negation word "not". The overall score is negative, so the complaint is classified as Negative.

**Limitation:** A basic lexicon-based approach may not understand sarcasm, complex sentences, or context-dependent meanings. It may also fail when negation is separated from the sentiment word by several words.

## A5.2 Extractive Text Summarisation

### Objective

Extractive summarisation produces a short summary by selecting important sentences directly from citizen complaints without generating completely new sentences.

### Proposed Method

The system identifies frequently occurring meaningful words and uses them to determine which sentences are important.

### Algorithm

1. Receive a collection of citizen complaints.
2. Convert all text into lowercase.
3. Split the text into individual sentences.
4. Remove common stop words such as "the", "is", "and", and "of".
5. Count the frequency of meaningful words.
6. Calculate a score for each sentence based on the frequency of important words it contains.
7. Rank the sentences according to their scores.
8. Select the highest-scoring sentences.
9. Arrange the selected sentences in their original order.
10. Display the final summary.

### Pseudocode

```text
ALGORITHM EXTRACTIVE_SUMMARISER(complaints, summary_limit)

BEGIN
    sentences ← SPLIT_INTO_SENTENCES(complaints)
    word_frequency ← EMPTY_DICTIONARY

    FOR each sentence IN sentences DO
        words ← SPLIT(sentence)

        FOR each word IN words DO
            word ← CONVERT_TO_LOWERCASE(word)

            IF word IS NOT A STOP WORD THEN
                word_frequency[word] ← word_frequency[word] + 1
            END IF
        END FOR
    END FOR

    sentence_scores ← EMPTY_LIST

    FOR each sentence IN sentences DO
        score ← 0
        words ← SPLIT(sentence)

        FOR each word IN words DO
            IF word EXISTS IN word_frequency THEN
                score ← score + word_frequency[word]
            END IF
        END FOR

        ADD (sentence, score) TO sentence_scores
    END FOR

    SORT sentence_scores BY SCORE IN DESCENDING ORDER

    selected_sentences ← SELECT TOP summary_limit SENTENCES

    ARRANGE selected_sentences IN ORIGINAL ORDER

    RETURN selected_sentences
END
```

### Example

Input complaints:

1. "Heavy smoke is coming from the nearby factory."
2. "The air contains dust and harmful smoke."
3. "People are experiencing breathing difficulties due to pollution."

Possible summary:

"Heavy smoke is coming from the nearby factory. The air contains dust and harmful smoke."

**Limitation:** Extractive summarisation selects existing sentences and may not produce a smooth or fully meaningful summary. Frequent words do not always represent the most important information.

## A5.3 Rule-Based Chatbot

### Objective

A rule-based chatbot answers common citizen questions about air quality using predefined keywords, rules, and information stored in the SQLite database.

### Proposed Method

The chatbot searches the user's question for keywords and selects an appropriate response.

### Example Rules

| User keyword or question | Chatbot response |
|---|---|
| PM2.5 | PM2.5 represents fine particulate matter in the air. |
| PM10 | PM10 represents particulate matter with a diameter of 10 micrometres or less. |
| pollution | Please specify the station or location to check pollution levels. |
| worst station | The system can identify the station with the highest average PM2.5. |
| temperature | The system can display the recorded temperature for a selected station. |
| help | You can ask about PM2.5, PM10, pollution levels, stations, or temperature. |

### Algorithm

1. Receive a question from the citizen.
2. Convert the question into lowercase.
3. Identify important keywords.
4. Match the keywords with predefined chatbot rules.
5. If the question requests pollution information, retrieve the relevant information from SQLite.
6. Generate a response based on the matched rule and database result.
7. If no rule matches, display a default message.
8. Return the response to the citizen.

### Pseudocode

```text
ALGORITHM RULE_BASED_CHATBOT(question)

BEGIN
    question ← CONVERT_TO_LOWERCASE(question)

    IF question CONTAINS "pm2.5" THEN
        response ← "PM2.5 represents fine particulate matter."

    ELSE IF question CONTAINS "pm10" THEN
        response ← "PM10 represents particulate matter."

    ELSE IF question CONTAINS "worst station" THEN
        response ← QUERY_DATABASE_FOR_HIGHEST_PM25()

    ELSE IF question CONTAINS "temperature" THEN
        response ← QUERY_DATABASE_FOR_TEMPERATURE()

    ELSE IF question CONTAINS "pollution" THEN
        response ← "Please specify the station or location."

    ELSE
        response ← "Sorry, I could not understand your question."
    END IF

    RETURN response
END
```

**Limitation:** A rule-based chatbot can answer only questions covered by its predefined rules. It cannot understand complex language, unfamiliar questions, or the full meaning of a conversation.

## A5.4 Alternative Machine Learning Approach

Instead of using predefined dictionaries and rules, machine learning models can be used to improve complaint analysis.

| Application | Proposed Machine Learning Alternative |
|---|---|
| Sentiment Analysis | Naive Bayes or Logistic Regression trained on labelled citizen complaints |
| Text Summarisation | Transformer-based summarisation models |
| Chatbot | Natural Language Processing (NLP) with an intent-classification model |

### Comparison

| Approach | Advantages | Limitations |
|---|---|---|
| Lexicon-based sentiment analysis | Simple, fast, and does not require training data | Limited understanding of context |
| Machine learning sentiment analysis | Can learn patterns from labelled examples | Requires training data and model evaluation |
| Frequency-based summarisation | Easy to implement and computationally inexpensive | May miss important context |
| Transformer-based summarisation | Can generate more meaningful summaries | Requires more computing resources |
| Rule-based chatbot | Easy to develop and control | Limited to predefined rules |
| NLP-based chatbot | Can understand a wider range of user questions | Requires training data and additional resources |

## Complexity Analysis

Let:
- N = Total number of words in the complaints.
- S = Total number of sentences.
- K = Number of keywords in the lexicon.

| Application | Time Complexity | Explanation |
|---|---|---|
| Lexicon-based sentiment analysis | O(N) average with efficient word lookup | Each word is checked against the sentiment dictionary. |
| Extractive summarisation | O(N + S log S) | Word frequencies are counted and sentence scores are sorted. |
| Rule-based chatbot | O(Q) for a fixed number of rules | Q represents the number of words in the user's question. |

## Conclusion

Sentiment analysis, extractive summarisation, and a rule-based chatbot can help convert large numbers of citizen complaints into useful information. These applications can identify public opinion, highlight common pollution problems, and answer frequently asked questions. Machine learning and NLP techniques can be introduced in the future to improve accuracy and understand more complex complaints.