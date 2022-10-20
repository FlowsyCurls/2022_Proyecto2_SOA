from vision import routine
import threading

# Create a thread and run the producer function
analyze_thread = threading.Thread(target=routine, args=())
analyze_thread.start()
