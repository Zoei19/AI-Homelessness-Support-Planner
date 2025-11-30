# Homelessness Support Planner

AI-powered agent system to assess risk and generate personalized action plans for vulnerable individuals.

## Problem Statement

Vulnerable individuals often need structured support. This project automates risk assessment, recommends services, identifies required documents, and generates actionable plans in HTML/PDF format.

## Why Agents?

Agents can handle multi-step decision-making efficiently, integrating tools like postcode lookup, service database, and document guidance to provide personalized recommendations.

## Features

* Multi-agent pipeline: risk assessment, service recommendation, document checklist, action plan generation (HTML/PDF)
* Memory bank stores session context
* Local tools: CSV service database, postcode geolocation, HTML/PDF generator
* Output validation for scenario testing

## Demo

1. Load a scenario JSON (`evaluation/scenario1.json`)
2. Run `python runner.py`
3. View outputs in `logs/` including HTML/PDF plan

## Architecture

[User Input] → [Agents A1 → A2 → A3 → A4] → [Memory Bank] → [Tools] → [HTML/PDF Plan]

## Build / Tech Stack

* Python 3.11
* Google ADK agents
* Tools: CSV, pdfkit, HTML templates
* Local testing: Windows 10 / venv

## Future Improvements

* Live service API integration for real-time updates
* NLP summarization for plan highlights
* Multi-language support

## Usage
bash
python runner.py
Outputs are stored in `logs/` folder.
