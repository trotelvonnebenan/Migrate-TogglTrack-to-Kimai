# Toggl Track to Kimai 2 Client Migrator

A lightweight Python utility to migrate **Clients** from Toggl Track to **Kimai 2** (v2.2+). 

This script automates the transition by creating **Customers** in Kimai and automatically generating a **corresponding Project** for each customer with the same name. It is designed to be idempotent, meaning you can run it multiple times without creating duplicate entries.

## ✨ Features
* **Duplicate Prevention:** Checks Kimai for existing customer names before creation.
* **Auto-Project Creation:** Automatically creates and links a project to every customer.
* **Localization:** Defaults to **Austria (AT)**, **EUR**, and **Europe/Vienna** (configurable).
* **Security:** Uses environment variables (`.env`) to keep your API keys safe.

---

## 🔑 Where to find your Tokens

### 1. Toggl Track API Token
* Log in to [Toggl Track](https://track.toggl.com/).
* Click on your profile icon (bottom left) -> **Profile Settings**.
* Scroll to the very bottom to the **API Token** section.
* Click "Click to reveal" and copy the token.

### 2. Toggl Workspace ID
* Log in to Toggl web.
* Click on your **Organization** or **Reports**.
* Look at the URL in your browser: `track.toggl.com/reports/summary/1234567`.
* The number `1234567` is your **Workspace ID**.

### 3. Kimai API Token
* Log in to your Kimai instance.
* Click on your user profile (top right) -> **Edit**.
* Select the **API Access** tab.
* Generate a new **API Token** (Personal Access Token).
* *Note: Ensure your Kimai user has "Manage Customer" and "Manage Project" permissions.*

---

## 🛠 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/toggl-to-kimai-migrator.git](https://github.com/yourusername/toggl-to-kimai-migrator.git)
   cd toggl-to-kimai-migrator

2. **Install dependencies:**
   ```bash
   pip install requests python-dotenv

3. **Create a `.env` file:**
   ```bash
   cp .env.example .env
   # Edit the .env file with your credentials

4. **Run the script:**
   ```bash
   python migrate_clients.py