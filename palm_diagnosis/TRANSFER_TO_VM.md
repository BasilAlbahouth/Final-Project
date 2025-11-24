# How to Transfer This Project to Windows VM

## Option 1: Copy Files Directly (Easiest)

1. **Copy the entire project folder:**
   - Copy `C:\Users\Basil\DjangoProjects\palm_diagnosis` folder
   - Paste it into your Windows VM (e.g., `C:\Users\YourName\DjangoProjects\palm_diagnosis`)

2. **On the VM, install Python and dependencies:**
   ```bash
   # Install Python 3.8+ if not already installed
   # Then install dependencies:
   cd C:\Users\YourName\DjangoProjects\palm_diagnosis
   py -m pip install -r requirements.txt
   ```

3. **Run migrations and start server:**
   ```bash
   py manage.py migrate
   py manage.py runserver
   ```

## Option 2: Create a ZIP Archive

1. **Create a ZIP file of the project:**
   - Right-click on `palm_diagnosis` folder
   - Select "Send to" > "Compressed (zipped) folder"
   - Transfer the ZIP to your VM

2. **On the VM:**
   - Extract the ZIP file
   - Follow steps 2-3 from Option 1

## Option 3: Use Git (Recommended for Development)

1. **Initialize Git repository:**
   ```bash
   cd C:\Users\Basil\DjangoProjects\palm_diagnosis
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push to GitHub/GitLab or use shared folder:**
   - Create a repository on GitHub/GitLab
   - Push the code
   - Clone on your VM

## Option 4: Shared Folder (VMWare/VirtualBox)

1. **Set up shared folder between host and VM**
2. **Copy project to shared folder**
3. **Access from VM and follow installation steps**

## Important Notes:

- **Database file:** The `db.sqlite3` file will be copied, but you may want to run `migrate` again on the VM
- **Static files:** Run `py manage.py collectstatic` on the VM if needed
- **Python version:** Make sure Python 3.8+ is installed on the VM
- **Dependencies:** Always run `pip install -r requirements.txt` on the VM

## Quick Setup Script for VM

After copying files to VM, run:
```bash
cd C:\path\to\palm_diagnosis
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py collectstatic --noinput
py manage.py runserver
```

