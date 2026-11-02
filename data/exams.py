"""Earlier exams (IDATT2202 autumn 2023, 2024, 2025) with the course's suggested solutions.

Question text is transcribed from the exam PDFs. `answer` is the 0-based index of the
option marked correct in the official solution. `why` is a short explanation drawn from
the lecture slides; `solution` is the suggested solution (HTML).
"""
from html import escape


def code(src):
    return f"<pre><code>{escape(src.strip(chr(10)))}</code></pre>"


def mc(n, title, marks, prompt, options, answer, topics, why=""):
    if "<pre>" in prompt:
        text, _, rest = prompt.partition("<pre>")
        prompt_html = f"<p>{text}</p><pre>{rest}"
    else:
        prompt_html = f"<p>{prompt}</p>"
    return dict(n=n, title=title, marks=marks, type="mc", prompt=prompt_html,
                options=[escape(o) for o in options], answer=answer, topics=topics, why=why)


def open_q(n, title, marks, prompt, solution, topics, kind="open"):
    return dict(n=n, title=title, marks=marks, type=kind, prompt=prompt,
                solution=solution, topics=topics)


# ---------------------------------------------------------------- 2023

EXAM_2023 = dict(
    year=2023,
    date="29.11.2023",
    intro="Written exam, 29 November 2023, 15:00–18:00. 22 questions. No printed or hand-written support material; a specific basic calculator was allowed.",
    questions=[
        mc(1, "Application isolation", 2,
           "Application isolation is an important property of an operating system because:",
           ["Communication between applications is risky and unnecessary.",
            "Only one application can be executing instructions on the CPU at a given time.",
            "Limitations on physical memory necessitate limited communication between applications.",
            "An error in one application should not disrupt other applications."],
           3, ["introduction"],
           "As referee, the OS isolates users and applications from each other, so a fault in one cannot take down the others."),
        mc(2, "Availability", 2,
           "The property of availability of an operating system can be improved by:",
           ["Decreasing the mean-time-to-failure.",
            "Increasing the mean-time-to-failure or decreasing the mean-time-to-repair.",
            "Decreasing the mean-time-to-failure and increasing the mean-time-to-repair.",
            "Increasing the mean-time-to-repair."],
           1, ["introduction"],
           "Availability is the portion of time the system is working. It goes up if failures are rarer (longer MTTF) or repairs are quicker (shorter MTTR)."),
        mc(3, "Upcalls and virtual machines", 2,
           "An upcall from the host kernel to a virtual machine player can be seen as analogous to:",
           ["Interprocess communication via shared memory",
            "An interrupt from a hardware device to the CPU",
            "A processor exception in a guest operating system",
            "A system call from a virtual machine player to the host kernel"],
           1, ["kernel"],
           "An upcall is the user-level version of an interrupt: signal handlers correspond to the interrupt vector, and the signal stack to the interrupt stack."),
        mc(4, "End of the interrupt handler", 2,
           "The atomic operation at the end of the interrupt handler does all of the following except:",
           ["Restore the program counter", "Switch to kernel mode",
            "Restore the program stack", "Restore processor status and condition codes"],
           1, ["kernel"],
           "At the end of the handler the CPU atomically restores PC, stack and processor status word, and switches back to <em>user</em> mode."),
        mc(5, "Bottom half of the interrupt handler", 2,
           "Which of the following statements is not true regarding the bottom-half of the interrupt handler?",
           ["The bottom-half of the interrupt handler must not communicate with any kernel threads.",
            "Interrupts must be disabled while the bottom-half of the handler is running.",
            "The bottom-half must finish as quickly as posisble.",
            "The bottom-half must be non-blocking."],
           0, ["kernel"],
           "Interrupt handlers do the minimum and then wake up other threads to do any real work, so communicating with kernel threads is exactly what they do."),
        mc(6, "Trap", 2, "A trap is defined as:",
           ["A general term for an asynchronous transfer from kernel- to user-mode.",
            "A general term for a synchronous transfer from user- to kernel-mode.",
            "A general term for an asynchronous transfer from user- to kernel-mode.",
            "A general term for a synchronous transfer from kernel- to user-mode."],
           1, ["kernel"],
           "System calls and exceptions are caused by the instruction being executed (synchronous) and move the CPU from user to kernel mode."),
        mc(7, "Processor exceptions", 2,
           "All of the following are examples of processor exceptions except:",
           ["Attempt to execute a privileged instruction in user-mode", "Divide-by-zero",
            "Illegal memory reference", "Timer interrupt"],
           3, ["kernel"],
           "Exceptions are triggered by unexpected program behaviour. A timer interrupt comes from a hardware device, asynchronously."),
        mc(8, "Mode switch", 2,
           "Which of the following C-statements would trigger a mode switch (a transition from user mode to kernel mode) during program execution?",
           ["char buffer[5];", "c++;", "int x=5;", 'printf("me\\n");'],
           3, ["kernel", "programming-interface"],
           "printf eventually calls the write system call to output to the terminal. The others are plain user-mode instructions."),
        open_q(9, "Fork bomb", 10,
               "<ol><li>(5 pts) A forkbomb is a simple program where the parent forks itself in an endless loop. Write a forkbomb in C.</li>"
               "<li>(3 pts) What is the expected consequence of running this code?</li>"
               "<li>(2 pts) What can be done from an operating system's perspective to guard against a forkbomb?</li></ol>",
               code("void main()\n{\n    while(1) fork();\n}")
               + "<p>The main point is that <code>fork()</code> is called repeatedly without any <code>exec()</code>, so the parent code runs again in every child. This rapidly overwhelms the system (memory, process limits, and so on) unless a maximum user process limit is set, for example with <code>ulimit</code>.</p>"
               "<p>Naming <code>ulimit</code> is not required for full points. The point is that the OS can control the number of processes a user creates, because the fork bomb has to call <code>fork()</code>, which is a system call.</p>",
               ["programming-interface"]),
        open_q(10, "Stack and heap", 10,
               "<p>Consider a process address space for the following questions.</p><ol>"
               "<li>(3 pts) What is the stack used for?</li>"
               "<li>(2 pts) Write a snippet of C code that allocates an integer variable to the stack. Use not more than 2–3 lines of code.</li>"
               "<li>(3 pts) What is the heap used for?</li>"
               "<li>(2 pts) Write a snippet of C code that allocates a region of memory of size 256 bytes to the heap. Use not more than 2–3 lines of code.</li></ol>",
               "<ol><li>The stack is a LIFO data structure used for storing variables local to a function and recording the return address of function calls.</li>"
               "<li><code>void func() { int a; }</code></li>"
               "<li>The heap stores dynamically allocated memory where the data would not normally be appropriate to store on the stack, for example large buffers or arrays and structures.</li>"
               "<li><code>void *mem = malloc(256);</code></li></ol>",
               ["address-translation", "c-for-the-exam"]),
        open_q(11, "Sum with a thread", 10,
               "<p>Write a small C program using the pthread library that starts a new thread that calculates the sum of the integers 1 to 1000 and returns the result as the thread exit status. The main process waits for the thread to complete and prints the result. Pseudocode is acceptable but take care to use the correct pthread library function names. Use the following skeleton code as a starting point:</p>"
               + code("""#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Function to calculate the sum of integers in the specified range
void *calculateSum(void *args) {
    int sum = 0;
    // Fill in with your answer here
}

int main() {
    pthread_t thread;
    int result;
    // Fill in with your answer here
    printf("The sum of integers from 1 to 1000: %d\\n", result);
    return 0;
}"""),
               code("""#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

// Function to calculate the sum of integers in the specified range
void *calculateSum(void *args) {
    int sum = 0;
    for (int i = 1; i <= 1000; i++) {
        sum += i;
    }
    // Exit the thread and return the sum as the exit status
    pthread_exit((void *)sum);
}

int main() {
    pthread_t thread;
    int result;

    // Create a new thread
    if (pthread_create(&thread, NULL, calculateSum, NULL) != 0) {
        perror("Error creating thread");
        exit(EXIT_FAILURE);
    }
    // Wait for the thread to complete
    if (pthread_join(thread, (void **)&result) != 0) {
        perror("Error joining thread");
        exit(EXIT_FAILURE);
    }
    // Print the result
    printf("The sum of integers from 1 to 1000: %d\\n", result);
    return 0;
}"""),
               ["threads"]),
        open_q(12, "Synchronising the sum", 10,
               "<p>Consider the threaded program from the previous exercise. Assume the variable <code>sum</code> is global instead of local to <code>calculateSum</code>. Assume the main process starts 10 threads to distribute the calculation evenly (thread 1 sums from 1–100, thread 2 from 101–200, thread 3 from 201–300, and so on). Each thread must update the global variable <code>sum</code> with its result. How would you synchronise the code so that the sum is always correct? Specifically:</p><ol>"
               "<li>(5 pts) Describe the minimum critical section of the thread function <code>calculateSum</code>.</li>"
               "<li>(5 pts) What synchronisation mechanism would you use and where would you place it?</li></ol>"
               "<p>Your answer does not need to include C code or pseudocode, but you may add it if you wish.</p>",
               "<ol><li>The critical section only needs to be the part of the code that reads and updates the global variable <code>sum</code>. Store the thread's own work in a local variable, then add it to the global sum:"
               + code("localsum = sum(start..end)\n// begin critical section\nsum = sum + localsum\n// end critical section")
               + "</li><li>A simple mutex lock, around the critical section only:"
               + code("localsum = sum(start..end)\n// begin critical section\npthread_mutex_lock(&lock);\nsum = sum + localsum\n// end critical section\npthread_mutex_unlock(&lock);")
               + "</li></ol>",
               ["synchronisation"]),
        mc(13, "Thread abstraction", 2, "What is meant by a thread abstraction?",
           ["A process without a process control block in kernel memory",
            "Each threads runs on its own virtual processor with unpredictable and variable speed",
            "Each threads runs on its own virtual processor with predictable speed",
            "A single sequence of instructions has the illusion of running on multiple processors at the same time"],
           1, ["threads"],
           "The thread abstraction gives the illusion of an infinite number of processors, but threads execute with variable speed, so programs must work with any schedule."),
        mc(14, "Wrapping pthread_create", 2,
           "POSIX pthread_create() requires several parameters. Imagine writing a simple wrapper function for pthread_create() called start_thread(). This wrapper function can take only one parameter. What should that parameter be?",
           ["A pointer to an empty thread control block which will store the new thread context",
            "A pointer to a function which represents the schedulable task",
            "A pointer to a callback function to indicate the thread has finished",
            "The address of a variable which will store the thread handle"],
           1, ["threads"],
           "A thread is a separately schedulable task: <code>thread_create(thread, func, args)</code> runs <code>func(args)</code>. Without the function there is nothing to run."),
        mc(15, "False sharing", 2, "False sharing is:",
           ["Two or more cores share the same physical L3 cache",
            "The same memory location (word) is read from by one core and written to by another",
            "Two different memory locations are sequentially accessed by the same core",
            "An entire cache line is presumed shared across cores when in fact the cores are referencing unique addresses within that cache line"],
           3, ["deadlock"],
           "Cache coherence works on whole cache lines, so cores writing different variables in the same line still invalidate each other."),
        open_q(16, "Page replacement policies", 9,
               "<p>Consider a process with 3 pages of physical memory (3 slots). When all 3 pages are allocated and an unmapped page is referenced resulting in a page fault, a page replacement policy must choose a page to evict. Memory is initially empty. The process has the following reference sequence (each letter is a different page):</p>"
               "<p class=\"refstring\">A B A B C B D D D A E A E F A B C</p>"
               "<p>Fill in the number of page faults for MIN (optimal), FIFO and LRU.</p>",
               "<table><thead><tr><th>Policy</th><th class=\"num\">Faults</th><th>Final contents</th></tr></thead><tbody>"
               "<tr><td>MIN</td><td class=\"num\">7</td><td>A B C</td></tr>"
               "<tr><td>FIFO</td><td class=\"num\">9</td><td>F B C</td></tr>"
               "<tr><td>LRU</td><td class=\"num\">9</td><td>C B A</td></tr></tbody></table>"
               "<p>A dot marks a reference that caused a page fault:</p>"
               + code("MIN:  A. B. A B C. B D. D D A E. A E F. A B C.\nFIFO: A. B. A B C. B D. D D A. E. A E F. A B. C.\nLRU:  A. B. A B C. B D. D D A. E. A E F. A B. C."),
               ["virtual-memory"], kind="fill"),
        open_q(17, "Round robin", 12,
               "<p>Consider the round robin scheduler with the following tasks, all arriving at t = 0:</p>"
               "<table><thead><tr><th>Task</th><th class=\"num\">Length</th></tr></thead><tbody>"
               "<tr><td>1</td><td class=\"num\">20</td></tr><tr><td>2</td><td class=\"num\">1</td></tr>"
               "<tr><td>3</td><td class=\"num\">5</td></tr><tr><td>4</td><td class=\"num\">2</td></tr></tbody></table>"
               "<p><em>Response time</em> is the time spent waiting after arrival before a task starts executing. <em>Turnaround time</em> is the time to complete the task after arrival. <em>Wait time</em> is the total time spent in the ready queue. Find the average response, turnaround and wait time for a time quantum of 2 and of 5.</p>",
               "<table><thead><tr><th>Quantum</th><th class=\"num\">Response</th><th class=\"num\">Turnaround</th><th class=\"num\">Wait</th></tr></thead><tbody>"
               "<tr><td>2</td><td class=\"num\">2.5</td><td class=\"num\">13</td><td class=\"num\">6</td></tr>"
               "<tr><td>5</td><td class=\"num\">5.5</td><td class=\"num\">14.5</td><td class=\"num\">7.5</td></tr></tbody></table>"
               "<p>Quantum 2: the schedule is 1 (0–2), 2 (2–3, done), 3 (3–5), 4 (5–7, done), 1 (7–9), 3 (9–11), 1 (11–13), 3 (13–14, done), 1 (14–28, done). Tasks start at 0, 2, 3 and 5; they finish at 28, 3, 14 and 7. Wait time is turnaround minus length: 8, 2, 9, 5.</p>"
               "<p>Quantum 5: 1 (0–5), 2 (5–6, done), 3 (6–11, done), 4 (11–13, done), 1 (13–28, done). Tasks start at 0, 5, 6 and 11 and finish at 28, 6, 11 and 13.</p>"
               "<p>The course checked this with the OSTEP simulator: <code>./scheduler.py -p RR -l 20,1,5,2 -q 2 -c</code>. Answers within the rounding range (for example 2–3 for 2.5) were accepted.</p>",
               ["scheduling"], kind="fill"),
        mc(18, "FAT volume size", 2,
           "Entries in the FAT filesystem table are 32 bits (4 bits are reserved, leaving 28 bits for blocks on disk). Given a block size of 4096 bytes, what is the largest possible volume size?",
           ["2 TB", "4 TB", "4 GB", "1 TB"], 3, ["file-systems"],
           "2<sup>28</sup> blocks × 2<sup>12</sup> bytes = 2<sup>40</sup> bytes = 1 TB."),
        mc(19, "FFS inodes", 2,
           "The Fast File System (FFS) uses what data structure to store inodes at its highest level?",
           ["Inode FIFO queue", "Inode array", "Inode linked list", "Inode hash table"],
           1, ["file-systems"],
           "FFS keeps an inode table (an array indexed by inode number), analogous to the FAT table."),
        mc(20, "File descriptor", 2, "A file descriptor (or handle) is:",
           ["a memory buffer used to store file contents during a call to read()",
            "metadata describing file attributes such as file creation time, file owner, file size",
            "a reference identifier to a file from its containing directory",
            "a file reference identifier resulting in a call to open() or create()"],
           3, ["programming-interface", "file-systems"],
           "open returns a handle (file descriptor) that is used in later calls on the file."),
        open_q(21, "Buffer overflow on stack and heap", 9,
               "<p>Consider a programming error that leads to a buffer overflow where an attacker can control the data written into the buffer.</p><ol>"
               "<li>(3 pts) What consequences can this have when the buffer is stored on the stack?</li>"
               "<li>(3 pts) What consequences can this have when the buffer is stored on the heap?</li>"
               "<li>(3 pts) There are many measures to mitigate or reduce the impact of buffer overflows. Name one such measure and describe it briefly.</li></ol>",
               "<ol><li>Stack local variables can be corrupted or modified, and the return address can be controlled, giving the attacker control over program execution.</li>"
               "<li>Allocated data on the heap after the buffer may be corrupted or modified. There is no return address on the heap, but function pointers can be stored there, so execution could also be controlled by the attacker.</li>"
               "<li>Example mitigations:<ul>"
               "<li>Safe libc calls such as <code>fgets</code> instead of <code>gets</code></li>"
               "<li>Code review</li>"
               "<li>Compiler options like <code>-fstack-protector</code> (stack canaries) and <code>-pie</code> (position independent executable)</li>"
               "<li>Shadow stacks (not covered in the course, but a valid answer)</li>"
               "<li>ASLR, which makes it difficult to find valid addresses within the process address space</li>"
               "<li>Running the vulnerable program with reduced permissions or in a container or VM</li></ul></li></ol>",
               ["security"]),
        mc(22, "Asymmetric encryption", 2,
           "For two parties to communicate secretly using asymmetric encryption, it is necessary that:",
           ["party A exchanges their private key for the public key of party B",
            "both parties exchange private keys",
            "both parties have the same shared key",
            "both parties exchange public keys"],
           3, ["security"],
           "For secrecy you encrypt with the receiver's public key, and only the receiver's private key can decrypt. Private keys are never shared."),
    ],
)

# ---------------------------------------------------------------- 2024

EXAM_2024 = dict(
    year=2024,
    date="11.12.2024",
    intro="Written exam, 11 December 2024, 09:00–12:00. 27 questions. A simple calculator was permitted.",
    questions=[
        mc(1, "Reliability", 2,
           "Which of the following is a symptom of poor reliability in an operating system?",
           ["A fault in the system hardware causes unexpected behaviour.",
            "A bug in a user program causes that program to crash.",
            "A temporary network outage delays the application of an operating system patch.",
            "A memory leak in one program causes other programs to stop responding."],
           3, ["introduction"],
           "Reliability asks whether the system does what it was designed to do. An OS that lets one program's leak affect others has failed at isolation."),
        mc(2, "Virtualisation", 2,
           "Virtualisation in the context of an operating system is defined as:",
           ["Providing the illusion of resources that may not be physically present.",
            "Restricting user programs to executing only unprivileged instructions.",
            "A set of common services offered to user programs.",
            "The base set of instructions common to all instruction set architectures."],
           0, ["introduction"],
           "This is the OS as illusionist: each application appears to have the entire machine to itself."),
        mc(3, "The heap", 2, "When a process is running, the heap is used for:",
           ["Dynamic memory", "Static memory", "Program code", "Global variables"],
           0, ["address-translation"]),
        mc(4, "The stack", 2, "The stack is used for:",
           ["Local variables", "Dynamic memory", "Program code", "Static variables"],
           0, ["address-translation"]),
        mc(5, "Running the same program twice", 2,
           "In order to run multiple copies of the same program, the operating system:",
           ["Makes multiple copies of the program's instructions, static data, and stack, and reuses the first existing copy of the program's heap to save memory",
            "Makes multiple copies of the program's static data, heap, and stack, and reuses the first existing copy of the program's instructions to save memory",
            "Makes multiple copies of the program's instructions, static data, heap, and stack",
            "Creates a pointer to first existing copy of the program's instructions, static data, heap, and stack"],
           1, ["address-translation"],
           "The code segment is read-only and can be shared between processes. Data, heap and stack are written to, so each process needs its own."),
        mc(6, "Base and bound", 2,
           "All of the following are limitations to base and bound memory protection except:",
           ["No process isolation", "Memory fragmentation", "Non-expandable heap and stack", "No shared memory"],
           0, ["address-translation"],
           "Base and bound is safe: every access is checked against the bound. Its problems are that it cannot share memory or grow stack and heap."),
        mc(7, "ASLR", 2, "Address space layout randomisation is a technique used to:",
           ["Reduce the chance of successful attack by malicious code by randomising the base and bound addresses of a process",
            "Reduce the chance of successful attack by malicious code by randomising the location of a process's shared library segments",
            "Reduce the chance of successful attack by malicious code by randomising the location of a process's heap, stack, and text segment",
            "Isolate kernel and user process memory spaces"],
           2, ["security", "address-translation"]),
        mc(8, "Upcall", 2, "An upcall is:",
           ["A software interrupt", "Interprocess communication",
            "A request to the kernel from a user process to perform a privileged action",
            "A method used by the kernel to notify a user process of some event"],
           3, ["kernel"],
           "An upcall (a UNIX signal) is user-level event delivery: the kernel notifies a user process of something that needs to be handled right away."),
        mc(9, "Interrupts versus polling", 2,
           "Interrupts are favourable compared to polling (aka busy waiting) because:",
           ["Interrupts require less hardware.", "Interrupts are simpler to implement in software.",
            "Polling is strictly synchronous.", "Polling wastes CPU cycles."],
           3, ["kernel"],
           "With polling the kernel waits until I/O is done; with interrupts it can do other work in the meantime."),
        mc(10, "Kernel philosophy", 2,
           "\"What can be at user level, should be\" is a philosophy of which type of kernel design?",
           ["Monolithic kernel", "Macrokernel", "Hybrid kernel", "Microkernel"],
           3, ["kernel"]),
        mc(11, "Threads versus processes", 2,
           "A main benefit of using threads for concurrency over processes is:",
           ["Threads are faster when executing.",
            "Threads do not require any memory (stack, heap) during execution.",
            "Threads do not need to be attached to a process.",
            "Threads require less resources and overhead to create."],
           3, ["threads"],
           "A thread shares the address space of its process, so creating one only needs a thread control block and a stack."),
        mc(12, "Yielding", 2, "What is meant by a thread \"yielding\"?",
           ["The thread gives up the CPU so that another thread can be scheduled.",
            "The thread is created in a paused state.", "The thread terminates abnormally.",
            "The thread requests to exit."],
           0, ["threads"],
           "<code>thread_yield()</code> relinquishes the processor voluntarily."),
        mc(13, "Memory barrier", 2, "A memory barrier is:",
           ["a memory reference that can never be satisfied.",
            "an instruction forcing reordering of memory accesses across that barrier.",
            "an instruction preventing reordering memory accesses across that barrier.",
            "a memory reference that must always be satisfied."],
           2, ["synchronisation"],
           "All operations before the barrier complete before it returns, and no operation after it starts until it returns."),
        mc(14, "Multicore synchronisation", 2,
           "A synchronisation problem unique to multicore systems as opposed to unicore systems is:",
           ["Lack of atomic instructions", "Lock contention can be much greater",
            "Releasing a spinlock cannot be guaranteed", "Lack of support for memory barriers"],
           1, ["deadlock"],
           "With several cores, many threads can try to take the same lock at the same instant, and the lock value pings between caches."),
        mc(15, "False sharing", 2, "False sharing is:",
           ["The same memory location (word) is read from by one core and written to by another",
            "Two or more cores share the same physical L3 cache",
            "Two different memory locations are sequentially accessed by the same core",
            "An entire cache line is presumed shared across cores when in fact the cores are referencing unique addresses within that cache line"],
           3, ["deadlock"]),
        mc(16, "RCU writers", 2,
           "The read-copy-update (RCU) lock allows how many writes to happen concurrently?",
           ["1", "3", "Unlimited", "2"], 0, ["deadlock"],
           "Readers proceed without a lock, but the writer acquires a write lock, so only one write happens at a time."),
        mc(17, "Deadlock conditions", 2,
           "Which of the following is NOT a necessary condition for a deadlock?",
           ["Preemption", "Hold while waiting", "Circular waiting", "Limited resources"],
           0, ["deadlock"],
           "The condition is <em>no</em> preemption. If resources can be taken away, the deadlock can be broken."),
        mc(18, "Segmentation", 2, "The basic idea of memory segmentation is:",
           ["A single pair of base and bounds registers is given to each process.",
            "Virtual and physical memory is divided in to small pages, which must be located contiguously (all in order) in physical memory.",
            "Each process is given an array of base and bound registers, one pair for each memory segment.",
            "Virtual and physical memory is divided in to small pages, which can be located in any order in physical memory."],
           2, ["address-translation"]),
        mc(19, "Write permission", 2,
           "Which type of memory segment should not have the write access flag set in the segment table?",
           ["Stack segment", "Data segment (e.g., global and static variables)", "Code segment", "Heap segment"],
           2, ["address-translation"],
           "Segmentation can protect the code segment from being overwritten."),
        mc(20, "Salting", 2, "Salting with random data before hashing a password helps against:",
           ["weak passwords", "rainbow tables (precomputed password hash tables)",
            "password re-use by users",
            "system administrators gaining access to the plaintext password"],
           1, ["security"],
           "Hashing the password with a random salt foils a precomputed password table lookup."),
        open_q(21, "Process abstraction", 10,
               "<p>Consider the following C source code. Describe what the output will be. Will the output always be the same? If yes, state why. If not, state why not.</p>"
               + code("""#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main()
{
    for(int i=0; i<5; i++)
    {
        int f = fork();
        if (f > 0)
        {
            printf("Process %d checking in\\n", i);
            exit(i);
        }
    }
    wait(NULL);
}""")
               + "<div class=\"note\"><p><strong>Correction from the course:</strong> the question should have read <code>if (f == 0)</code>, not <code>if (f &gt; 0)</code>. The code as written is still worth studying. Compile and run it, draw the process tree, and use <code>strace -f ./fork</code> to follow it. Who enters the <code>if</code>, how many unique parents fork a child, and which process finally calls <code>wait(NULL)</code>?</p></div>",
               "<p>The parent forks 5 children, each of which prints <code>Process %d checking in</code> with the loop variable <code>i</code>. The first forked child prints <code>Process 0 checking in</code>, and so on while <code>i &lt; 5</code>. The parent does not print anything; it waits for the children before exiting.</p>"
               + code("Process 0 checking in\nProcess 1 checking in\nProcess 3 checking in\nProcess 2 checking in\nProcess 4 checking in")
               + "<p>Because the kernel schedules processes unpredictably, the output will not always be the same between runs.</p>",
               ["programming-interface"]),
        open_q(22, "Writing numbers to a file", 10,
               "<p>Write a C program that creates a new file called <code>numbers.txt</code> and writes the numbers 1 through 30, each on its own line, into the file. (The exam attached man pages for the libc functions.)</p>",
               "<p>Many answers are possible. The main points are that the correct calls are used (<code>fopen</code>, <code>fwrite</code>/<code>fprintf</code>, <code>fclose</code>). Partial points were given for writing to stdout with <code>printf</code> instead, and for having the general structure. Pseudocode was acceptable.</p>"
               + code("""#include <stdio.h>
#include <stdlib.h>

// Suggested solution using fprintf
int main()
{
    FILE *f = fopen("numbers.txt", "w");
    for(int i=1; i<=30; i++)
    {
        fprintf(f, "%d\\n", i);
    }
    fclose(f);
}"""),
               ["c-for-the-exam", "programming-interface"]),
        open_q(23, "Threading: fill in the blanks", 16,
               "<p>The following C program creates 5 threads and waits for them to finish before printing their exit statuses. Fill in the blanks with the correct keywords.</p>"
               "<p>Keywords to choose from: <code>input</code>, <code>pthread</code>, <code>main</code>, <code>join</code>, <code>param</code>, <code>stdin</code>, <code>go</code>, <code>execve</code>, <code>stdio.h</code>, <code>NUMTHREADS</code>, <code>create</code>, <code>exit</code>, <code>fork</code>, <code>libc.h</code>, <code>wait</code>.</p>"
               + code("""#include <____>
#include <____.h>
#define NUMTHREADS 5
pthread_t threads[NUMTHREADS];

void *go(void *param)
{
    printf("Thread %d says hello\\n", (int*) ____);
    pthread_____((int*)param);
}

int main()
{
    for(int i=0; i<____; i++)
    {
        pthread_____(&threads[i], NULL, ____, (void*)i);
    }
    for(int i=0; i<NUMTHREADS; i++)
    {
        void* retval;
        pthread_____(threads[i], &retval);
        printf("main: thread %d returned %d\\n", i, retval);
    }
}"""),
               code("""#include <stdio.h>
#include <pthread.h>
#define NUMTHREADS 5
pthread_t threads[NUMTHREADS];

void *go(void *param)
{
    printf("Thread %d says hello\\n", (int*) param);
    pthread_exit((int*)param);
}

int main()
{
    for(int i=0; i<NUMTHREADS; i++)
    {
        pthread_create(&threads[i], NULL, go, (void*)i);
    }
    for(int i=0; i<NUMTHREADS; i++)
    {
        void* retval;
        pthread_join(threads[i], &retval);
        printf("main: thread %d returned %d\\n", i, retval);
    }
}"""),
               ["threads"], kind="fill"),
        open_q(24, "Two-level address translation", 9,
               "<p>Virtual address format: <strong>8-bit page number | 8-bit page number | 16-bit offset</strong>. Convert the virtual addresses to physical addresses using the two-level page table below, or write <em>invalid</em>.</p>"
               "<table><thead><tr><th>Top level</th><th>Table A</th><th>Table B</th></tr></thead><tbody>"
               "<tr><td>0 → Page table A</td><td>0 → 0xFEAD</td><td>0 → 0xBEEF</td></tr>"
               "<tr><td>1 → invalid</td><td>1 → 0xFEED</td><td>1 → 0xFEFE</td></tr>"
               "<tr><td>2 → invalid</td><td>2 → 0xFEEF</td><td>2 → 0x0000</td></tr>"
               "<tr><td>3 → Page table B</td><td>3 → 0xCACA</td><td>3 → 0xAEFF</td></tr>"
               "<tr><td>rest invalid</td><td>rest invalid</td><td>4 → 0x0002</td></tr>"
               "<tr><td></td><td></td><td>5 → 0xFFAE</td></tr></tbody></table>"
               "<ol><li>0x0003AB05</li><li>0x03008080</li><li>0x01044140</li></ol>",
               "<ol><li><strong>0xCACAAB05</strong>. Top index 0x00 → table A; second index 0x03 → frame 0xCACA; offset 0xAB05 passes through.</li>"
               "<li><strong>0xBEEF8080</strong>. Top index 0x03 → table B; second index 0x00 → 0xBEEF; offset 0x8080.</li>"
               "<li><strong>invalid</strong>. Top index 0x01 is invalid.</li></ol>",
               ["address-translation"], kind="fill"),
        open_q(25, "FFS first-fit allocation", 7,
               "<p>An FFS implementation with first-fit allocation accepts these commands: <code>file /a &lt;blocks&gt;</code> creates a file, <code>dir /a</code> creates a directory, <code>delete /a</code> deletes a file or directory (recursively). In the layouts below, each row is a block group: first the inodes, then the data blocks. For example <code>file /a 3</code> gives:</p>"
               + code("0 /a-------- /aaa------ ---------- ----------\n1 ---------- ---------- ---------- ----------")
               + "<p>1. Which three commands give this layout?</p>"
               + code("0 /ab------- /aaaabb--- ---------- ----------\n1 c--------- c--------- ---------- ----------")
               + "<p>2. Which two commands then give this?</p>"
               + code("0 /abc------ /aaaabbccc ---------- ----------\n1 ---------- ---------- ---------- ----------")
               + "<p>3. Which two commands then give this?</p>"
               + code("0 /abc------ /aaaabbccc ---------- ----------\n1 dE-------- dEEEEEEEEE EEEEEEEEEE EEEEEEEEEE"),
               "<ol><li><code>file /a 4</code>, <code>file /b 2</code>, <code>dir /c</code>. The directory goes into a new block group, which is how FFS spreads subdirectories.</li>"
               "<li><code>delete /c</code>, then <code>file /c 3</code>. The file is in the root directory, so it goes into group 0 with the other files of /.</li>"
               "<li><code>dir /d</code>, then <code>file /d/E 29</code>. The directory starts a new group, and the file inside it is placed in the same group as its directory.</li></ol>"
               "<p>The original exam had a typo in the last layout, so this part was marked manually.</p>",
               ["file-systems"], kind="fill"),
        open_q(26, "Round robin time quantum", 4,
               "<p>Discuss the tradeoffs between a short and long time quantum for a scheduling algorithm like round robin (RR).</p>",
               "<p>A short time quantum gives high responsiveness. If it is too short, each job progresses slowly and there is high overhead from frequent context switching (user → kernel and kernel → user) by the scheduler.</p>"
               "<p>A long time quantum means low responsiveness, but each process gets more work done per scheduled CPU time.</p>",
               ["scheduling"]),
        open_q(27, "FAT or NTFS for a camera", 4,
               "<p>State the advantages and disadvantages of a FAT filesystem versus an NTFS filesystem for an embedded device such as a digital camera. Which is more appropriate for this application area?</p>",
               "<p>FAT is simple to implement and suits embedded systems where memory and processing power are restricted. A camera does not need the features of a more powerful file system such as NTFS or FFS: ownership, permissions and other metadata.</p>"
               "<p><strong>FAT advantages:</strong> simple linked-list structure, easy to find free blocks, simple implementation. <strong>FAT disadvantages:</strong> random access is slow because the linked list must be traversed, but a camera mostly appends new files. The 4 GB file size limit can be a problem for HD video (exFAT can be mentioned but is not needed). No journalling, which can lead to data loss. Fragmentation over time.</p>"
               "<p><strong>NTFS</strong> is more flexible with file size, metadata and permissions, supports journalling and addresses fragmentation by design. For an embedded device, the overhead of unused features makes it generally unsuitable. FAT is the more appropriate choice.</p>",
               ["file-systems"]),
    ],
)

# ---------------------------------------------------------------- 2025

EXAM_2025 = dict(
    year=2025,
    date="10.12.2025",
    intro="Written exam, 10 December 2025, 09:00–12:00. 27 questions. No printed or hand-written support material.",
    questions=[
        mc(1, "Temporal locality", 2, "Temporal locality refers to:",
           ["Memory addresses that have been accessed recently are likely to be used in the near future",
            "Memory addresses nearby those that have been recently accessed are likely to be accessed in the near future",
            "Memory addresses that have been accessed recently are unlikely to be used in the near future",
            "Memory addresses nearby those that have been recently accessed are unlikely to be accessed in the near future"],
           0, ["virtual-memory"],
           "Temporal locality: the same locations are referenced again (instructions in a loop). The second option describes spatial locality."),
        mc(2, "Permissions in FFS", 2, "A typical Unix filesystem like FFS has permissions:",
           ["Globally (one permission for the entire filesystem tree)",
            "Per directory where all files inherit from their parent directory",
            "Per hard link", "Per file"],
           3, ["file-systems"],
           "Permissions are part of the file's metadata in its inode, alongside owner and access times."),
        mc(3, "Interrupt", 2, "An interrupt is defined as:",
           ["An asynchronous signal to the processor that an external event has occurred.",
            "A hardware event caused by the execution of a user program instruction.",
            "A hardware event caused by the execution of an exception handler instruction.",
            "An asynchronous signal to the kernel that an external event has occurred."],
           0, ["kernel"]),
        mc(4, "NTFS filenames", 2, "In NTFS, the filename of a file is stored in:",
           ["The file's MFT record", "The file's parent directory MFT record",
            "The file allocation table (FAT)", "The inode array"],
           0, ["file-systems"]),
        mc(5, "Semaphore as a lock", 2, "A semaphore can emulate a lock under what condition?",
           ["When the semaphore is initialised to 3.", "When the semaphore is initialised to 1.",
            "When the semaphore is initialised to 2.", "When the semaphore is initialised to 0."],
           1, ["synchronisation"],
           "With value 1, the first P() takes it to 0 and any further P() waits until V() is called, so only one thread is inside at a time."),
        mc(6, "TLB", 2, "The main purpose of a translation lookaside buffer (TLB) is to:",
           ["Map processes to specific cores in multicore systems so that context switching is faster.",
            "Allow many processes to access common shared pages by storing all shared pages in a separate address translation table.",
            "Cache disk blocks in memory for faster access by processes performing I/O.",
            "Caching the addresses to recently accessed pages, thereby avoiding walking the page tables."],
           3, ["address-translation"]),
        mc(7, "Yielding", 2, "What is meant by a thread \"yielding\"?",
           ["The thread gives up the CPU so that another thread can be scheduled.",
            "The thread terminates abnormally.", "The thread requests to exit.",
            "The thread is created in a paused state."],
           0, ["threads"]),
        mc(8, "Running a new program", 2, "When a new program is run, the role of the operating system is:",
           ["Ensure that the program code is small enough to fit into physical memory",
            "Copy the program code into memory if it doesn't already exist",
            "Compile the program into machine code",
            "Ensure that no other copies of the program are already running"],
           1, ["programming-interface"]),
        mc(9, "Thread abstraction", 2, "What is meant by a thread abstraction?",
           ["Each threads runs on its own virtual processor with predictable speed",
            "A single sequence of instructions has the illusion of running on multiple processors at the same time",
            "Each threads runs on its own virtual processor with unpredictable and variable speed",
            "A process without a process control block in kernel memory"],
           2, ["threads"]),
        mc(10, "Trap", 2, "A trap is defined as:",
           ["A general term for an asynchronous transfer from user- to kernel-mode.",
            "A general term for a synchronous transfer from kernel- to user-mode.",
            "A general term for an asynchronous transfer from kernel- to user-mode.",
            "A general term for a synchronous transfer from user- to kernel-mode."],
           3, ["kernel"]),
        mc(11, "Least privilege", 2, "What is not an example of the principle of least privilege?",
           ["Users should have exactly the permissions required to complete tasks and not more.",
            "Run server daemons (e.g., webservers) as root user.",
            "Minimise the amount of code running in kernel space.",
            "Reduce the number of programs with the set-UID root flag set to absolute minimum."],
           1, ["security"]),
        mc(12, "Round robin with equal jobs", 2,
           "In a round robin scheduler where all jobs have equal length, which performance metric is most negatively affected compared to first-in-first-out (FIFO) scheduling?",
           ["CPU utilisation (percentage of time CPU is busy)",
            "Fairness (degree to which jobs share CPU time equally)",
            "Throughput (number of jobs completed per unit time)",
            "Mean response time (average time until a job completes)"],
           3, ["scheduling"],
           "If tasks are equal in size, round robin has very poor average response time: every job finishes near the end."),
        mc(13, "Inode fields", 2, "Which one of the following fields is not contained in an inode?",
           ["Group", "Set-uid", "User (owner)", "Parent directory"],
           3, ["file-systems"],
           "The inode holds metadata such as owner, permissions and access times. The name-to-inode mapping lives in the directory, not the inode."),
        mc(14, "Windows and Linux process creation", 2,
           "What is the main difference between creating a new process in the Windows and Linux kernels?",
           ["The Windows kernel stores the process control block in user space.",
            "exec() is not necessary when starting a new program that has a different text segment from the parent process in the Linux kernel.",
            "fork() on Linux copies the parent process image into the child (new) process image. CreateProcess on the other hand reads the executable process image from disk.",
            "The only difference is the name of the system call: fork() vs CreateProcess()."],
           2, ["programming-interface"]),
        mc(15, "Write-through cache", 2, "A write-through cache is one that:",
           ["Is actually an illusion - all updates go directly to main memory",
            "Updates to the cache location are sent onward through the memory hierarchy only when they evicted from the cache",
            "Updates to the cache location are immediately sent onward through the memory hierarchy",
            "Is actually an illusion - all updates go directly to the hard disk"],
           2, ["virtual-memory"],
           "Write-through sends changes immediately to the next level. Write-back (the second option) keeps them until the block is replaced."),
        mc(16, "Cooperative thread", 2, "A cooperative thread is a thread that:",
           ["Works together with other threads on shared data.", "Yields to let other threads run.",
            "Must be interrupted to give up the CPU.", "Is scheduled by the kernel."],
           1, ["threads"]),
        mc(17, "Interrupt stack", 2,
           "A separate interrupt stack is required for handling interrupts because:",
           ["Why not? Memory is cheap!",
            "The handler may require more space than is available on the user process stack.",
            "The state of a user process stack cannot be trusted by the kernel.",
            "There is only one stack per CPU."],
           2, ["kernel"]),
        mc(18, "Longer time quantum", 1,
           "Increasing the length of the time quantum has which effect on round robin scheduling?",
           ["Overhead is increased", "Job length is increased", "Job length is decreased", "Overhead is decreased"],
           3, ["scheduling"],
           "Fewer time slices means fewer context switches."),
        mc(19, "Insecure function", 2,
           "Consider the C code below. What is the insecure function call?"
           + code('#include <stdio.h>\nint main()\n{\n    char buff[32];\n    gets(buff);\n    printf("%s", buff);\n}'),
           ["printf", "main", "buff", "gets"],
           3, ["security"],
           "<code>gets</code> copies input into the buffer without checking its length."),
        mc(20, "wait()", 2, "wait(), called by a parent process, is used to:",
           ["Block until the specified child process has exited.", "Block until the parent process exits.",
            "Sleep for the specified number of seconds.", "Block until the parent's call to fork() returns."],
           0, ["programming-interface"]),
        open_q(21, "Order of output with condition variables", 8,
               "<p>Study the following threaded and synchronised C code. The <code>usleep(1000)</code> ensures that thread B is always scheduled first. Put the printed lines in the correct order: Alpha 1, Alpha 2, Alpha 3, Beta 1, Beta 2, Beta 3, Ready A updated, Ready B updated.</p>"
               + code("""pthread_mutex_t lock_A = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_A = PTHREAD_COND_INITIALIZER;
int ready_A = 0;
pthread_mutex_t lock_B = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t cond_B = PTHREAD_COND_INITIALIZER;
int ready_B = 0;

void *thread_A(void *arg) {
    printf("Alpha 1\\n");
    pthread_mutex_lock(&lock_A);
    ready_A = 1;
    printf("Ready A updated\\n");
    printf("Alpha 2\\n");
    pthread_cond_signal(&cond_A);
    pthread_mutex_unlock(&lock_A);

    pthread_mutex_lock(&lock_B);
    while (!ready_B) {
        pthread_cond_wait(&cond_B, &lock_B);
    }
    pthread_mutex_unlock(&lock_B);
    printf("Alpha 3\\n");
    return NULL;
}

void *thread_B(void *arg) {
    pthread_mutex_lock(&lock_A);
    while (!ready_A) {
        printf("Beta 1\\n");
        pthread_cond_wait(&cond_A, &lock_A);
    }
    printf("Beta 2\\n");
    pthread_mutex_unlock(&lock_A);
    printf("Beta 3\\n");

    pthread_mutex_lock(&lock_B);
    ready_B = 1;
    printf("Ready B updated\\n");
    pthread_cond_signal(&cond_B);
    pthread_mutex_unlock(&lock_B);
    return NULL;
}

int main() {
    pthread_t tA, tB;
    pthread_create(&tB, NULL, thread_B, NULL);
    usleep(1000);
    pthread_create(&tA, NULL, thread_A, NULL);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    return 0;
}"""),
               code("Beta 1\nAlpha 1\nReady A updated\nAlpha 2\nBeta 2\nBeta 3\nReady B updated\nAlpha 3")
               + "<p>B runs first, finds <code>ready_A == 0</code>, prints <em>Beta 1</em> and waits (releasing lock_A). A prints <em>Alpha 1</em>, sets <code>ready_A</code>, prints <em>Ready A updated</em> and <em>Alpha 2</em>, then signals. A then waits for <code>ready_B</code>. B wakes, prints <em>Beta 2</em> and <em>Beta 3</em>, sets <code>ready_B</code>, prints <em>Ready B updated</em> and signals. Finally A prints <em>Alpha 3</em>.</p>",
               ["synchronisation"], kind="fill"),
        open_q(22, "A simple shell: fill in the blanks", 10,
               "<p>Fill in the blanks so that the simple shell compiles and works. Keywords: <code>char</code>, <code>execvp</code>, <code>return</code>, <code>args</code>, <code>0</code>, <code>wait</code>, <code>while</code>, <code>printf</code>, <code>fork</code>, <code>waitpid</code>.</p>"
               + code("""#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/____.h>
#define MAX_LINE 80
#define TOKEN_DELIM " \\t\\r\\n\\a"

void parse_command(char *line, char **args) {
    char *token;
    int i = 0;
    token = strtok(line, TOKEN_DELIM);
    while (token != NULL) {
        args[i++] = token;
        token = strtok(NULL, TOKEN_DELIM);
    }
    args[i] = NULL;
}

int main(void) {
    ____ line[MAX_LINE];
    char *args[MAX_LINE/2 + 1];
    int status;
    pid_t pid;
    ____ (1) {
        ____("simple_shell> ");
        if (!fgets(line, MAX_LINE, stdin))
            break;
        parse_command(line, args);
        if (____[0] == NULL)
            continue;
        pid = ____();
        if (pid < 0) {
            perror("Error");
            exit(EXIT_FAILURE);
        } else if (pid == ____) {
            if (____(args[0], args) == -1) {
                perror("Error");
                exit(EXIT_FAILURE);
            }
        } else {
            ____(pid, &status, 0);
        }
    }
    ____ 0;
}"""),
               "<p>In order: <code>wait</code> (<code>sys/wait.h</code>), <code>char</code>, <code>while</code>, <code>printf</code>, <code>args</code>, <code>fork</code>, <code>0</code>, <code>execvp</code>, <code>waitpid</code>, <code>return</code>.</p>"
               "<p>This is the fork–exec–wait pattern: the child (where <code>fork</code> returns 0) replaces itself with the command using <code>execvp</code>, and the parent waits for that child with <code>waitpid</code>.</p>",
               ["programming-interface"], kind="fill"),
        open_q(23, "Command-line arguments", 10,
               "<p>Write a C program that takes (1) a numeric argument N and (2) a string argument from the command line and prints the string N times to standard output.</p>"
               + code('$ ./myprog 3 "String"\nStringStringString'),
               "<p>Marking: correct command-line argument handling (4 pts), conversion of the numeric argument to an integer (2 pts), correct output repetition without extra spaces or newlines (4 pts). Error checking was not required; input can be assumed valid.</p>"
               + code("""#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    int N = atoi(argv[1]);
    for (int i=0; i<N; i++)
    {
        printf(argv[2]);
    }
}"""),
               ["c-for-the-exam"]),
        open_q(24, "Paging", 12,
               "<p>A system uses paging with a page size of <strong>256 bytes</strong> and a <strong>20-bit virtual address space</strong>. Part of the page table (VPN = virtual page number, PFN = page frame number, PB = present bit; entries not shown have PB 0):</p>"
               + code("""VPN  PFN             PB
15   0110 0000 0110  1
14   0001 0110 0000  1
13   0111 0111 0111  1
12   0101 1011 1011  1
11   0100 0000 1110  1
10   0000 0000 0000  0
 9   0001 0010 1010  1
 8   0110 0001 1111  1
 7   0110 0000 1011  1
 6   0100 0000 0001  1
 5   0010 1110 1000  1
 4   0000 0000 0000  0""")
               + "<ol><li>How many entries does the page table have?</li>"
               "<li>How many bits is the page offset?</li>"
               "<li>What is the size of the virtual address space?</li>"
               "<li>What does the virtual address <code>0000 0000 1110 1010 1011</code> translate to?</li>"
               "<li>Where is the page table located?</li>"
               "<li>With a page size of 16 KB and a 36-bit virtual address space using two-level paging, how many entries are in each page table?</li></ol>",
               "<ol><li><strong>4096</strong>. 256-byte pages need an 8-bit offset, leaving 20 − 8 = 12 bits of page number: 2<sup>12</sup> = 4096.</li>"
               "<li><strong>8 bits</strong> (2<sup>8</sup> = 256).</li>"
               "<li><strong>1 MB</strong> (2<sup>20</sup> bytes).</li>"
               "<li><strong>0001 0110 0000 1010 1011</strong>. The upper 12 bits <code>0000 0000 1110</code> are VPN 14, which maps to PFN <code>0001 0110 0000</code> (present). The 8-bit offset <code>1010 1011</code> passes through unchanged.</li>"
               "<li><strong>RAM</strong> (internal memory).</li>"
               "<li><strong>2048</strong>. A 16 KB page gives a 14-bit offset, leaving 36 − 14 = 22 bits of page number, split over two levels: 11 bits each, 2<sup>11</sup> = 2048.</li></ol>",
               ["address-translation"], kind="fill"),
        open_q(25, "Page replacement policies", 9,
               "<p>A process has 3 pages of physical memory, initially empty. Count the page faults for MIN (optimal), FIFO and LRU with the reference sequence:</p>"
               "<p class=\"refstring\">A B C A D B E F A C D</p>",
               "<table><thead><tr><th>Policy</th><th class=\"num\">Faults</th></tr></thead><tbody>"
               "<tr><td>MIN</td><td class=\"num\">7</td></tr><tr><td>FIFO</td><td class=\"num\">9</td></tr><tr><td>LRU</td><td class=\"num\">10</td></tr></tbody></table>"
               "<p><strong>MIN:</strong> A, B, C fault. A hits. D evicts C (used furthest ahead). B hits. E evicts B (never used again). F evicts E. A hits. C faults (evict A or F, neither is needed). D hits. 7 faults.</p>"
               "<p><strong>FIFO:</strong> A, B, C fault, A hits, then D evicts A, B hits, E evicts B, F evicts C, A evicts D, C evicts E, D evicts F. 9 faults.</p>"
               "<p><strong>LRU:</strong> A, B, C fault, A hits, then every remaining reference misses: D evicts B, B evicts C, E evicts A, F evicts D, A evicts B, C evicts E, D evicts F. 10 faults.</p>",
               ["virtual-memory"], kind="fill"),
        open_q(26, "False sharing", 5,
               "<p>Explain the concept of false sharing in the context of multicore systems (2 pts). Why does it occur (2 pts), and what impact does it have on performance (1 pt)?</p>",
               "<p>False sharing occurs when threads on different cores modify variables that sit on the same cache line, even though the variables are logically independent. Because cache coherence works at the granularity of a cache line (typically 64 bytes), any update to one variable invalidates the whole line in the other cores' caches. (2 pts)</p>"
               "<p>Cache lines are the smallest unit of coherence. If two threads update different variables on one line, the hardware treats it as a conflict and the line is repeatedly invalidated and reloaded. (2 pts)</p>"
               "<p>It increases memory latency and reduces scalability, because cores spend their time maintaining coherence instead of doing useful work. (1 pt)</p>",
               ["deadlock"]),
        open_q(27, "Zero-on-reference and copy-on-write", 6,
               "<ol><li>What is zero-on-reference and why is it useful? (3 pts)</li>"
               "<li>What is copy-on-write in the context of a process fork and why is it useful? (3 pts)</li></ol>",
               "<ol><li><strong>Zero-on-reference</strong>: memory pages are not physically allocated or zeroed until the process first accesses them. On the first access a page fault occurs, and the OS allocates a page and fills it with zeros. It avoids pre-zeroing large regions that may never be used, saving time and memory.</li>"
               "<li><strong>Copy-on-write</strong>: after a fork, parent and child share the same physical pages, marked read-only. If either writes to a page, the OS traps and makes a private copy for that process. It avoids duplicating every page during fork, improving performance and saving memory.</li></ol>",
               ["virtual-memory", "address-translation"]),
    ],
)

EXAMS = [EXAM_2023, EXAM_2024, EXAM_2025]
