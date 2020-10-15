# Boolean-Query-and-Inverted-Index-TFIDF
## In this project, I have a sample input text file consisting of Doc IDs and sentences. Based on this provided input text file, I built my own inverted index using the data. The index is stored as a Linked List in memory. Having built this index, I implemented a Document-at-a-time (DAAT) strategy to return Boolean query results(AND and OR).

## Input Dataset
Project_Dryrun_Corpus.txt is a tab-delimited file where each line is a document; the first field is
the document ID, and the second is a sentence. The two fields are separated by a tab.

## Follwing are the steps followed:

## Step 1: Build Your Own Inverted Index
Implemented a pipeline which takes as input the given corpus, and returns an inverted index.

1. Extracted the document ID and document from each line.

2. Performed a series of preprocessing on the document:
a. Converted document text to lowercase
b. Removed special characters. Only alphabets, numbers and whitespaces are present in the document.
c. Removeed excess whitespaces. There is only 1 white space between tokens, and no whitespace at the starting or ending of the document.
d. Tokenized the document into terms using white space tokenizer.
e. Removed stop words from the document.
f. Performed Porter’s stemming on the tokens.

Note: Simple python regex and inbuilt functions are used and not NLTK.
3. For each token, created a postings list. Postings list is stored as linked lists. Postings of each term are ordered by increasing document ids.

## Step 2: Boolean Query Processing
I implemented the following methods, and provided the results for a set of Boolean “AND” queries on the created index. Results are output as a JSON file in the required format. Given a user query, the first step is preprocessing the query using the same document preprocessing steps.

1. Below are the preprocessing steps that are performed on each user query
a. Converted query to lowercase
b. Removed special characters from query
c. Removed excess whitespaces. There is only 1 white space between query tokens, and no whitespace at the starting or ending of the query.
d. Tokenized the query into terms using white space tokenizer.
e. Removed stop words from the query.
f. Performed Porter’s stemming on the query tokens.

2. Get postings lists
This method retrieves the postings lists for each of the given query terms. Input of this method is a set of terms: term0, term1,..., termN. It outputs the
document ID wise sorted postings list for each term.

3. Document-at-a-time AND query
This function is used to implement multi-term boolean AND query on the index using document-at-a-time(DAAT) strategy. Input of this function is a set of query terms: term0, term1, …, termN. I implemented the MERGE algorithm, and returned a sorted list of document ids, along with the number of comparisons made.
NOTE: A comparison (for field “num_comparisons”) is counted whenever you compare two Document IDs during the union or intersection operation.

## Step 3: JSON output in the correct format
The results of the postings list and DAAT AND queries is combined in a
single python dictionary, and saved as a json file. 
