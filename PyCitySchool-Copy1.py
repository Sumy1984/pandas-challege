#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Dependencies
import pandas as pd
import os
import numpy as np


# In[2]:


#define path
schools_file = os.path.join("schools_complete.csv")
students_file = os.path.join("students_complete.csv")


# In[3]:


#read csv
schools_df = pd.read_csv(schools_file)
students_df = pd.read_csv(students_file)


# In[4]:


# Combine the data into a single dataset.  
school_data_complete = pd.merge(schools_df, students_df, how="left", on=["school_name", "school_name"])
school_data_complete.head()


# ## District Summary

# In[5]:


# Calculate the total number of unique schools
unique_school_names = schools_df['school_name'].unique()
print(unique_school_names)


# In[6]:


school_count = len(unique_school_names)
print(school_count)


# In[7]:


# Calculate the total number of students
student_count = schools_df['size'].sum()
print (student_count)


# In[8]:


# Calculate the total budget
total_budget = schools_df['budget'].sum()
print(total_budget)


# In[9]:


# Calculate the average (mean) math score
average_math_score = students_df['math_score'].mean()
print(average_math_score)


# In[10]:


# Calculate the average (mean) reading score
average_reading_score =  students_df['reading_score'].mean()
print( average_reading_score)


# In[11]:


# calculate the percentage of students who passed math (math scores greather than or equal to 70)
passing_math_count = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"]
passing_math_percentage = passing_math_count / float(student_count) * 100
passing_math_percentage


# In[12]:


# Calculate the percentage of students who passed reading 
passing_reading_count = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"]
passing_reading_percentage = passing_reading_count / float(student_count) * 100
passing_reading_percentage


# In[13]:


# Use the following to calculate the percentage of students that passed math and reading
passing_math_reading_count = school_data_complete[
    (school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)
].count()["student_name"]
overall_passing_rate = passing_math_reading_count /  float(student_count) * 100
overall_passing_rate


# In[14]:


# Create a high-level snapshot of the district's key metrics in a DataFrame
district_summary = pd.DataFrame({
    
    "Total Schools": [school_count],
    "Total Students": [student_count],
    "Total Budget": [total_budget],
    "Average Math Score": [average_math_score],
    "Average Reading Score": [average_reading_score],
    "Passing Math%": [passing_math_percentage],
    "Passing Reading%":[passing_reading_percentage],
     "Overall Passing Rate": [overall_passing_rate]})

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## School Summary 

# In[15]:


# school type
school_types = schools_df.set_index(["school_name"])["type"]
school_types


# In[16]:


# Calculate the total student count
by_school = school_data_complete.set_index('school_name').groupby(['school_name'])
stu_per_sch = by_school['Student ID'].count()
stu_per_sch


# In[17]:


# school budget
sch_budget = schools_df.set_index('school_name')['budget']
sch_budget


# In[18]:


#student budget 
stu_budget = schools_df.set_index('school_name')['budget']/schools_df.set_index('school_name')['size']
stu_budget


# In[19]:


# Calculate the average test scores
per_school_math =  by_school['math_score'].mean()
per_school_math


# In[20]:


# Calculate the average test scores
per_school_reading = by_school['reading_score'].mean()
per_school_reading


# 

# In[21]:


# Calculate the number of schools with math scores of 70 or higher

pass_math = school_data_complete[school_data_complete['math_score'] >= 70]
pass_math


# In[22]:


# Calculate the number of schools with reading scores of 70 or higher
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70]
pass_read


# In[23]:


# Use the provided code to calculate the schools that passed both math and reading with scores of 70 or higher
passing_math_and_reading = school_data_complete[
    (school_data_complete["reading_score"] >= 70) & (school_data_complete["math_score"] >= 70)]
passing_math_and_reading


# In[24]:


# Use the provided code to calculate the passing rates
per_school_passing_math = pass_math.groupby(["school_name"]).count()["student_name"] / stu_per_sch * 100
per_school_passing_reading = pass_read.groupby(["school_name"]).count()["student_name"] / stu_per_sch * 100
overall_passing_rate = passing_math_and_reading.groupby(["school_name"]).count()["student_name"] / stu_per_sch * 100


# In[25]:


district_summary = pd.DataFrame({
    "School Type": school_types,
    "Total Students": stu_per_sch,
    "Per Student Budget": stu_budget,
    "Total Budget": sch_budget,
    "Average Math Score": per_school_math,
    "Average Reading Score": per_school_reading,
    '% Passing Math': per_school_passing_math,
    '% Passing Reading': per_school_passing_reading,
    "Overall Passing Rate": overall_passing_rate})

# Formatting
district_summary["Total Students"] = district_summary["Total Students"].map("{:,}".format)
district_summary["Total Budget"] = district_summary["Total Budget"].map("${:,.2f}".format)
district_summary["Per Student Budget"] = district_summary["Per Student Budget"].map("${:,.2f}".format)

# Display the DataFrame
district_summary


# ## Highest-Performing Schools (by % Overall Passing)

# In[26]:


# sort values by passing rate and then only print top 5 
top_5 = district_summary.sort_values("Overall Passing Rate", ascending = False)
top_5.head()


# ## Bottom Performing Schools (By % Overall Passing)

# In[35]:


# Sort the schools by `% Overall Passing` in ascending order and display the top 5 rows.
bottom_5 = district_summary.sort_values(["Overall Passing Rate"], ascending=True)
bottom_5.head()


# ## Math Scores by Grade

# In[28]:


ninth_math = students_df.loc[students_df['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = students_df.loc[students_df['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = students_df.loc[students_df['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = students_df.loc[students_df['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores_by_grade= math_scores[['9th', '10th', '11th', '12th']]
math_scores_by_grade.index.name = None

#show 
math_scores_by_grade


# ## Reading Score by Grade

# In[29]:


#creates grade level average reading scores for each school
ninth_reading = students_df.loc[students_df['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_reading = students_df.loc[students_df['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_reading = students_df.loc[students_df['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_reading = students_df.loc[students_df['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

#merges the reading score averages by school and grade together
reading_scores_by_grade = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading
})
reading_scores_by_grade = reading_scores_by_grade[['9th', '10th', '11th', '12th']]
reading_scores_by_grade.index.name = None

#show
reading_scores_by_grade


# ## Scores by School Spending

# In[36]:


# Establish the bins 
spending_bins = [0, 585, 630, 645, 680]
group_name = ["<$585", "$585-630", "$630-645", "$645-680"]


# In[37]:


# Create a copy of the school summary since it has the "Per Student Budget" 
school_spending_df = district_summary.copy()


# In[40]:


# Use `pd.cut` to categorize spending based on the bins.
school_spending_df['spending_bins'] = pd.cut( district_summary["Per Student Budget"]spending_bins, labels = group_name, include_lowest=True)
school_spending_df


# In[ ]:


# Create a group based off of the bins
school_spending_df = school_spending_df.groupby('Per Student Budget').mean()
school_spending_df.head()


# In[ ]:


spending_math_scores = school_spending_df.groupby(["Spending Ranges (Per Student)"]).mean()["Average Math Score"]


# ## Scores by School Size

# In[ ]:


# Establish the bins.
size_bins = [0, 1000, 2000, 5000]
group_names = ["Small (<1000)", "Medium (1000-2000)", "Large (2000-5000)"]


# In[ ]:


# Create a new data frame by locating the desired columns
scores_size = district_summary.loc[:,['Average Math Score',
                                  'Average Reading Score','% Passing Math',
                                  '% Passing Reading','Overall Passing Rate',]]
# Add a new columns named School Size and binning based off total students
scores_size['School Size']= pd.cut(district_summary['Total Students'],size_bins, labels = group_names, include_lowest=True)
# Create a group based off of the bins
scores_size = scores_size.groupby('School Size').mean()
scores_size.head()



# In[ ]:


"School Type": school_types,
   "Total Students": stu_per_sch,
   "Per Student Budget": stu_budget,
   "Total Budget": sch_budget,
   "Average Math Score": per_school_math,
   "Average Reading Score": per_school_reading,
   '% Passing Math': per_school_passing_math,
   '% Passing Reading': per_school_passing_reading,
   "Overall Passing Rate": overall_passing_rate})


# In[ ]:


#calculations
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    '% Passing Math': pass_math,
    '% Passing Reading': pass_read,
    "Overall Passing Rate": overall})
scores_by_spend.index.name = "Per Student Budget"
scores_by_spend = scores_by_spend.reindex(group_name)


# In[ ]:





# In[ ]:





# In[ ]:




