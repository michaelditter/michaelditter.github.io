#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def create_ai_readiness_chart():
    # Data for AI readiness across industries
    industries = [
        'Financial Services', 
        'Technology', 
        'Healthcare', 
        'Manufacturing', 
        'Retail', 
        'Energy',
        'Transportation'
    ]
    
    # Readiness scores (0-100) for each dimension
    strategic_clarity = [78, 82, 65, 58, 63, 55, 59]
    data_maturity = [75, 80, 62, 60, 67, 57, 54]
    tech_infrastructure = [72, 85, 60, 65, 70, 62, 61]
    talent_skills = [70, 88, 58, 52, 56, 48, 50]
    governance = [80, 72, 68, 55, 58, 60, 52]
    
    # Calculate overall readiness (average of all dimensions)
    overall = []
    for i in range(len(industries)):
        avg = (strategic_clarity[i] + data_maturity[i] + tech_infrastructure[i] + 
               talent_skills[i] + governance[i]) / 5
        overall.append(avg)
    
    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Width of bars
    width = 0.13
    
    # Position of bars on x-axis
    ind = np.arange(len(industries))
    
    # Creating bars
    bar1 = ax.bar(ind - 2.5*width, strategic_clarity, width, label='Strategic Clarity')
    bar2 = ax.bar(ind - 1.5*width, data_maturity, width, label='Data Maturity')
    bar3 = ax.bar(ind - 0.5*width, tech_infrastructure, width, label='Tech Infrastructure')
    bar4 = ax.bar(ind + 0.5*width, talent_skills, width, label='Talent & Skills')
    bar5 = ax.bar(ind + 1.5*width, governance, width, label='Governance')
    bar6 = ax.bar(ind + 2.5*width, overall, width, label='Overall', color='darkblue')
    
    # Add labels, title, and custom x-axis tick labels
    ax.set_xlabel('Industry', fontweight='bold', fontsize=12)
    ax.set_ylabel('Readiness Score (0-100)', fontweight='bold', fontsize=12)
    ax.set_title('AI Readiness Scores by Industry (2023)', fontweight='bold', fontsize=14)
    ax.set_xticks(ind)
    ax.set_xticklabels(industries, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    
    # Adding the legend and placing it at the top-right
    ax.legend(loc='upper right', ncols=3)
    
    # Add a grid for easier reading
    ax.yaxis.grid(True, linestyle='--', alpha=0.7)
    
    # Add source reference
    plt.figtext(0.12, 0.01, "Source: Based on Deloitte's State of AI 2023 report", 
                fontsize=9, color='gray')
    
    # Tight layout to ensure everything fits well
    plt.tight_layout()
    
    # Create the output directory if it doesn't exist
    img_dir = Path("img/blog")
    img_dir.mkdir(parents=True, exist_ok=True)
    
    # Save the chart
    output_path = img_dir / "ai-readiness-chart.jpg"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Created AI readiness chart: {output_path}")
    
    # Close the plot to free memory
    plt.close()

if __name__ == "__main__":
    create_ai_readiness_chart() 