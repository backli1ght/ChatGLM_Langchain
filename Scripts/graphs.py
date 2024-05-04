from matplotlib import pyplot as plt
# Sample data for types of hallucinations
hallucinations = ['Incorrect Facts', 'Nonsensical Responses', 'Irrelevant Responses']
percentages = [30, 50, 20]

# Plot pie chart
fig, ax = plt.subplots()
ax.pie(percentages, labels=hallucinations, autopct='%1.1f%%', startangle=90, colors=['#FF9999','#66B3FF','#99FF99'])
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Add title
ax.set_title('Types of Hallucinations')

# Save the figure
file_path = '/mnt/data/hallucinations_pie_chart.png'
plt.savefig(file_path)

file_path
