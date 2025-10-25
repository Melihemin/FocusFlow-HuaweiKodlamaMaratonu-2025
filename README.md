### 🏆 This repository took 2nd place in the "Kodlama Maratonu 2025" competition, organized by @Huawei and @BTK.

# FocusFlow: AI-Powered Learning for ADHD

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-development-green.svg)]()

**FocusFlow** is an advanced EdTech platform developed by **Code N’ Vision** for the Huawei Turkey Kodlama Maratonu 2025. Our project aligns with Sustainable Development Goal 4 (Quality Education) by providing a data-driven, personalized learning experience for students with **ADHD (Attention-Deficit/Hyperactivity Disorder)**.

FocusFlow is designed to improve the quality of life and learning for students with ADHD. In this app, users can learn various lessons (e.g., math, physics, biology, soft skills) through a highly personalized interface. The system recommends content and videos specifically chosen based on user-provided data, such as learning type, focus span, and ADHD subtype.

---

## 📖 Table of Contents

* [About The Project](#-about-the-project)
* [Key Features](#-key-features)
* [Technical Architecture](#-technical-architecture)
    * [Cloud Architecture (Huawei Cloud)](#cloud-architecture-huawei-cloud)
    * [AI Architecture (RAG)](#ai-architecture-rag)
* [Tech Stack](#-tech-stack)
* [Demo](#-demo)
* [Our Team](#-our-team)
* [License](#-license)

## About The Project

Students with ADHD often struggle to maintain focus in traditional educational settings. FocusFlow addresses this challenge by creating a unique learning environment for each student. Our platform actively measures a user's focus level in real-time and dynamically adapts the content (text, videos, and quizzes) to match their attention span and learning style.

Our goal is to contribute to equality in education by enabling every student to reach their full potential.

## Key Features

* **Personalized Learning (RAG)**: Generates a unique stream of educational content using a RAG (Retrieval-Augmented Generation) model, tailored to the student's learning pace, focus span, and ADHD profile.
* **Eye-Tracking & Focus Measurement**: An active focus module that tracks eye and mouse movements during study sessions to analyze the student's attention level in real-time.
* **Personal Analysis Panel**: A comprehensive dashboard for students and parents displaying heatmaps, focus duration, completed lessons, and performance metrics.
* **Gamified Experience**: Engages students and boosts motivation through point systems, competitive leaderboards, and achievement badges.
* **Data-Driven & GDPR/KVKK Compliant**: Securely analyzes all user data to provide the most accurate content recommendations within a privacy-compliant framework.

## Technical Architecture

Our platform is built on two robust, scalable, and high-performance architectures: a Huawei Cloud infrastructure and a RAG-based AI model.

### Cloud Architecture (Huawei Cloud)

Our services are securely hosted on a scalable Huawei Cloud infrastructure:

1.  **User Access**: Users access the platform via the internet.
2.  **Load Balancer (ELB)**: Incoming traffic is managed by an Elastic Load Balancer (ELB) to prevent system overloads during peak hours (e.g., after school).
3.  **Container Engine (CCE)**: Our application runs on CCE (Cloud Container Engine) as two main pod groups:
    * **Pod 1 (Application Service)**: Hosts the Frontend (JavaScript) and Backend (FastAPI) services.
    * **Pod 2 (AI Service)**: Runs the RAG architecture and other compute-heavy AI models.
4.  **Database (RDS - PostgreSQL)**: All user data, profiles, focus metrics, quiz results, and progress records are stored in a high-performance **PostgreSQL** Relational Database Service (RDS).
5.  **Storage (OBS - Object Storage Service)**: All static and large files, such as lesson documents (DOCX, PDF), logs, and media, are securely stored in OBS.
6.  **Network (VPC & NAT Gateway)**: All services operate within an isolated Virtual Private Cloud (VPC). A NAT Gateway is used to allow AI services to securely access external APIs (e.g., Gemini) without being exposed to the internet.

---
<img width="1322" height="500" alt="Ekran Resmi 2025-10-25 12 59 15" src="https://github.com/user-attachments/assets/1bc18ef5-77ff-4e07-af1c-7c8e38a853bb" />
---

### AI Architecture (RAG)

Content personalization is achieved through our RAG (Retrieval-Augmented Generation) architecture:

1.  **Query**: A user selects a topic, initiating a query.
2.  **Contextualization**: The query is enriched with user data (focus span, learning type, ADHD profile) retrieved from the **RDS (PostgreSQL)** database to create a "mega-prompt".
3.  **Retrieval**:
    * The system retrieves relevant lesson documents from **OBS (Object Storage)**.
    * A **FAISS** vector database is used to find the most relevant "context" chunks matching the user's enriched prompt.
4.  **Generation**:
    * The "mega-prompt" and the retrieved "context" are sent to a fine-tuned LLM (**Gemini 1.5 Flash**).
    * The LLM generates two types of output:
        1.  A personalized text-based lesson plan.
        2.  A dynamic web search query (using Gemini Tools) to find the most suitable video for the user's profile.
5.  **Serve & Save**: The generated content (text and video) is served to the user. This successful "match" (e.g., "User X with 10min focus span was served content Y") is saved back to the **RDS (PostgreSQL)** database to create a feedback loop for future model training.

---
<img width="1404" height="761" alt="Ekran Resmi 2025-10-25 12 58 55" src="https://github.com/user-attachments/assets/1f071299-5136-401c-a213-18132f9b8878" />
---

## Tech Stack

| Category | Technology |
| :--- | :--- |
| **Cloud Provider** | Huawei Cloud |
| **Container & Orchestration**| Huawei CCE (Kubernetes) |
| **Database** | Huawei RDS (PostgreSQL) |
| **Storage** | Huawei OBS |
| **Backend** | FastAPI (Python) |
| **Artificial Intelligence** | RAG, Gemini 1.5 Flash, FAISS |
| **AI/ML Monitoring** | LangChain / LangSmith |

## Demo

Watch our full project demo, including a detailed walkthrough of the features and architecture, on YouTube:

[**FocusFlow | Code N' Vision - Project Explanation (YouTube)**](https://www.youtube.com/watch?v=KnRb824DJA8)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
