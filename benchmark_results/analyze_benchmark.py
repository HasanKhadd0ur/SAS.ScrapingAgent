import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("benchmark_stats.csv")

# Calculate stats
total_messages = df["messages_processed"].sum()
total_time = df["time_seconds"].sum()
avg_msgs_per_sec = total_messages / total_time

print(f"✅ Total messages processed: {total_messages}")
print(f"⏱️  Total time taken: {total_time:.2f} seconds")
print(f"📈 Average throughput: {avg_msgs_per_sec:.2f} messages/second")

# --- Plot 1: Messages processed per task ---
plt.figure(figsize=(12, 5))
plt.plot(df["task_index"], df["messages_processed"], marker="o", linestyle="-", color="teal")
plt.title("Messages Processed Per Task")
plt.xlabel("Task Index")
plt.ylabel("Messages Processed")
plt.grid(True)
plt.tight_layout()
plt.savefig("messages_per_task.png")  # Saves the plot
plt.show()

# --- Plot 2: Cumulative messages processed over time ---
df["cumulative_messages"] = df["messages_processed"].cumsum()
df["cumulative_time"] = df["time_seconds"].cumsum()

plt.figure(figsize=(12, 5))
plt.plot(df["cumulative_time"], df["cumulative_messages"], color="purple", linewidth=2)
plt.title("Cumulative Messages Processed Over Time")
plt.xlabel("Time (seconds)")
plt.ylabel("Cumulative Messages")
plt.grid(True)
plt.tight_layout()
plt.savefig("cumulative_messages.png")
plt.show()
