# "Concurrency and Parallelism"

Hi there! 😉

For today's homework, I'll apply concepts of multiprocessor and multithreaded programming to develop an efficient program for parallel searching of specific keywords in text files.

---

### Goals of the Assignment:

By completing this task, I will:
- Learn how to work with files in the context of multithreaded and multiprocessor programming.
- Understand how task distribution among threads or processes impacts performance and data processing efficiency.

This assignment will not only deepen my understanding of multithreaded and multiprocessor programming but also allow me to compare the effectiveness of both approaches. Moreover, I'll gain practical skills in using these concepts to optimize task distribution and resource utilization in applications.

---

### Technical Task Description:

I will develop a program that processes and analyzes text files in parallel to search for specified keywords. The program will have two versions:
- One using the **`threading`** module for multithreaded programming.
- Another using the **`multiprocessing`** module for multiprocessor programming.

---

### Step-by-Step Instructions:

#### **1. Multithreaded Approach (using `threading`):**
- Divide the list of files among multiple threads.
- Each thread will search for the specified keywords in its assigned set of files.
- Collect and output the search results from all threads.

#### **2. Multiprocessor Approach (using `multiprocessing`):**
- Divide the list of files among multiple processes.
- Each process will handle its subset of files, searching for the keywords.
- Use a data exchange mechanism (e.g., **`Queue`**) to collect and output the search results.
