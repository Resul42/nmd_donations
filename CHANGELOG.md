# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- De emails worden uitgelezen.
- voor elke product in een unieke email wordt deze opgeslagen in de database (per project is een row insect)
- nadat deze zijn opgeslagen wordt er een in de Command line een log gedaan met de donatie met de verwachte opzet ( Bilal Kocak - Sadaqa (€100,00) - 0612345678)
- De mail server wordt nu elk 10 seconden uitgelezen en wordt er in de database gecheckt of deze email al verwerkt is, zo ja stipt ie m zo niet wordt deze verwerkt en gelogd.
- De unique identifier hiervoor is de donatienummer vanuit de subject van de email.
- Added comprehensive logging to show that the application is running and waiting for emails
