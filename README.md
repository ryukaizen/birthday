<p align="center" width="100%">
<img src="https://freesvg.org/img/birthday-cake.png" width="100" height="100">
</p>

# Birthday Greeter
Scheduled birthday greeting script. Made using PyMongo, smtplib and PIL.

## Features
1. Automated emailing of wishes.
    - Scheduled delivery at 12:00 AM (midnight).
    - Random birthday wishes.
    - Current age calculation.
2. Birthday card generation using Pillow.
    - Random birthday card backgrounds.
    - Send as an attachment with emails.
3. MongoDB as database.
    - Add or remove birthdays.
    - Show upcoming birthdays.
    - List every birthday.

---

## Table of Contents
1. [Before you start (what you need)](#1-before-you-start-what-you-need)
2. [Install Python](#2-install-python)
3. [Install Git](#3-install-git)
4. [Download this project](#4-download-this-project)
5. [Install the required packages](#5-install-the-required-packages)
6. [Set up MongoDB Atlas (the database)](#6-set-up-mongodb-atlas-the-database)
7. [Set up a Gmail App Password (to send emails)](#7-set-up-a-gmail-app-password-to-send-emails)
8. [Create your `.env` settings file](#8-create-your-env-settings-file)
9. [Run the program](#9-run-the-program)
10. [Keep it running every day](#10-keep-it-running-every-day)
11. [Troubleshooting](#11-troubleshooting)
12. [Security tips](#12-security-tips)

---

## 1. Before you start (what you need)
- A computer (Windows, macOS or Linux) that is **switched on and connected to the internet** at midnight if you want automatic greetings.
- A free **MongoDB Atlas** account (Step 6).
- A **Gmail** account to send the greetings from (Step 7).
- About 30 minutes.

> **Tip:** Anything shown in a grey box is something you type into the **Terminal** (macOS/Linux) or **Command Prompt / PowerShell** (Windows).
> - Windows: press the `Windows` key, type `cmd`, press Enter.
> - macOS: press `Cmd + Space`, type `Terminal`, press Enter.
> - Linux: press `Ctrl + Alt + T`.

---

## 2. Install Python
Python is the programming language this project runs on. **pip** (the tool that installs extra packages) comes bundled with it.

### Windows
1. Go to <https://www.python.org/downloads/> and click the yellow **Download Python 3.x** button.
2. Open the downloaded file.
3. **IMPORTANT:** On the first screen, tick the box **"Add python.exe to PATH"**, then click **Install Now**.
4. When it finishes, click **Close**.

### macOS
1. Go to <https://www.python.org/downloads/macos/> and download the latest installer.
2. Open it and follow the steps (Continue → Agree → Install).

### Linux (Ubuntu / Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv -y
```

### Check it worked
Open a **new** Terminal / Command Prompt window and type:
```bash
python --version
pip --version
```
(On macOS/Linux you may need to use `python3` and `pip3` instead of `python` and `pip`. Use whichever works, and keep using it for the rest of this guide.)

You should see something like `Python 3.12.x`. Python 3.8 or newer is required.

---

## 3. Install Git
Git is used to download the project.

- **Windows:** download from <https://git-scm.com/download/win>, run the installer and click **Next** through all the screens (the defaults are fine).
- **macOS:** in Terminal type `git --version`. If it isn't installed, macOS will offer to install it. Click **Install**.
- **Linux:** `sudo apt install git -y`

Check it worked:
```bash
git --version
```

> **No Git? No problem.** On the project page, click the green **Code** button → **Download ZIP**, then unzip it and skip to Step 4's "move into the folder" part.

---

## 4. Download this project
In your Terminal, go to a folder where you want to keep it (for example your Documents folder) and run:
```bash
cd Documents
git clone https://github.com/ryukaizen/birthday.git
cd birthday
```
You are now "inside" the project folder. All the next commands must be run from here.

### (Recommended) Create a virtual environment
This keeps the project's packages separate from the rest of your computer.

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```
**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```
You should now see `(venv)` at the start of your command line. Every time you open a new terminal to run this project, activate it again with the last command above.

---

## 5. Install the required packages
```bash
pip install -r requirements.txt
pip install click requests pillow
```
> The second line installs a few packages that the script uses but are not yet listed in `requirements.txt`. Running both is safe.

---

## 6. Set up MongoDB Atlas (the database)
MongoDB Atlas is a free online database where your list of birthdays is stored. The screens are occasionally redesigned by MongoDB, but the steps and names below stay essentially the same.

### 6.1 Create an account
1. Go to <https://www.mongodb.com/cloud/atlas/register>.
2. Sign up with Google, GitHub, or an email and password.
3. Verify your email if asked, then log in.
4. If asked a few welcome questions (goal, experience, etc.), answer anything or click **Skip**.

### 6.2 Create a free cluster
1. Click **Create** (or **Build a Database** / **+ Create** under *Clusters*).
2. Choose the **M0 / Free** plan.
3. Pick any cloud provider (AWS is fine) and a region close to you.
4. Give it a name (for example `Cluster0`), then click **Create Deployment** (or **Create Cluster**).
5. Wait 1–3 minutes for it to be created.

### 6.3 Create a database user (a username + password for the script)
Atlas usually shows a "Connect to Cluster" pop-up right after creation with this step. If not, in the left menu go to **Security → Database Access → Add New Database User**.
1. Choose **Password** authentication.
2. Enter a username, e.g. `birthdayuser`.
3. Enter a password. Click **Autogenerate Secure Password** and **copy it somewhere safe**.
   - Prefer letters and numbers only. If your password contains special characters like `@ : / ? # %`, they must be URL-encoded in the connection string (see [Troubleshooting](#11-troubleshooting)).
4. Under privileges, choose **Read and write to any database** (or the built-in role `readWriteAnyDatabase`).
5. Click **Add User**.

### 6.4 Allow your computer to connect (Network Access)
1. In the left menu go to **Security → Network Access → Add IP Address**.
2. Click **Add Current IP Address** and then **Confirm**.
3. If your computer's internet address changes often (most home internet does) or you're running this on a different machine, you can instead enter `0.0.0.0/0` ("Allow access from anywhere"). This is less secure, but it is protected by your username and password. Only do this if you need to.

### 6.5 Create the database and collection
Atlas needs a database name and a collection (like a "table") name. You will put both into your `.env` file later.
1. In the left menu click **Database** (or **Clusters**), then click **Browse Collections** on your cluster.
2. Click **+ Create Database** (or **Add My Own Data**).
3. Database name: `birthdaydb` (or anything you like).
4. Collection name: `birthdays` (or anything you like).
5. Click **Create**.

Write both names down. You don't need to add any data by hand. The program will ask you for it (Step 9).

### 6.6 Get your connection string (MongoDB URL)
1. In the left menu click **Database** (or **Clusters**).
2. On your cluster, click **Connect**.
3. Choose **Drivers**.
4. Select **Python** and the latest version.
5. Copy the connection string shown. It looks like this:
   ```
   mongodb+srv://birthdayuser:<db_password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0
   ```
6. Replace `<db_password>` (or `<password>`) with the password from Step 6.3. **Remove the `<` and `>` brackets too.**
   Example: `mongodb+srv://birthdayuser:MyPass123@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority`

Keep this string private. It's the key to your database.

---

## 7. Set up a Gmail App Password (to send emails)
Gmail doesn't allow scripts to log in with your normal password. You need a special 16-character **App Password**.

1. Go to <https://myaccount.google.com/security> and sign in to the Gmail account that will send the greetings.
2. Turn on **2-Step Verification** (follow Google's steps) if it isn't already on.
3. Go to <https://myaccount.google.com/apppasswords> (or search "App passwords" in the search bar of your Google Account page).
4. Type a name like `Birthday Greeter` and click **Create**.
5. Google shows a 16-character password. **Copy it right away.** You won't see it again. Spaces don't matter.

> If you can't find "App passwords", 2-Step Verification is probably not on, or your account is a work/school account where the administrator has disabled it.

---

## 8. Create your `.env` settings file
This file holds your private settings. It is ignored by Git so it won't get uploaded by accident.

1. In the project folder, make a copy of `.env.example` named `.env`:
   - **Windows:** `copy .env.example .env`
   - **macOS / Linux:** `cp .env.example .env`
2. Open `.env` in Notepad (Windows) or TextEdit (macOS) / any text editor.
3. Fill in the values:

```env
GMUSER = youremail@gmail.com
GMPASS = abcdefghijklmnop
HOST = smtp.gmail.com
PORT = 587

MONGO_URI = mongodb+srv://birthdayuser:MyPass123@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority
DB_NAME = birthdaydb
COLLECTION_NAME = birthdays
```

| Setting | What to put |
|---|---|
| `GMUSER` | The Gmail address that sends the greetings |
| `GMPASS` | The 16-character App Password from Step 7 (**not** your normal password) |
| `HOST` / `PORT` | Leave as `smtp.gmail.com` and `587` |
| `MONGO_URI` | The connection string from Step 6.6 with the password filled in |
| `DB_NAME` | The database name from Step 6.5 |
| `COLLECTION_NAME` | The collection name from Step 6.5 |

> **Important:** The program reads the variable named **`MONGO_URI`**. The older `.env.example` file calls it `MONGO_URL`. If your file says `MONGO_URL`, rename it to `MONGO_URI`, otherwise the program can't connect to the database.
>
> Do not add quotation marks, and do not put comments (`# ...`) on the same line as a value.

Save the file.

---

## 9. Run the program
Make sure you're in the project folder and your virtual environment is active (you see `(venv)`), then run:
```bash
python main.py
```
(Use `python3 main.py` on macOS/Linux if needed.)

The program will check today's birthdays and then ask you some yes/no questions:

| Question | What it does |
|---|---|
| Check upcoming birthday/s? | Shows birthdays later this month |
| List all birthday entries? | Shows everyone saved |
| Add new birthday/s? | Lets you add people (see below) |
| Remove any existing birthday/s? | Lets you delete someone |

Press **Enter** to accept the default (`Y`), or type `n` then Enter to skip.

### Adding a birthday
Choose **yes** at "Add new birthday/s?" and answer each prompt:
```
Enter name: Alice
Enter email: alice@example.com
Enter birthday day: 5
Enter birthday month: 11
Enter birthday year: 1995
```
- Type day and month **without a leading zero** (`5`, not `05`).
- Type the year with 4 digits.
- When asked `Enter "n" to continue adding, "y" if you're done adding`, type `n` to add another person or `y` (or just press Enter) to finish and save.

You can check the data in Atlas: **Database → Browse Collections**.

### Test it
Add yourself with **today's** date and your own email, then run `python main.py` again. You should receive a birthday email with a card attached.

When you've answered all the questions, the program prints that the greeting job is running and stays open, waiting for midnight. To stop it, press `Ctrl + C`.

---

## 10. Keep it running every day
The program checks for birthdays at **00:00 (midnight)** every day, but **only while the program is running and the computer is on**. Closing the terminal or turning off the PC stops it.

Also note: at each midnight run the program asks the same questions as in Step 9, so it works best when it is left running in a terminal window. For truly unattended use, run it on an always-on computer or server.

### Option A: Simple (keep the window open)
Leave the terminal window open and don't let the computer sleep. (Windows: Settings → System → Power → set "Sleep" to Never.)

### Option B: Always-on Linux server / Raspberry Pi
```bash
sudo apt install screen -y
screen -S birthday
cd ~/birthday
source venv/bin/activate
python main.py
```
Press `Ctrl + A` then `D` to leave it running in the background. Return to it with `screen -r birthday`.

---

## 11. Troubleshooting

| Problem | Likely fix |
|---|---|
| `'python' is not recognized` (Windows) | Reinstall Python and tick **Add python.exe to PATH**, then open a new Command Prompt. |
| `'git' is not recognized` | Install Git (Step 3) and open a new terminal. |
| `ModuleNotFoundError: No module named ...` | Run `pip install -r requirements.txt` and `pip install click requests pillow`. Make sure `(venv)` is active. |
| `pymongo.errors.ServerSelectionTimeoutError` / timeout | Your IP isn't allowed. Add it in Atlas → **Network Access** (Step 6.4). Also check your internet connection. |
| `Authentication failed` / `bad auth` | Wrong username or password in `MONGO_URI`. Make sure you removed the `< >` brackets. |
| Password has special characters (`@ : / ? # %`) | URL-encode them (e.g. `@` → `%40`, `#` → `%23`, `/` → `%2F`, `:` → `%3A`) or create a new password with only letters and numbers. |
| `The DNS query name does not exist` / SRV error | Check the connection string is copied fully. Try a different network (some networks block it) or run `pip install dnspython`. |
| `SSL` / certificate errors | Update Python and run `pip install --upgrade pymongo certifi`. On macOS, run "Install Certificates.command" in your Python folder in Applications. |
| `TypeError: ... MongoClient ... None` or `Invalid URI` | `.env` isn't being read or the variable is misnamed. Ensure the file is named exactly `.env` (not `.env.txt`), is in the project folder, and uses `MONGO_URI`. |
| `SMTPAuthenticationError (535)` | Use the 16-character **App Password**, not your normal password. Make sure 2-Step Verification is on. |
| Email lands in spam | Mark it "Not spam" once; sending from a personal Gmail account to a few people usually works fine. |
| `OSError: cannot open resource` (font) | Run the program from inside the project folder so `assets/fonts/GrandHotel-Regular.ttf` can be found. |
| No email sent on a birthday | Check the birthday's day/month were entered without leading zeros, and that the program was running at midnight. |
| Windows hides file extensions so `.env` is really `.env.txt` | In File Explorer: **View → Show → File name extensions**, then rename it. |

---

## 12. Security tips
- **Never** share or upload your `.env` file, your MongoDB connection string, or your Gmail App Password. The `.env` file is already listed in `.gitignore`.
- If you think a password was exposed, delete the Gmail App Password and create a new one, and change the Atlas database user's password (**Database Access → Edit**).
- Prefer adding only your own IP in Atlas Network Access instead of `0.0.0.0/0` whenever possible.
- Give the database user only the access it needs.

---

## To-do
- [ ] Input timeout

- [ ] Custom greetings

- [ ] Print if there are no upcoming birthdays
