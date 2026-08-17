# Phishing Datasets

This directory is intended to store raw and processed datasets for training the machine learning models.

## Expected Format
The training script expects a CSV file named `emails.csv` (or similar) with at least two columns:
- `text`: The raw email body/subject content.
- `label`: `0` for legitimate, `1` for phishing.

Replace `dummy_dataset.csv` with a large production dataset when ready.
