import asyncio
import csv
import logging
import os
import sys
from pathlib import Path
from typing import Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, SecretStr
from PyPDF2 import PdfReader

from browser_use import ActionResult, Agent, Controller
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.browser.context import BrowserContext

from openai import OpenAI

import uuid

# Validate required environment variables
load_dotenv()
required_env_vars = ['OPENAI_API_KEY']
for var in required_env_vars:
	if not os.getenv(var):
		raise ValueError(f'{var} is not set. Please add it to your environment variables.')

logger = logging.getLogger(__name__)
# full screen mode
controller = Controller()

CV = Path.cwd() / 'cv_04_24.pdf'




@controller.action('Read my cv for context to fill forms')
def read_cv():
		pdf = PdfReader(CV)
		text = ''
		for page in pdf.pages:
			text += page.extract_text() or ''
		logger.info(f'Read cv with {len(text)} characters')
		return ActionResult(message=text, include_in_memory=True)


@controller.action('Save the information about the job to a text file in the job_details folder')
def save_job_information(job_information:str):
		directory = r"job_details"
		os.makedirs(directory, exist_ok=True)
		filename = f"{uuid.uuid4().hex}.txt"
		filepath = os.path.join(directory, filename)
		with open(filepath, 'w', encoding='utf-8') as f:
			f.write(job_information)
		return ActionResult(message=f"Saved job information to {filepath}", include_in_memory=True)



browser = Browser(
	config=BrowserConfig(
		disable_security=True,
	)
)

async def main():
	model = ChatOpenAI(model="gpt-4o-mini")
	

	task = [
		"""1. Go to https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=f3528c8d-9e21-4a8c-a4c0-5f7c82288f0f&ccId=19000101_000001&selectedMenuKey=CurrentOpenings&jobId=531048"
		2. Find the job description and save it to a text file using save_job_information"""
	]

	"""agents = []
	for task in tasks:"""

	agent = Agent(task=task, llm=model, controller=controller, browser=browser)
	#agents.append(agent)

	#await asyncio.gather(*[agent.run() for agent in agents])
	await agent.run()


asyncio.run(main())

