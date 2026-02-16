#!/bin/bash
set -euo pipefail

Assignment=CSIMPLE_DEMOML1_Assignment.ipynb

SubmissionFile=submission.ipynb
SubmissionPath=/shared/submission
SharedDiskPath=/learner_workplace/$UserId/$CourseId/$LessonId

# copy synced files (exam image typically sync all files in lesson folder)
echo "Copy learner submission from $SharedDiskPath/$Assignment to $SubmissionPath/$SubmissionFile"
cp $SharedDiskPath/$Assignment $SubmissionPath/$SubmissionFile