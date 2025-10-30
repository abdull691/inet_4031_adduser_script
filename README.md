# INET 4031 – Automated User Creation Script

## 🧾 Overview
This repository contains a Python script used to automate the creation of user accounts and groups on an Ubuntu Linux system.  
It was developed as part of **Lab 8 (Part 2)** for the **INET 4031: Linux System Administration** course.

The script reads user account details from a text input file (`create-users.input`) and then creates corresponding accounts, assigns passwords, and adds users to appropriate groups using Linux command-line utilities.

---

## ⚙️ Repository Contents
| File Name | Description |
|------------|--------------|
| `create-users.py` | The original version of the automation script. Reads user data from `stdin` and executes Linux commands to create users and groups. |
| `create-users2.py` | An improved version of the script that adds an **interactive prompt** to choose between dry-run or real-run modes. |
| `create-users.input` | Input data file containing colon-delimited user details. |
| `README.md` | This documentation file explaining setup, usage, and operation. |

---

### 🔹 Input Format
Each line of the input file must contain **five colon-separated fields** in this order:
