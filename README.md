# InterviewHandout

Question: The ETL team at MaestroQA manages several python jobs that run at various intervals. For various reasons, we may not want multiple of the same job running for a given client at any given time. For example, we may not want two workers to be running “sync job” for Test Company concurrently. Implement a locking system using the Database operations defined in mock_db.py, that can achieve this goal. We have provided a sample worker to use your solution, as well as a test script to verify the results of running the worker.

In worker.py, we have a simple python script that will write 'Maestro is the best......' to output.txt.
In starter_code.py, we run this worker 5 times on different threads.
In test_output.py we have a simple test to verify the correctness of the output. Basically, we want the text from above to be written several times, separated by 2 newlines each time. Note that this may be fewer than 5 times, as the workers are designed to crash with some probability. Be sure to remove the contents of output.txt after an unsuccessful run, as this could impact subsequent runs of the test script.

If you run the starter code, you will see that there is a concurrency issue, as multiple workers write to the file at the same time, interleaving the chunks of text. Using the fake database functions in mock_db.py, come up with a system to control the execution of workers so that the concurrency is handled correctly. You will only need to modify code outside the main function in starter_code.py. Furthermore, this should be accomplished by running the script once. That is, it should handle all failures appropriately and run all subsequent workers. A valid solution will write the previously mentioned output to output.txt by only running `python start_code.py`. It will also pass all assertions when running `python test_output.py`.
