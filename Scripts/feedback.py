import matplotlib.pyplot as plt
import numpy as np
# Adjusted data for the revised questionnaire
categories_revised = ['How effective do you find the system', 'Accuracy and Relevance', 'System Scalability',
                      'Document Processing', 'Speed and Responsiveness', 'Customization and Adaptability',
                      'User Interface and Usability', 'Overall Satisfaction']
ratings_revised = [7.5, 8.3, 7.0, 8.0, 6.8, 7.5, 8.2, 7.8]

# Setting up the plot
fig, ax = plt.subplots(figsize=(14, 8))
colors_revised = plt.cm.viridis(np.linspace(0, 1, len(categories_revised)))

# Creating the bar plot
bars_revised = ax.barh(categories_revised, ratings_revised, color=colors_revised, alpha=0.8)

# Adding labels, title, and customizing the axes for the adjusted questionnaire
ax.set_xlabel('Average Ratings', fontsize=14)
ax.set_title('Feedback Analysis with Focus on Future Development', fontsize=16, fontweight='bold')
ax.set_xlim(0, 10)
ax.invert_yaxis()  # Reverse the order to have the highest rating at the top
ax.tick_params(axis='both', which='major', labelsize=12)

# Adding numerical ratings next to each bar for clarity
for bar in bars_revised:
    width = bar.get_width()
    ax.annotate(f'{width}',
                xy=(width, bar.get_y() + bar.get_height() / 2),
                xytext=(3, 0),  # 3 points horizontal offset
                textcoords="offset points",
                ha='left', va='center', fontsize=12)

plt.tight_layout()
plt.show()
