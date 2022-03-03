#!/usr/bin/env python3
from numpy.random import default_rng
import argparse
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create reviewing assignments')
    parser.add_argument('--n', dest='n', type=int, default=3, required=False, help='number of reviews per submission')
    args = parser.parse_args()

    with open('reviewers.txt') as f:
        all_reviewers = f.read().splitlines()

    reviewer_counts = {}
    for r in all_reviewers:
        reviewer_counts[r] = 0
    
    with open('reviewer-counts.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            reviewer_counts[row[0]] = int(row[1])

    submissions = []
    submitters = {}
    with open('submissions.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            submission = row[0]
            submitter = row[1]
            submissions.append(submission)
            submitters[submission] = submitter

    rng = default_rng()

    # print CSV header
    print("--- Assignments ---")
    header = ['Submission'] + [f'R{i}' for i in range(1,args.n+1)]
    print(','.join(header))

    assignments = {}
    for s in submissions:
        # reviewer probabilities
        m = max(reviewer_counts.values())
        p = [m - v + 1 for v in reviewer_counts.values()]
        
        # if there's a conflict, set the prob to 0 so it's not assigned
        try:
            i = list(reviewer_counts.keys()).index(submitters[s])
            p[i] = 0
        except ValueError:
            pass

        # normalize to 1
        probs = [v / sum(p) for v in p]

        # pick reviewers
        reviewers = rng.choice(list(reviewer_counts.keys()), size=args.n, replace=False, p=probs)
        assignments[s] = reviewers
        print(f'{s},{",".join(assignments[s])}')

        for r in reviewers:
            reviewer_counts[r] = reviewer_counts.get(r) + 1

    reviewsPerPerson = {}
    for r in all_reviewers:
        reviewsPerPerson[r] = 0
    for a in assignments:
        reviewsPerPerson[assignments[a][0]] = reviewsPerPerson[assignments[a][0]] + 1
        reviewsPerPerson[assignments[a][1]] = reviewsPerPerson[assignments[a][1]] + 1

    print("--- Assignment Counts ---")
    print("Reviewer,Count")
    for r in all_reviewers:
        existing = reviewer_counts[r] - reviewsPerPerson[r]
        print(f'{r},{reviewer_counts[r]}')
