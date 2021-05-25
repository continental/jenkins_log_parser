# jenkins_log_parser

## What is it?

The jenkins_log_parser python package is a tool to create a readable log out of the raw log data from a jenkins job.
It creates a log file per stage and if the stage has parallel executions, it creates a directory named after the stage and 
puts the logs of the parallel executions there. So in the end you get a rather similar output like the blue ocean overview
of a job, just as files.

## How does it work?

The tool takes either a zip archive with the raw log data or a directory as positional argument. The readable logs are then put into the 
current directory or you specify a directory with the `-t` option.

The raw logdata is searched for the xml node files, which are parsed and then using the log-index and the raw log to put into multiple logfiles
and directory structure when parallel executions exist.

## Current state of development

First version, which works for our current usecase of processing archived raw log data from our build jobs. The probability is high that 
the tool also works for all pipeline jobs, but might have still bugs in special cases.

## Important note

Please keep in mind that the tests are missing the test input data and that you've to provide your own input data if you want to run the tests yourself.

## Bugfixes and contributions welcome!
