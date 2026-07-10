# 📚 CourseFit: Registration Planner

> An intelligent course registration planning system that helps students generate valid, conflict-free course schedules using graph algorithms and scheduling optimization techniques.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-red)
![Algorithms](https://img.shields.io/badge/Algorithms-Graph%20Theory-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📖 Overview

CourseFit is a smart registration planner designed to simplify the university course enrollment process.

Students often struggle with:

- Course prerequisite validation
- Time-table conflicts
- Choosing the best course combinations
- Manual planning errors

CourseFit automates this process by applying **Graph Theory**, **Topological Sorting**, **Interval Scheduling**, and **Optimization Algorithms** to generate feasible and efficient course registration plans.

---

## 🎯 Problem Statement

Manual course registration becomes increasingly difficult as the number of available courses grows.

Students need to:

- Verify prerequisite chains
- Avoid timetable clashes
- Maximize credit utilization
- Select the best combination of courses

CourseFit addresses these challenges by automatically generating valid schedules while satisfying all academic constraints.

---

# ✨ Features

- 📌 Prerequisite Validation
- 📅 Conflict-Free Timetable Generation
- 📊 Course Dependency Visualization
- ⚡ Fast Registration Planning
- 🧠 Graph-based Course Modeling
- 📈 Schedule Optimization
- 💻 Interactive Streamlit Interface
- 📂 CSV Dataset Support

---

# 🏗️ System Architecture

```
                Course Dataset
                      │
                      ▼
            Data Preprocessing
                      │
                      ▼
         Graph Construction (DAG)
                      │
                      ▼
      Topological Sorting (DFS)
                      │
                      ▼
     Interval Scheduling Algorithm
                      │
                      ▼
       Optimized Registration Plan
                      │
                      ▼
        Streamlit User Interface
```

---

# 🧮 Algorithms Used

## 1. Directed Acyclic Graph (DAG)

Each course is represented as a node.

Each prerequisite is represented as a directed edge.

Example:

```
Programming-I
      │
      ▼
Programming-II
      │
      ▼
Data Structures
      │
      ▼
Algorithms
```

---

## 2. Topological Sorting

Used to:

- Validate prerequisite order
- Detect cyclic dependencies
- Generate feasible learning paths

**Time Complexity**

```
O(V + E)
```

where

- V = Number of Courses
- E = Number of Prerequisites

---

## 3. Interval Scheduling

Ensures selected courses do not overlap in timing.

Greedy strategy:

- Sort classes by finish time
- Select earliest finishing compatible class

Time Complexity:

```
O(n log n)
```

---

## 4. Dynamic Programming (Optional Optimization)

Used for weighted scheduling where:

- Credits
- Priority
- Importance

are considered while selecting courses.

---

# ⚙️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend Logic |
| Streamlit | Web Interface |
| Pandas | Data Processing |
| NetworkX | Graph Operations |
| Matplotlib | Graph Visualization |
| CSV | Dataset Storage |

---

# 📂 Project Structure

```
CourseFit/
│
├── app.py
├── scheduler.py
├── graph_utils.py
├── dataset/
│     ├── courses.csv
│     └── prerequisites.csv
│
├── assets/
│
├── requirements.txt
│
├── README.md
│
└── screenshots/
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/your-username/coursefit-registration-planner.git
```

Go to project folder

```bash
cd coursefit-registration-planner
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Streamlit application

```bash
streamlit run app.py
```

---

# 📊 Workflow

```
Input Course Data
        │
        ▼
Read CSV Files
        │
        ▼
Create Course Graph
        │
        ▼
Check Prerequisites
        │
        ▼
Detect Cycles
        │
        ▼
Topological Sorting
        │
        ▼
Check Time Conflicts
        │
        ▼
Apply Scheduling Algorithm
        │
        ▼
Generate Best Registration Plan
        │
        ▼
Display Results
```

---

# 📈 Complexity Analysis

| Operation | Complexity |
|------------|------------|
| Graph Construction | O(V + E) |
| DFS | O(V + E) |
| Topological Sort | O(V + E) |
| Greedy Scheduling | O(n log n) |
| Dynamic Programming | O(n²) |

---

# 🎯 Advantages

- Eliminates manual scheduling errors
- Prevents prerequisite violations
- Detects timetable clashes automatically
- Generates optimized course combinations
- Easy to use
- Fast execution
- Scalable for large university datasets

---

# 🔮 Future Scope

- 🤖 AI-based Course Recommendation
- 🎓 Degree Progress Tracking
- ☁️ University ERP Integration
- 📱 Mobile Application
- 🔔 Registration Notifications
- 👥 Collaborative Academic Planning
- 📊 Predictive Course Demand Analysis

---

# 📸 Screenshots

Add screenshots of the application here.

```
screenshots/
├── home.png
├── planner.png
├── graph.png
└── output.png
```

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository

2. Create a new branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push the branch

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 👨‍💻 Team

**CourseFit Development Team**

- Antik Mondal
- Soumyo Jeet
- *Add other team members here*

---

# 📚 References

- Introduction to Algorithms – Cormen, Leiserson, Rivest & Stein (CLRS)
- Graph Theory by Narsingh Deo
- Streamlit Documentation
- Python Official Documentation
- NetworkX Documentation

---

# 📄 License

This project is licensed under the MIT License.

---

## ⭐ If you found this project useful, please consider giving it a Star on GitHub!

```
⭐ Star this repository
🍴 Fork the project
🐞 Report issues
💡 Suggest new features
```
