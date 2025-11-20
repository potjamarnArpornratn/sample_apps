#!/usr/bin/env python3

"""
Authored by: Potjamarn Arpornratn
Date: Nov 20, 2025

This script parses text files in a given folder and compose the contents as dictionary feedback objects.
Usage: python file_parser.py
"""

from __future__ import annotations
import os
import requests
import logging

# Constants
HEADER_LINE_COUNT = 3

logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def parse_file_contents(file_path: str) -> list[str]:
    """Read and return the contents of a file as a list of strings.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        UnicodeDecodeError: If the file contains invalid UTF-8 characters.
    """
    logger.info(f"Parsing file contents from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as data_file:
            contents = data_file.readlines()
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode file {file_path}: {e}")
        raise
    return contents

def generate_dictionary_from_contents(contents: list[str]) -> dict:
    """Generate a dictionary from a list of strings using title, name, date, and feedback as keys"""
    if len(contents) < HEADER_LINE_COUNT:
        raise ValueError(f"File must contain at least {HEADER_LINE_COUNT} lines (title, name, date). Found {len(contents)} lines.")
    
    results = {}

    results['title'] = contents[0].strip()
    results['name'] = contents[1].strip()
    results['date'] = contents[2].strip()
    
    # Extract and validate feedback
    if len(contents) == HEADER_LINE_COUNT:
        results['feedback'] = ''
        logger.warning("Feedback content is empty.")
    else:
        feedback_lines = [line.strip() for line in contents[HEADER_LINE_COUNT:]]
        results['feedback'] = '\n'.join(feedback_lines)
    
    logger.info(f"Generated dictionary from contents: {results}")

    return results

def post_feedback(feedback_dict: dict, url: str) -> requests.Response:
    """Post the feedback dictionary to the specified URL and return the response.
    
    Raises:
        requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        requests.RequestException: If a network error occurred.
    """
    response = requests.post(url, json=feedback_dict)
    response.raise_for_status()
    logger.info(f"Feedback posted successfully with status code {response.status_code}.")
    return response

# Sample code to demonstrate usage
if __name__ == "__main__":
    data_dir = "./data/feedback/"
    logger.info(f"Data directory set to {data_dir}")

    for filename in os.listdir(data_dir):   
        data_file_path = os.path.join(data_dir, filename)
        
        # Skip if not a file
        if not os.path.isfile(data_file_path):
            logger.info(f"Skipping {filename} (not a file)")
            continue
        
        try:
            contents = parse_file_contents(data_file_path)
            logger.info(f"****** contents of file: {filename} ******")
            feedback_dict = generate_dictionary_from_contents(contents)
            print(feedback_dict)
        except (FileNotFoundError, UnicodeDecodeError, ValueError) as e:
            logger.error(f"Failed to process {filename}: {e}")
            continue
        except Exception as e:
            logger.error(f"Unexpected error processing {filename}: {e}")
            continue
