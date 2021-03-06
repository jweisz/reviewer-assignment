# Reviewer Assignment

There are two scripts in this folder to be used for generating review assignments. These scripts are useful when making reviewing assignments for a conference. They were developed for the [IBM Spark Design Festival](https://medium.com/design-ibm/creating-a-spark-with-the-ibm-spark-design-festival-e4396c36ce2a).

## Prerequisites

Before running any Python scripts, please make sure you have installed the required dependencies by running the following command in the terminal. You only need to do this once.

```
pip install -r requirements.txt
```

## Initial reviewing assignments: `assign-without-priors.py`

This script should be used for generating review assignments when _no previous assignments have been made_. This is equivalent to the "Round 1" assignments made in 2021. This script reads in data from two files:

- a CSV file listing submission and submitter IDs in `submissions.csv` 
- a text file listing reviewers in `reviewers.txt` 

> This script takes one optional argument, `--n`, which determines how many assignments to make per submission. For example, to assign 4 reviewers per submission, run the command `python3 assign-without-priors.py --n 4`. If fancier logic is needed (e.g. one submission type needs 3 reviews but other submissions only need 2), then the script will need some modification.


### How to run

1. Ensure the `reviewers.txt` and `submissions.txt` files are in the same folder as the script. Samples are shown below.

2. Run the following command in the terminal.

```
$ python3 assign-without-priors.py
```

For the sample data listed below, it will produce the following output (note that this is random and will change each time you run it!).

```
--- Assignments ---
Submission,R1,R2,R3
Submission-1,Storyboard Vinaigrette,Johnny Appleyard,Harry Bovik
Submission-2,Justin Weisz,Storyboard Vinaigrette,Johnny Appleyard
Submission-3,Justin Weisz,Harry Bovik,Johnny Appleyard
Submission-4,Justin Weisz,Harry Bovik,Storyboard Vinaigrette
Submission-5,Johnny Appleyard,Justin Weisz,Storyboard Vinaigrette
Submission-6,Johnny Appleyard,Harry Bovik,Justin Weisz
--- Assignment Counts ---
Reviewer,Count
Justin Weisz,5
Harry Bovik,4
Storyboard Vinaigrette,4
Johnny Appleyard,5
```

### Sample `reviewers.txt`

This is a plain text file with a list of reviewer names or IDs.

```
Justin Weisz
Harry Bovik
Storyboard Vinaigrette
Johnny Appleyard
```

### Sample `submissions.csv`

This is a CSV file where the first field is a unique identifier for the submission and the second field is the name or ID of the person who submitted it.

> Note: This script currently assumes that submissions only have one author associated with them. In the future, the script should be extended to support multiple authors per submission.

```
Submission-1,Justin Weisz
Submission-2,Harry Bovik
Submission-3,Storyboard Vinaigrette
Submission-4,Johnny Appleyard
Submission-5,Null Void
Submission-6,Foo Bar
```


## Subsequent reviewing assignments: `assign-with-priors.py`

This script should be used for generating review assignments when _previous assignments have been made_. This is equivalent to the "Round 2" assignments made in 2021. This script reads in data from three files:

- a CSV file listing submission and submitter IDs in `submissions.csv` 
- a text file listing reviewers in `reviewers.txt` 
- a CSV that includes counts of how many reviews have already been assigned to each reviewer in `reviewer-counts.csv`

> This script takes one optional argument, `--n`, which determines how many assignments to make per submission. For example, to assign 4 reviewers per submission, run the command `python3 assign-without-priors.py --n 4`. If fancier logic is needed (e.g. feature presentations get 3 reviews but other submissions only get 2), then the script will need some modification. In 2021, the `assign.py` script looked at the submission ID to determine how many reviews the submission needed.

> Note that not all of the reviewers listed in `reviewers.txt` need to be included in `reviewer-counts.csv`. This is useful in case new reviewers have been added to the reviewing pool. In this case, their names only need to be added to `reviewers.txt`.

> Also note that you should **not** include any submissions in `submissions.csv` that have already been assigned reviewers. Otherwise, you will end up assigning reviewers to a submission that has already received reviewers!

### How to run

1. Ensure the `reviewer-counts.csv` and `submissions.csv` files are in the same folder as the script. Samples are shown below.

3. Run the following command in the terminal.

```
$ python3 assign-with-priors.py
```

For the sample data listed below, it will produce the following output (note that this is random and will change each time you run it!).

```
--- Assignments ---
Submission,R1,R2,R3
Submission-1,Storyboard Vinaigrette,Harry Bovik,Johnny Appleyard
Submission-2,Johnny Appleyard,Justin Weisz,Storyboard Vinaigrette
Submission-3,Justin Weisz,Johnny Appleyard,Harry Bovik
Submission-4,Justin Weisz,Storyboard Vinaigrette,Harry Bovik
Submission-5,Harry Bovik,Johnny Appleyard,Storyboard Vinaigrette
Submission-6,Johnny Appleyard,Harry Bovik,Justin Weisz
--- Assignment Counts ---
Reviewer,Count
Justin Weisz,6
Harry Bovik,6
Storyboard Vinaigrette,4
Johnny Appleyard,6
```

### Sample `reviewer-counts.csv`

This is a CSV file where the first field is a unique identifier for the reviewer and the second field is a number indicating how many submissions that revewer has already been assigned.

```
Justin Weisz,2
Harry Bovik,1
Storyboard Vinaigrette,0
Johnny Appleyard,1
```

### Sample `submissions.csv`

This is a CSV file where the first field is a unique identifier for the submission and the second field is the name or ID of the person who submitted it.

> Note: This script currently assumes that submissions only have one author associated with them. In the future, the script should be extended to support multiple authors per submission.

```
Submission-1,Justin Weisz
Submission-2,Harry Bovik
Submission-3,Storyboard Vinaigrette
Submission-4,Johnny Appleyard
Submission-5,Null Void
Submission-6,Foo Bar
```


## Final Guidance

The files `submissions.csv`, `reviewers.txt`, and `reviewer-counts.csv` should be considered "working files," rather than an authoratitive state. Thus, we recommend saving reviewer assignments in separate files, corresponding to the "round" in which the assignment was made. An example of how this might work is as follows:

- Make the initial assignments in Round 1. Keep the authoritative list of submissions in `submissions-round1.csv` and reviewers in `reviewers-round1.txt`. After making the assignments, save the assignment counts in `reviewer-r1counts.csv`.
- As new submissions come in or new reviewers are added to the pool, run a new round of reviewing using `assign-with-priors.py`. For example, to run Round 2, keep a list of new submissions (received after Round 1) in `submissions-round2.csv` and make a new master list of all reviewers (including any new ones) in `reviewers-round2.txt`. Then, copy the contents of these "round2" files to the filenames required by the script (i.e. `submissions.csv`, `reviewers.txt`, `reviewer-counts.csv`). Save the new assignment counts in `reviewers-r2counts.csv`, in case additional reviewing rounds are needed.
