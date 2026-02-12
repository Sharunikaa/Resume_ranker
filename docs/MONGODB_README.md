# MongoDB Setup & Usage Guide

This guide explains how to create a MongoDB database and use it with the Resume Ranker app.

---

## What is MongoDB?

MongoDB is a **document database**. This project uses it to store:

- **jobs** – job postings and extracted requirements  
- **candidates** – resume data, scores, rankings, and insights  

You can use either **MongoDB Atlas** (cloud, free tier) or **MongoDB on your computer** (local).

---

## Option 1: MongoDB Atlas (Cloud, Recommended)

Atlas is MongoDB’s hosted service. Free tier is enough for this project.

### Step 1: Create an account and cluster

1. Go to **[https://www.mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)**  
2. Sign up (Google/Email).  
3. Create an **organization** and **project** if asked (you can keep defaults).  
4. Click **Build a Database**.  
5. Choose **M0 (FREE)** and a region near you.  
6. Click **Create**.  
7. Wait until the cluster status is **Active**.

### Step 2: Create a database user

1. In the left sidebar: **Database Access** → **Add New Database User**.  
2. **Authentication:** Password.  
3. Choose a **username** and **password** (save them; you’ll need them for the connection string).  
4. Under **Database User Privileges**, leave **Atlas admin** or choose **Read and write to any database**.  
5. Click **Add User**.

### Step 3: Allow network access

1. In the left sidebar: **Network Access** → **Add IP Address**.  
2. For quick setup: choose **Allow Access from Anywhere** (`0.0.0.0/0`).  
3. Confirm.  
4. For production, you’d restrict this to your server IP.

### Step 4: Get the connection string

1. Go back to **Database** (left sidebar).  
2. Click **Connect** on your cluster.  
3. Choose **Drivers** (or “Connect your application”).  
4. Copy the connection string. It looks like:

   ```text
   mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
   ```

5. Replace `<username>` and `<password>` with the database user you created.  
6. If the password contains special characters (e.g. `#`, `@`, `%`, `&`), **URL-encode** them:
   - [URL encode tool](https://www.urlencoder.org/)  
   - Example: `pass#123` → `pass%23123`

### Step 5: Use it in this project

1. In the project folder, copy the env template:

   ```bash
   cp .env.example .env
   ```

2. Open `.env` and set:

   ```env
   MONGODB_URI=mongodb+srv://YOUR_USER:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=resume_ranker
   ```

   Use your real username, (encoded) password, and cluster hostname from the connection string.

3. You do **not** need to create the database or collections yourself. The app will create the **resume_ranker** database and the **jobs** and **candidates** collections when you run it and create a job or upload a resume.

---

## Option 2: Local MongoDB (On Your Computer)

### Install (macOS with Homebrew)

```bash
brew tap mongodb/brew
brew install mongodb-community@8.0
brew services start mongodb-community@8.0
```

### Use it in this project

1. Copy env and set in `.env`:

   ```env
   MONGODB_URI=mongodb://localhost:27017
   DATABASE_NAME=resume_ranker
   ```

2. The app will create the **resume_ranker** database and the **jobs** and **candidates** collections when you use the app.

---

## How the app uses MongoDB

- The app reads **MONGODB_URI** and **DATABASE_NAME** from `.env`.  
- It connects to MongoDB when the backend starts.  
- When you **create a job** in the UI, a document is stored in the **jobs** collection.  
- When you **upload and process resumes**, documents are stored in the **candidates** collection.  
- No need to create the database or collections manually; they are created on first use.

---

## How to view your data

### If you use MongoDB Atlas

1. In Atlas: **Database** → **Browse Collections** on your cluster.  
2. Select the **resume_ranker** database.  
3. Open **jobs** or **candidates** to see documents.

You can also use **mongosh** (MongoDB Shell) with your Atlas connection string:

```bash
mongosh "mongodb+srv://YOUR_USER:YOUR_PASSWORD@YOUR_CLUSTER.mongodb.net/"
```

Then:

```bash
use resume_ranker
show collections
db.jobs.find().pretty()
db.candidates.find().pretty()
```

### If you use local MongoDB

1. Open a terminal and run:

   ```bash
   mongosh
   ```

2. Then run:

   ```bash
   show dbs
   use resume_ranker
   show collections
   db.jobs.find().pretty()
   db.candidates.find().pretty()
   ```

- **show dbs** – list databases  
- **use resume_ranker** – switch to this app’s database  
- **show collections** – list collections (e.g. `jobs`, `candidates`)  
- **db.jobs.find().pretty()** – show all jobs  
- **db.candidates.find().pretty()** – show all candidates  

---

## Troubleshooting

| Issue | What to do |
|--------|------------|
| Connection timeout / cannot connect | **Atlas:** Check Network Access allows your IP (or `0.0.0.0/0`). **Local:** Ensure MongoDB is running: `brew services list` and start it if needed. |
| Authentication failed | **Atlas:** Confirm username/password and that special characters in the password are URL-encoded in **MONGODB_URI**. |
| Database or collection not found | Normal before first use. Create a job or upload a resume in the app; the database and collections will be created automatically. |
| Where do I set the connection string? | In the project root, in the **.env** file (copy from **.env.example**). Use **MONGODB_URI** and **DATABASE_NAME**. |

---

## Summary

1. **Create** a MongoDB database: use **Atlas** (cloud) or **install MongoDB locally**.  
2. **Get** a connection string (Atlas) or use `mongodb://localhost:27017` (local).  
3. **Put** `MONGODB_URI` and `DATABASE_NAME=resume_ranker` in `.env`.  
4. **Run** the app; it will create the database and collections when you create a job or add candidates.  
5. **View** data in Atlas (Browse Collections) or with **mongosh** as shown above.
