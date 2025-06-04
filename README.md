# Netfix

## Overview
Netfix is a web platform designed to connect **customers** with **companies** providing various home services. Whether it's **plumbing, interior design, or housekeeping**, customers can request services, and companies can manage their offerings seamlessly.

## Features
- **User Authentication**:
  - Customers and Companies can register and log in.
  - Unique email and username enforcement.
  - Profile pages displaying relevant details.

- **Service Management**:
  - Companies create services based on their specialization.
  - "All in One" companies can offer all service types.
  - Customers can view and request services.

- **Service Requests**:
  - Customers specify **address** and **service duration** when requesting.
  - Request history with calculated cost and provider details.
  - Most requested services list.

- **Navigation & Filtering**:
  - View services **by category**.
  - See **latest services** (newest first).
  - Click company names to explore their offerings.

## Tech Stack
- **Backend**: Django 3.1.14 (Python)
- **Database**: PostgreSQL (or SQLite for local development)
- **Caching & Optimization**: Redis (optional)
- **Authentication**: Django’s built-in system

## Project Structure
