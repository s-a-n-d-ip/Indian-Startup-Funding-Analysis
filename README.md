# Startup Funding Analysis Dashboard

## Overview

Startup Funding Analysis Dashboard is an interactive data analytics application built using **Streamlit**, **Pandas**, **Matplotlib**, and **Scikit-learn**. The application allows users to analyze startup funding trends, investor behavior, startup details, and discover similar investors using cosine similarity.

The dashboard provides a user-friendly interface for exploring startup funding data and gaining insights into investments across sectors and years.

---

## Features

### Overall Analysis

Provides a high-level view of startup funding data:

* Total funding amount invested
* Top 5 highest funded startups
* Year-wise funding trend
* Top sectors by investment amount
* Month-on-month funding trend

---

### Startup Analysis

Allows users to explore individual startup details:

* Startup sector information
* Sub-sector information
* City/location information
* Investment history
* Funding rounds
* Investor details

---

### Investor Analysis

Provides detailed information about investors:

* Recent investments
* Largest investments
* Sector distribution
* Yearly investment trends
* Similar investors recommendation system

---

### Investor Recommendation Engine

The application uses **Cosine Similarity** to identify investors with similar investment patterns.

#### Steps:

1. Split investor names
2. Create Investor × Vertical matrix
3. Convert matrix into numerical vectors
4. Compute cosine similarity
5. Return top similar investors

---

## Tech Stack

Frontend:

* Streamlit

Backend/Data Processing:

* Pandas
* NumPy

Visualization:

* Matplotlib

Machine Learning:

* Scikit-learn
* Cosine Similarity

---

## Project Structure

```bash
Startup-Funding-Analysis/
│
├── streamlit_doc.py
├── cleaned_startup_funding.csv
├── README.md
├── requirements.txt
└── assets/
```

---

## Dataset Information

Dataset contains startup funding details such as:

| Column      | Description        |
| ----------- | ------------------ |
| startup     | Startup name       |
| investors   | Investor names     |
| vertical    | Startup sector     |
| subvertical | Startup sub-sector |
| city        | Startup location   |
| round       | Funding round      |
| amount      | Investment amount  |
| date        | Funding date       |

---

## Installation

Clone the repository:

```bash
git clone https://github.com/s-a-n-d-ip/Indian-Startup-Funding-Analysis.git
```

Move to project directory:

```bash
cd startup-funding-analysis
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Requirements
Install:

```bash
pip install -r requirements.txt
```

## Run Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will run at:

```bash
http://localhost:8501
```

---

## Dashboard Screens

### Overall Dashboard

Shows:

* Total funding amount
* Top funded startups
* Sector analysis
* Investment trends

### Startup Dashboard

Shows:

* Startup details
* Funding history
* Investor information

### Investor Dashboard

Shows:

* Recent investments
* Investment distribution
* Similar investors

---

## Future Improvements

Potential enhancements:

* Add startup recommendation engine
* Interactive Plotly visualizations
* Investor clustering using KMeans
* NLP-based startup similarity search
* City-wise heatmaps
* Advanced filtering
* Deploy using Docker and AWS

---

## Author

Sandip Ghosh

Machine Learning & Data Science Enthusiast

---

## License

This project is licensed under the MIT License.
