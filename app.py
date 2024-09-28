from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import nest_asyncio
import asyncio
from urllib.parse import urlparse

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Use /help for instructions.")

# Function to display help instructions
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "Instructions:\n"
        "1. Use /setcookies <cookies_string> to set your cookies manually.\n"
        "   Example: /setcookies session_id=123; csrftoken=abc;\n"
        "2. Use /apply_job <job_url> to apply for a job automatically.\n"
        "   Example: /apply_job https://www.linkedin.com/jobs/view/12345678\n"
    )
    await update.message.reply_text(help_text)

# Function to set cookies manually
async def set_cookies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) < 1:
        await update.message.reply_text("Please provide your cookies after the command.")
        return
    cookies = ' '.join(context.args)  # Join arguments to form the cookies string
    context.bot_data[user_id] = cookies
    await update.message.reply_text("Cookies saved successfully!")

# Function to fetch cookies automatically (now unused)
def fetch_cookies(job_url):
    session = requests.Session()
    
    # Set a User-Agent header
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        # Fetch the job page to get cookies
        response = session.get(job_url, headers=headers)
        
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to fetch job page. Status code: {response.status_code}")
            return None
        
        # Extract cookies
        cookies_dict = session.cookies.get_dict()
        
        if not cookies_dict:
            print("No cookies found.")
            return None

        return cookies_dict
    
    except requests.RequestException as e:
        print(f"Error fetching cookies: {e}")
        return None

# Function to apply for jobs on LinkedIn
def apply_linkedin(job_url, cookies):
    session = requests.Session()
    session.cookies.update(cookies)
    
    # Here you would implement the actual LinkedIn job application logic
    print(f"Automatically applying to LinkedIn job at {job_url} using cookies.")
    return f"Applied to LinkedIn job: {job_url}"

# Function to apply for jobs on Internshala
def apply_internshala(job_url, cookies):
    session = requests.Session()
    session.cookies.update(cookies)
    
    # Here you would implement the actual Internshala job application logic
    print(f"Automatically applying to Internshala job at {job_url} using cookies.")
    return f"Applied to Internshala job: {job_url}"

# Command to apply for jobs
async def apply_job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if len(context.args) < 1:
        await update.message.reply_text("Please provide a job URL after the command.")
        return

    job_url = context.args[0]

    # Validate the URL
    parsed_url = urlparse(job_url)
    if parsed_url.netloc not in ['www.linkedin.com', 'internshala.com']:
        await update.message.reply_text("Please provide a valid LinkedIn or Internshala job URL.")
        return

    # Retrieve the manually set cookies
    cookies_string = context.bot_data.get(user_id)
    
    if not cookies_string:
        await update.message.reply_text("Please set your cookies first using /setcookies.")
        return

    # Convert cookies string to a dictionary
    cookies = {item.split('=')[0]: item.split('=')[1] for item in cookies_string.split('; ')}

    # Apply for the job
    if "linkedin" in job_url:
        result = apply_linkedin(job_url, cookies)
        await update.message.reply_text(result)
    elif "internshala" in job_url:
        result = apply_internshala(job_url, cookies)
        await update.message.reply_text(result)

# Main function
async def main():
    app = ApplicationBuilder().token("7846806097:AAFiEm0oIGs8LGXjQ5Z3pJiZqWIlCXm3cmk").build()
    app.add_handler(CommandHandler('start', start))  # Add the /start command handler
    app.add_handler(CommandHandler('help', help_command))  # Add the /help command handler
    app.add_handler(CommandHandler('setcookies', set_cookies))  # Add the /setcookies command handler
    app.add_handler(CommandHandler('apply_job', apply_job))  # Add the /apply_job command handler
    await app.run_polling()

# Entry point
if __name__ == '__main__':
    asyncio.run(main())
