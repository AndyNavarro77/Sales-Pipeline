# 📊 Sales Data Pipeline — End-to-End Business Analytics

> **ETL pipeline that transforms raw sales data into strategic business intelligence — from Excel source to interactive Power BI dashboard, with automated KPIs, performance alerts, and a daily HTML email report delivered every morning.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![MySQL](https://img.shields.io/badge/MySQL-8.0-orange?logo=mysql)](https://mysql.com)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi)](https://powerbi.microsoft.com)
[![Pandas](https://img.shields.io/badge/Pandas-ETL-green?logo=pandas)]()
[![Automation](https://img.shields.io/badge/Automation-Task%20Scheduler-blue)]()
[![Status](https://img.shields.io/badge/Status-Active-brightgreen)]()

---

## 🧠 The Business Problem

Most companies accumulate sales data in Excel files, disconnected systems, or manual reports. The result:

- **No real-time visibility** over revenue, volume, or rep performance
- **Decisions based on intuition** rather than current data
- **Operational inefficiencies** that go undetected until it's too late
- **Missed growth opportunities** hidden inside raw transactional data

A sales manager shouldn't need to wait for a weekly report to know that a rep is underperforming or that a product category is driving 60% of revenue.

**This pipeline eliminates that blind spot.**

---

## ✅ The Solution

An end-to-end data pipeline that simulates a real business environment: new sales records are generated and ingested daily, cleaned and enriched, aggregated by key business dimensions, loaded into a relational database, and surfaced through an interactive dashboard — with a professional HTML email report delivered automatically every morning and built-in performance alerts that fire when reps fall below threshold.

> *Every day the dataset grows, the KPIs update, and the report lands in the inbox — just like a real sales operation.*

---

## 📐 Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Excel File    │───▶│  Python ETL      │───▶│   MySQL DB      │
│  (ventas.xlsx)  │    │  etl_ventas.py   │    │  (5 tables)     │
└─────────────────┘    └──────────────────┘    └────────┬────────┘
                                                         │
                              ┌──────────────────────────▼──────────┐
                              │         Power BI Dashboard           │
                              │  (KPIs · Trends · Rep Performance)   │
                              └─────────────────────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                           │
     ┌────────▼────────┐       ┌─────────▼──────────┐               │
     │ Task Scheduler  │       │   Alert Engine +    │               │
     │ (Daily trigger) │       │   HTML Email Report │               │
     └─────────────────┘       └────────────────────┘               │
```

---

## 🔄 Pipeline — Step by Step

| Step | Action | Technology | Business Value |
|------|--------|------------|----------------|
| 1 | Generate and ingest new sales records daily | Python · openpyxl | Simulates real operational data — dataset grows every run |
| 2 | Clean, type-cast and compute revenue | Python · pandas | Ensures consistent, analysis-ready data |
| 3 | Generate business aggregations | Python · pandas | Pre-built views by day, product, rep, channel |
| 4 | Detect underperforming sales reps | Python · pandas | Proactive alert before manual discovery |
| 5 | Generate structured daily report | Python | Revenue, units, avg ticket, top rep, top product, channel split |
| 6 | Load transactions + aggregations to MySQL | SQLAlchemy · SQL | Centralized, queryable data store — 5 tables |
| 7 | Send HTML email report | Python · smtplib | Professional daily briefing delivered to inbox automatically |
| 8 | Visualize KPIs and trends | Power BI | Decision-ready insights at a glance |
| 9 | Daily automated execution | Windows Task Scheduler | Zero manual intervention |

---

## 📊 Dashboard

The Power BI dashboard was built for business users — every view answers a specific operational question:

![Sales Dashboard](img/sales_dashboard.png)

**What it surfaces:**

- **KPI Cards:** Max Sale · Total Revenue · Sales Volume · Avg. Ticket · Sales Status
- **Daily Revenue Trend** — time-series line chart tracking revenue fluctuations across the month
- **Revenue by Sales Representative** — ranked bar chart to instantly spot top and bottom performers
- **Channel Distribution** — Online vs. in-store revenue split (donut chart)
- **Revenue by Product Category** — horizontal bar chart ranking products by total contribution

---

## ✉️ Live Proof — It Actually Runs

This pipeline isn't just code — it runs in production every day via Task Scheduler. New sales records are added on each execution, KPIs update automatically, and this report lands in the inbox every morning:

![Email Report](img/email_report.png)

**What the daily email surfaces:**
- Today's Revenue · Units Sold · Avg. Ticket · Top Rep
- Online vs. in-store channel split with percentages
- Top product by revenue
- Total records processed
- Performance alert status — green if all clear, amber if a rep is underperforming

> The numbers change every day because the dataset is live — 30 new sales records are ingested on each run, simulating real business activity.

---

## 🔔 Built-in Alert Engine

The pipeline evaluates business performance automatically on every run:

**Underperforming rep detection** — if any rep's revenue falls below 50% of the average:
```
⚠ Low performance detected: [Rep Name]
```

**Below-average total sales** — if total revenue falls below the historical average:
```
⚠ Sales below average threshold
```

Both alerts are embedded directly in the email report — color-coded green (all clear) or amber (action needed).

---

## 💡 Key Results & Value Delivered

| Before | After |
|--------|-------|
| Manual Excel review to track performance | Automated aggregations by rep, product, channel, day |
| No visibility on underperforming reps | Named alerts triggered automatically on each run |
| Static snapshots with no trend analysis | Interactive time-series dashboard with full history |
| Revenue calculations done by hand | Pipeline computes revenue, avg ticket, and volume automatically |
| No daily briefing for management | Professional HTML email report delivered every morning |
| Data siloed in Excel files | Centralized MySQL database ready for any BI tool |

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| Data Generation | Python · numpy · random | Realistic sales simulation — 5,000+ records, grows daily |
| Extraction | Python · openpyxl | Excel ingestion with incremental updates |
| Transformation | Python · pandas | Cleaning, revenue calc, type-casting |
| Aggregation | Python · pandas | Pre-built views: by day, product, rep, channel |
| Storage | MySQL 8.0 · SQLAlchemy | 5-table relational schema — transactions + aggregations |
| Visualization | Power BI | Interactive dashboard and KPI reporting |
| Alerting | Python (built-in) | Performance threshold detection on every run |
| Reporting | Python · smtplib | HTML email report with live KPIs |
| Scheduling | Windows Task Scheduler | Automated daily pipeline execution |

---

## 📁 Repository Structure

```
Sales-Pipeline/
│
├── etl_ventas.py              # Main ETL — extract, transform, aggregate, alert, email, load
├── generar_datos_ventas.py    # Data generator — 5,000 realistic sales records
├── requirements.txt           # Python dependencies
├── schema.sql                 # MySQL database schema — ready to deploy
├── .env.example               # Environment variables template (no credentials)
├── LICENSE                    # MIT License
├── dashboard/
│   └── dashboard_ventas.pbix  # Power BI dashboard file
├── data/
│   ├── ventas.xlsx            # Raw sales source — grows on every pipeline run
│   ├── ventas_limpio.csv      # Cleaned transactions
│   ├── ventas_por_dia.csv     # Aggregation: daily revenue
│   ├── ventas_por_producto.csv# Aggregation: by product
│   ├── ventas_por_vendedor.csv# Aggregation: by sales rep
│   └── ventas_por_canal.csv   # Aggregation: by channel
├── img/
│   ├── sales_dashboard.png    # Dashboard screenshot
│   └── email_report.png       # Daily email report screenshot
└── README_ES.md               # Spanish version
```

---

## 👤 Author

**Andrés Navarro**
Data Analyst · BI · ETL · Python · SQL

[![GitHub](https://img.shields.io/badge/GitHub-AndyNavarro77-black?logo=github)](https://github.com/AndyNavarro77)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://www.linkedin.com/in/andr%C3%A9s-navarro77/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-orange?logo=netlify)](https://andres-navarro-portfolio.netlify.app/)

---

*Built to simulate a real business scenario where data drives daily decisions — demonstrating end-to-end data engineering, automated reporting, and business-oriented analytics applicable to any sales-driven organization.*