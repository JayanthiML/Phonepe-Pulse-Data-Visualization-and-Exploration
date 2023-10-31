# Phonepe Pulse Data Visualization Project

## Overview

This project aims to extract, transform, and visualize data from the Phonepe Pulse GitHub repository, providing valuable insights and information in an interactive and user-friendly dashboard.
We create a web app to analyse the Phonepe transaction and users depending on various Years, Quarters, States, and Types of transaction and give a Geographical and Geo visualization output based on given requirements.

## Problem Statement

The Phonepe Pulse GitHub repository contains a large amount of data related to various metrics and statistics. The goal is to extract this data and process it to obtain insights and information that can be visualized in a user-friendly manner.

## Usage

The dashboard provides various dropdown options for users to select different facts and figures to display. It allows easy navigation and data analysis.

### Project Steps

1. **Data Extraction**: Clone the GitHub repository using scripting to fetch the data and store it in a suitable format.

2. **Data Transformation**: Use Python and Pandas to manipulate and preprocess the data, including cleaning and transforming it for analysis.

3. **Database Insertion**: Utilize "mysql-connector-python" to insert the transformed data into a MySQL database for efficient storage and retrieval.

4. **Dashboard Creation**: Create an interactive and visually appealing dashboard using Streamlit and Plotly in Python to display the data. The dashboard should allow users to select various facts and figures.

5. **Data Retrieval**: Fetch data from the MySQL database to display on the dashboard, enabling dynamic updates.

6. **Deployment**: Ensure the solution is secure and user-friendly. Deploy the dashboard for public access.

## Getting Started

To get started with this project, follow these steps:

1. Install required Modules and Libraries.
2. ETL Process.
   - Extract: Clone the GitHub repository.
   - Transform: Transform and preprocess the data using the provided scripts.
   - Load: Insert the data into a MySQL database.
3. Fetch the data from MySQL database to transform and visualise.
4. Create and run the Streamlit and Plotly dashboard.
5. Access the dashboard in your web browser to explore the insights.

## Install required Modules and Libraries

I have included Requirements.txt file. To install the required modules and libraries at once:  
  -  Download the file and save in your project directory.
  -  using command prompt navigate to project directory.
  -  Run the following command to install all the packages listed in the Requirements.txt file using pip:

     pip install -r Requirements.txt

## Clone the GitHub repository

Data Link provided in the pdf file contains the GitHub repository of PhonePe Pulse Data. 
You can directly download the file to local storage or clone it using python scripting to local storage.

## Transform and preprocess the data

Process the data and transform into DataFrames.

## Insert the data into a MySQL database

Connect to MySQL database, create database, create tables, insert the dataframes to the tables.

## Fetch the data from MySQL database to transform and visualise

Fetch the data stored in MySQL database and transform it to required formats to visualise the data using streamlit and ploty

## Create and run the Streamlit and Plotly dashboard

Create an interactive dashboard for analysing and visualising the data.

## Access the dashboard in your web browser to explore the insights

Access the dashboard and analyse the data.

## Tools Used
    - Python (3.11.4)
    - VS Code - for .py and .ipynb
    - MySQL
    - GitHub Repository
    - GeoJson data 

## User Guide

Step 1: Select any one option from All India or State wise or Top Ten categories.  
Step 2: Select any one option from Transaction or User.  
Step 3: Select any Year, Quarter and additional required option.  
Step 4: Finally, You get the Geo Visualization Analysis or Bar chart Analysis and Table format Analysis.  
